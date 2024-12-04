import tkinter as tk
from tkinter import messagebox, scrolledtext, Scrollbar, OptionMenu
from tkcalendar import DateEntry
from datetime import datetime
from controllers.rental_controller import *
from controllers.vehicle_controller import *
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
        
        self.canvas = tk.Canvas(self.root, height=500, width=600, bg=self.root.cget("bg"))
        self.canvas.pack()
        
        # Draw the parking lot map
        self.rectangles = {}
        for space in parking_spaces.values():
            free_space = space in available_lots
            color = "#2e7bf0" if free_space else "#cccccc"
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

        self.tooltip = tk.Label(self.root, text="", bg="#93b5c6", relief="solid", bd=1, wraplength=150)

    def show_tooltip(self, event, space):
        attrs = "\n".join(f"{k}: {v}" for k, v in space.attributes.items())
        self.tooltip.config(text=f"Space {space.space_id}\n{attrs}")
        self.tooltip.place(x=event.x_root - self.root.winfo_x() + 10, y=event.y_root - self.root.winfo_y() + 10)

    def hide_tooltip(self, event):
        self.tooltip.place_forget()

    def create_main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Parking Lot Rental System", font=("Arial", 16), background=self.root.cget("bg"), foreground="lightgray").pack(pady=20)
        tk.Button(self.root, text="Rent a Parking Lot", command=self.enter_vehicle).pack(pady=10)
        tk.Button(self.root, text="Register Vehicle", command=self.register_vehicle_menu).pack(pady=10)
        tk.Button(self.root, text="View My Rentals", command=self.show_user_rentals).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def enter_vehicle(self):
        self.clear_window()
        tk.Label(self.root, text="Rent a Parking Lot", font=("Arial", 16), background=self.root.cget("bg"), foreground="lightgray").pack(pady=10)

        # Create a list of vehicles (using a dropdown)
        vehicles = list_vehicles()
        if not vehicles:
            self.clear_window()
            messagebox.showinfo("No vehicles found", "Please register a vehicle first.")
            # Redirect to the main menu
            self.create_main_menu()
            return
        
        vehicle_list = [f"{vehicle.plate} - {vehicle.color} {vehicle.model}" for vehicle in vehicles]
        self.vehicle_entry = tk.StringVar()
        self.vehicle_entry.set(vehicle_list[0])
        vehicle_menu = OptionMenu(self.root, self.vehicle_entry, *vehicle_list)
        vehicle_menu.pack()
        self.vehicle_entry.trace_add("write", self.update_vehicle_plate)
        
        # Submit button
        tk.Button(self.root, text="Submit", command=self.enter_date).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)

    def update_vehicle_plate(self, *args):
        vehicle_str = self.vehicle_entry.get()
        plate = vehicle_str.split(" - ")[0]
        self.vehicle_plate = plate

    def register_vehicle_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Register Vehicle", font=("Arial", 16), background=self.root.cget("bg"), foreground="lightgray").pack(pady=10)

        # Vehicle Plate
        tk.Label(self.root, text="Vehicle Plate:", background=self.root.cget("bg"), foreground="lightgray").pack()
        self.vehicle_plate_entry = tk.Entry(self.root)
        self.vehicle_plate_entry.pack()

        # Vehicle Color
        tk.Label(self.root, text="Vehicle Color:", background=self.root.cget("bg"), foreground="lightgray").pack()
        self.vehicle_color_entry = tk.Entry(self.root)
        self.vehicle_color_entry.pack()

        # Vehicle Model
        tk.Label(self.root, text="Vehicle Model:", background=self.root.cget("bg"), foreground="lightgray").pack()
        self.vehicle_model_entry = tk.Entry(self.root)
        self.vehicle_model_entry.pack()

        # Submit button
        tk.Button(self.root, text="Submit", command=self.handle_vehicle_registration).pack(pady=10)

        # Back button
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)

    def handle_vehicle_registration(self):
        try:
            plate = self.vehicle_plate_entry.get()
            color = self.vehicle_color_entry.get()
            model = self.vehicle_model_entry.get()
            if not plate or not color or not model:
                raise ValueError("Vehicle Plate, Color, and Model cannot be empty.")
            if not validate_plate(plate):
                raise ValueError("Invalid vehicle plate. Must be in the format ABC1234 or ABC1D23.")
            vehicle = find_vehicle_by_plate(plate)
            if vehicle:
                raise ValueError("Vehicle already registered.")
            register_vehicle(plate, color, model)
            messagebox.showinfo("Success", "Vehicle registered successfully.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def enter_date(self):
        self.clear_window()
        tk.Label(self.root, text="Rent a Parking Lot", font=("Arial", 16), background=self.root.cget("bg"), foreground="lightgray").pack(pady=10)

        # Start Date & Time
        tk.Label(self.root, text="Start Date:", background=self.root.cget("bg"), foreground="lightgray").pack()
        self.start_date_entry = DateEntry(self.root, date_pattern="yyyy-mm-dd")
        self.start_date_entry.pack() 

        tk.Label(self.root, text="Start Time (HH:MM):", background=self.root.cget("bg"), foreground="lightgray").pack()
        self.start_time_entry = tk.Entry(self.root)
        self.start_time_entry.insert(0, "10:00")
        self.start_time_entry.pack()

        # End Date & Time
        tk.Label(self.root, text="End Date:", background=self.root.cget("bg"), foreground="lightgray").pack()
        self.end_date_entry = DateEntry(self.root, date_pattern="yyyy-mm-dd")
        self.end_date_entry.pack()

        tk.Label(self.root, text="End Time (HH:MM):", background=self.root.cget("bg"), foreground="lightgray").pack()
        self.end_time_entry = tk.Entry(self.root)
        self.end_time_entry.insert(0, "12:00")
        self.end_time_entry.pack()

        # Submit button
        tk.Button(self.root, text="Submit", command=self.draw_map).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)

    def rent_space(self, parking_space):
        self.clear_window()
        tk.Label(self.root, text="Rent a Parking Lot", font=("Arial", 16), background=self.root.cget("bg"), foreground="lightgray").pack(pady=10)

        # Payment Method
        tk.Label(self.root, text="Payment Method:", background=self.root.cget("bg"), foreground="lightgray").pack()
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
            payment_method = self.payment_method_entry.get()

            if not payment_method:
                raise ValueError("Payment Method cannot be empty.")
                
            rental = rent_parking_space(self.parking_space, self.start_time, self.end_time, self.vehicle_plate, payment_method)
            if rental:
                messagebox.showinfo("Success", f"Rental successful!\n{rental}")
            else:
                messagebox.showerror("Error", "Parking lot not available.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show_user_rentals(self):
        rentals = get_user_rentals()

        self.clear_window()

        tk.Label(self.root, text="Your Rentals", font=("Arial", 14), background=self.root.cget("bg"), foreground="lightgray").pack(pady=10)
        if not rentals:
            tk.Label(self.root, text="No rentals found.", background=self.root.cget("bg"), foreground="lightgray").pack()
        else:
            for rental in rentals:
                tk.Label(self.root, text=str(rental), background=self.root.cget("bg"), foreground="lightgray").pack()

        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def run_app():
    root = tk.Tk()
    root.geometry("500x600")
    root.configure(background="#282828")
    app = ParkingApp(root)
    root.mainloop()
