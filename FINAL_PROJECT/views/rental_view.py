import tkinter as tk
from tkinter import messagebox, scrolledtext, Scrollbar
from tkcalendar import DateEntry
from datetime import datetime
from controllers.rental_controller import list_available_parking_lots, rent_parking_lot, get_user_rentals

class ParkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EasyPark")
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Parking Lot Rental System", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Rent a Parking Lot", command=self.enter_date).pack(pady=10)
        tk.Button(self.root, text="View My Rentals", command=self.show_user_rentals).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def list_available_lots(self):
        # Get the start and end dates from the entries
        start_date_str = self.start_date_entry.get() + " " + self.start_time_entry.get()
        end_date_str = self.end_date_entry.get() + " " + self.end_time_entry.get()
        self.start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M")
        self.end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M")

        # Call the controller to get the available lots
        available_lots = list_available_parking_lots(self.start_date, self.end_date)

        self.clear_window()

        tk.Label(self.root, text="Available Parking Lots", font=("Arial", 16)).pack(pady=10)

        if not available_lots:
            tk.Label(self.root, text="No parking lots available.").pack()

        else:
            # Create a scrolled text widget to show the available lots
            st = scrolledtext.ScrolledText(self.root, width=self.root.winfo_width(), height=self.root.winfo_height(),
                                           cursor="arrow", relief="sunken")
            st.pack(pady=10)
            st.configure(state='normal', font=("Arial", 11), background="lightgrey")
            
            for lot in available_lots:
                st.insert(tk.END, "\n")
                st.insert(tk.END, f"{lot.location} - ${lot.price_per_hour}/hr\n", f"button-{lot.lot_id}")
                st.tag_configure(f"button-{lot.lot_id}", foreground="black", justify="center", borderwidth=1, 
                                 relief="raised", background="lightgray", spacing1=5, spacing2=5, spacing3=5)
                st.tag_bind(f"button-{lot.lot_id}", "<Button-1>", lambda event, lot_id=lot.lot_id: self.rent_lot(lot_id))
            
            st.insert(tk.END, "\n\n")
            st.insert(tk.END, "   Back   ", "buttonback")                
            st.tag_configure("buttonback", foreground="black", justify="left", borderwidth=1, 
                             relief="raised", background="lightgray", spacing1=5, spacing2=5, spacing3=5)
            st.tag_bind("buttonback", "<Button-1>", lambda event: self.create_main_menu())

            st.configure(state='disabled')

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
        tk.Button(self.root, text="Submit", command=self.list_available_lots).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)

    def rent_lot(self, lot_id):
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
        self.payment_method_entry.set("cash")
        payment_methods = ["cash", "pix"]
        tk.OptionMenu(self.root, self.payment_method_entry, *payment_methods).pack()

        self.lot_id = lot_id

        # Submit button
        tk.Button(self.root, text="Submit", command=self.handle_rent).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)

    def handle_rent(self):
        try:
            vehicle_plate = self.vehicle_plate_entry.get()
            payment_method = self.payment_method_entry.get()
            if not vehicle_plate or not payment_method:
                raise ValueError("Vehicle Plate and Payment Method cannot be empty.")
            rental = rent_parking_lot(self.lot_id, self.start_date, self.end_date, vehicle_plate, payment_method)
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
