import tkinter as tk
from tkinter import messagebox, scrolledtext, Scrollbar
from tkcalendar import DateEntry
from datetime import datetime
from controllers.rental_controller import list_available_spaces, rent_parking_space, \
      get_user_rentals, validate_plate
from data.storage import parking_spaces

class ParkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EasyPark")
        self.canvas = None
        self.tooltip = None
        self.create_main_menu()

    def draw_map(self):
        # Get the start and end dates from the entries
        start_time_str = self.start_date_entry.get() + " " + self.start_time_entry.get()
        end_time_str = self.end_date_entry.get() + " " + self.end_time_entry.get()
        self.start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
        self.end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M")

        # Get available lots
        available_lots = list_available_spaces(self.start_time, self.end_time)

        if self.canvas:
            self.canvas.destroy()
        if self.tooltip:
            self.tooltip.destroy()
        
        self.canvas = tk.Canvas(self.root, height=600, width=600)
        self.canvas.pack()
        
        # Draw the parking lot map
        self.rectangles = {}
        for space in parking_spaces.values():
            free_space = space in available_lots
            color = "blue" if free_space else "red"
            offsetx = 10
            offsety = 40
            x = 4 * space.x + offsetx
            y = 4 * space.y + offsety
            width = 4 * space.width
            height = 4 * space.height

            rect = self.canvas.create_rectangle(
                x, y, x + width, y + height,
                fill=color, tags=str(space.space_id)
            )
            self.rectangles[space.space_id] = rect

            # Bind events for hover and click
            if free_space:
                self.canvas.tag_bind(rect, "<Enter>", lambda event, s=space: self.show_tooltip(event, s))
                self.canvas.tag_bind(rect, "<Leave>", self.hide_tooltip)
                self.canvas.tag_bind(rect, "<Button-1>", lambda event, s=space: self.rent_space(s))

        self.tooltip = tk.Label(self.root, text="", bg="yellow", relief="solid", bd=1, wraplength=150)

    def show_tooltip(self, event, space):
        attrs = "\n".join(f"{k}: {v}" for k, v in space.attributes.items())
        self.tooltip.config(text=f"Space {space.space_id}\n{attrs}")
        self.tooltip.place(x=event.x_root - self.root.winfo_x() + 10, y=event.y_root - self.root.winfo_y() + 10)

    def hide_tooltip(self, event):
        self.tooltip.place_forget()

    def create_main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Parking Lot Rental System", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Rent a Parking Lot", command=self.enter_date).pack(pady=10)
        tk.Button(self.root, text="View My Rentals", command=self.show_user_rentals).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def enter_date(self):
        self.clear_window()
        tk.Label(self.root, text="Rent a Parking Lot", font=("Arial", 16)).pack(pady=10)

        # Start Date & Time
        tk.Label(self.root, text="Start Date:").pack()
        self.start_date_entry = DateEntry(self.root, date_pattern="yyyy-mm-dd")
        self.start_date_entry.pack()

        tk.Label(self.root, text="Start Time (HH:MM):").pack()
        self.start_time_entry = tk.Entry(self.root)
        self.start_time_entry.insert(0, "10:00")
        self.start_time_entry.pack()

        # End Date & Time
        tk.Label(self.root, text="End Date:").pack()
        self.end_date_entry = DateEntry(self.root, date_pattern="yyyy-mm-dd")
        self.end_date_entry.pack()

        tk.Label(self.root, text="End Time (HH:MM):").pack()
        self.end_time_entry = tk.Entry(self.root)
        self.end_time_entry.insert(0, "12:00")
        self.end_time_entry.pack()

        # Submit button
        tk.Button(self.root, text="Submit", command=self.draw_map).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)

    def rent_space(self, parking_space):
        self.clear_window()
        tk.Label(self.root, text="Rent a Parking Lot", font=("Arial", 16)).pack(pady=10)

        # Car Plate
        tk.Label(self.root, text="Vehicle Plate:").pack()
        self.vehicle_plate_entry = tk.Entry(self.root)
        self.vehicle_plate_entry.pack()

        # Payment Method
        tk.Label(self.root, text="Payment Method:").pack()
        # For simplicity, we will only accept cash or pix
        self.payment_method_entry = tk.StringVar()
        self.payment_method_entry.set("Cash")
        payment_methods = ["Cash", "Pix"]
        tk.OptionMenu(self.root, self.payment_method_entry, *payment_methods).pack()

        self.parking_space = parking_space

        # Submit button
        tk.Button(self.root, text="Submit", command=self.handle_rent).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)

    def handle_rent(self):
        try:
            vehicle_plate = self.vehicle_plate_entry.get()
            payment_method = self.payment_method_entry.get()
            if not vehicle_plate or not payment_method:
                raise ValueError("Vehicle Plate and Payment Method cannot be empty.")
            if not validate_plate(vehicle_plate):
                raise ValueError("Invalid vehicle plate. Must be in the format ABC1234 or ABC1D23.")
            rental = rent_parking_space(self.parking_space, self.start_time, self.end_time, vehicle_plate, payment_method)
            if rental:
                messagebox.showinfo("Success", f"Rental successful!\n{rental}")
            else:
                messagebox.showerror("Error", "Parking lot not available.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show_user_rentals(self):
        rentals = get_user_rentals()

        self.clear_window()

        tk.Label(self.root, text="Your Rentals", font=("Arial", 14)).pack(pady=10)
        if not rentals:
            tk.Label(self.root, text="No rentals found.").pack()
        else:
            for rental in rentals:
                tk.Label(self.root, text=str(rental)).pack()

        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def run_app():
    root = tk.Tk()
    app = ParkingApp(root)
    root.geometry("500x600")
    root.mainloop()
