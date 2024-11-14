from models.parking_lot import ParkingLot

# Simulated in-memory storage
parking_lots = {
    1: ParkingLot(1, "Downtown", 10),
    2: ParkingLot(2, "Airport", 15),
    3: ParkingLot(3, "Mall", 8),
}

rentals = []
test_user = "test_user"