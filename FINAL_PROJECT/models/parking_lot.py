class ParkingLot:
    def __init__(self, lot_id, location, price_per_hour):
        self.lot_id = lot_id
        self.location = location
        self.price_per_hour = price_per_hour
        self.reservations = []

    def __str__(self):
        return f"Parking Lot {self.lot_id} at {self.location}, ${self.price_per_hour}/hr ({len(self.reservations)} reservations)"