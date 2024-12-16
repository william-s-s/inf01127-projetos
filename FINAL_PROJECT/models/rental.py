from datetime import datetime
from enum import Enum

class PaymentMethod(Enum):
    CASH = "Cash"
    PIX = "Pix"

class Rental:
    def __init__(self, user, parking_space, start_time: datetime, end_time: datetime, 
                 vehicle_plate, payment_method: PaymentMethod):
        self.user = user
        self.space_id = parking_space.space_id
        self.start_time = start_time
        self.end_time = end_time
        self.hours = (end_time - start_time).seconds / 3600
        self.total_cost = parking_space.price_per_hour * self.hours
        self.vehicle_plate = vehicle_plate
        self.payment_method = payment_method

    def __str__(self):
        return (f"Rental for {self.user}:\n"
                f"  - Parking Space: {self.space_id}\n"
                f"  - Vehicle Plate: {self.vehicle_plate}\n"
                f"  - Start Time: {self.start_time}\n"
                f"  - End Time: {self.end_time}\n"
                f"  - Total Cost: ${self.total_cost}"
                f"  - Payment Method: {self.payment_method}")
    
