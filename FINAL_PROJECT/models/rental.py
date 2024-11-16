from datetime import datetime
from enum import Enum

class PaymentMethod(Enum):
    CASH = "cash"
    PIX = "pix"

class Rental:
    def __init__(self, user, parking_lot, start_date: datetime, end_date: datetime, 
                 vehicle_plate, payment_method: PaymentMethod):
        self.user = user
        self.parking_lot = parking_lot
        self.start_date = start_date
        self.end_date = end_date
        self.hours = (end_date - start_date).seconds / 3600
        self.total_cost = parking_lot.price_per_hour * self.hours
        self.vehicle_plate = vehicle_plate
        self.payment_method = payment_method

    def __str__(self):
        return (f"Rental for {self.user}:\n"
                f"  - Vehicle Plate: {self.vehicle_plate}\n"
                f"  - Lot: {self.parking_lot.location}\n"
                f"  - Start Date: {self.start_date}\n"
                f"  - End Date: {self.end_date}\n"
                f"  - Total Cost: ${self.total_cost}"
                f"  - Payment Method: {self.payment_method}")
    
