class ParkingSpace:
    def __init__(self, space_id, x, y, width, height, price_per_hour, attributes):
        self.space_id = space_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.price_per_hour = price_per_hour
        self.attributes = attributes # Dictionary of attributes
        self.reservations = []

    def __str__(self):
        return f"Parking Lot {self.lot_id} at {self.location}, ${self.price_per_hour}/hr ({len(self.reservations)} reservations)"