from models.parking_space import ParkingSpace

# Simulated in-memory storage
parking_spaces = {
    1: ParkingSpace(1, 0, 0, 10, 10, 10, {"covered": True, "security": True, "electric": True}),
    2: ParkingSpace(2, 10, 0, 10, 10, 15, {"covered": False, "security": True, "electric": False}),
    3: ParkingSpace(3, 20, 0, 10, 10, 20, {"covered": True, "security": False, "electric": False}),
    4: ParkingSpace(4, 30, 0, 10, 10, 25, {"covered": False, "security": False, "electric": True}),
    5: ParkingSpace(5, 40, 0, 10, 10, 30, {"covered": True, "security": True, "electric": True}),
    6: ParkingSpace(6, 50, 0, 10, 10, 35, {"covered": False, "security": True, "electric": False}),
    7: ParkingSpace(7, 60, 0, 10, 10, 40, {"covered": True, "security": False, "electric": False}),
    8: ParkingSpace(8, 70, 0, 10, 10, 45, {"covered": False, "security": False, "electric": True}),
    9: ParkingSpace(9, 80, 0, 10, 10, 50, {"covered": True, "security": True, "electric": True}),
    10: ParkingSpace(10, 90, 0, 20, 10, 55, {"covered": False, "security": True, "electric": False}),
    11: ParkingSpace(11, 0, 10, 10, 10, 60, {"covered": True, "security": False, "electric": False}),
    12: ParkingSpace(12, 10, 10, 10, 10, 65, {"covered": False, "security": False, "electric": True}),
    13: ParkingSpace(13, 20, 10, 10, 10, 70, {"covered": True, "security": True, "electric": True}),
    14: ParkingSpace(14, 30, 10, 10, 10, 75, {"covered": False, "security": True, "electric": False}),
    15: ParkingSpace(15, 40, 10, 10, 10, 80, {"covered": True, "security": False, "electric": False}),
    16: ParkingSpace(16, 50, 10, 10, 10, 85, {"covered": False, "security": False, "electric": True}),
    17: ParkingSpace(17, 60, 10, 10, 10, 90, {"covered": True, "security": True, "electric": True}),
    18: ParkingSpace(18, 70, 10, 10, 10, 95, {"covered": False, "security": True, "electric": False}),
    19: ParkingSpace(19, 80, 10, 10, 10, 100, {"covered": True, "security": False, "electric": False}),
    20: ParkingSpace(20, 90, 10, 20, 10, 105, {"covered": False, "security": False, "electric": True}),
    21: ParkingSpace(21, 0, 20, 10, 10, 110, {"covered": True, "security": True, "electric": True}),
    22: ParkingSpace(22, 10, 20, 10, 10, 115, {"covered": False, "security": True, "electric": False}),
    23: ParkingSpace(23, 20, 20, 10, 10, 120, {"covered": True, "security": False, "electric": False}),
    24: ParkingSpace(24, 30, 20, 10, 10, 125, {"covered": False, "security": False, "electric": True}),
    25: ParkingSpace(25, 40, 20, 10, 10, 130, {"covered": True, "security": True, "electric": True}),
    26: ParkingSpace(26, 50, 20, 10, 10, 135, {"covered": False, "security": True, "electric": False}),
    27: ParkingSpace(27, 60, 20, 10, 10, 140, {"covered": True, "security": False, "electric": False}),
    28: ParkingSpace(28, 70, 20, 10, 10, 145, {"covered": False, "security": False, "electric": True}),
    29: ParkingSpace(29, 80, 20, 10, 10, 150, {"covered": True, "security": True, "electric": True}),
    30: ParkingSpace(30, 90, 20, 30, 20, 155, {"covered": False, "security": True, "electric": False}),
}

rentals = []
vehicles = []
test_user = "test_user"