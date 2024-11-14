class ParkingLot:
    def __init__(self, lot_id, location, price_per_hour):
        self.lot_id = lot_id
        self.location = location
        self.price_per_hour = price_per_hour
        self.is_available = True

    def __str__(self):
        status = "Available" if self.is_available else "Occupied"
        return f"Parking Lot {self.lot_id} at {self.location}, {status}, ${self.price_per_hour}/hr"