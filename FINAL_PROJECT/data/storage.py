from models.parking_lot import ParkingLot

# Simulated in-memory storage
parking_lots = {
    1: ParkingLot(1, "Downtown", 10),
    2: ParkingLot(2, "Airport", 15),
    3: ParkingLot(3, "Mall", 8),
    4: ParkingLot(4, "Stadium", 12),
    5: ParkingLot(5, "Beach", 5),
    6: ParkingLot(6, "Park", 3),
    7: ParkingLot(7, "Hospital", 7),
    8: ParkingLot(8, "University", 6),
    9: ParkingLot(9, "Train Station", 9),
    10: ParkingLot(10, "Bus Station", 9),
    11: ParkingLot(11, "Zoo", 4),
    12: ParkingLot(12, "Library", 5),
    13: ParkingLot(13, "Museum", 6),
    14: ParkingLot(14, "Restaurant", 7),
    15: ParkingLot(15, "Cinema", 8),
    16: ParkingLot(16, "Theater", 9),
    17: ParkingLot(17, "Concert Hall", 10),
    18: ParkingLot(18, "Bar", 11),
    19: ParkingLot(19, "Nightclub", 12),
    20: ParkingLot(20, "Hotel", 13)
}

rentals = []
test_user = "test_user"