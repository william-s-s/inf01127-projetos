import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
from controllers.rental_controller import list_available_parking_lots, rent_parking_lot, get_user_rentals

class ParkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parking Lot Rental System")
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Parking Lot Rental System", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Rent a Parking Lot", command=self.rent_parking_lot).pack(pady=10)
        tk.Button(self.root, text="View My Rentals", command=self.show_user_rentals).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def rent_parking_lot(self):
        self.clear_window()
        tk.Label(self.root, text="Rent a Parking Lot", font=("Arial", 14)).pack(pady=10)

        # Enter Lot ID
        tk.Label(self.root, text="Enter Lot ID:").pack()
        self.lot_id_entry = tk.Entry(self.root)
        self.lot_id_entry.pack()

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

        # Car Plate
        tk.Label(self.root, text="Car Plate:").pack()
        self.car_plate_entry = tk.Entry(self.root)
        self.car_plate_entry.pack()

        # Payment Method
        tk.Label(self.root, text="Payment Method:").pack()
        # For simplicity, we will only accept cash or pix
        # Create a dropdown menu with the options
        self.payment_method_entry = tk.StringVar()
        self.payment_method_entry.set("cash")
        payment_methods = ["cash", "pix"]
        tk.OptionMenu(self.root, self.payment_method_entry, *payment_methods).pack()

        # Submit button
        tk.Button(self.root, text="Submit", command=self.handle_rent).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)

    def handle_rent(self):
        try:
            lot_id = int(self.lot_id_entry.get())
            start_date_str = self.start_date_entry.get() + " " + self.start_time_entry.get()
            end_date_str = self.end_date_entry.get() + " " + self.end_time_entry.get()
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M")
            car_plate = self.car_plate_entry.get()
            payment_method = self.payment_method_entry.get()

            if not car_plate or not payment_method:
                raise ValueError("Car Plate and Payment Method cannot be empty.")

            rental = rent_parking_lot(lot_id, start_date, end_date, car_plate, payment_method)
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
