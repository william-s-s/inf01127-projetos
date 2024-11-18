from models.vehicle import Vehicle
from data.storage import vehicles

def register_vehicle(plate, color, model):
    # Check if the vehicle is already registered
    if any(vehicle.plate == plate for vehicle in vehicles):
        return False  # Vehicle already registered
    new_vehicle = Vehicle(plate, color, model)
    vehicles.append(new_vehicle)
    return True

def find_vehicle_by_plate(plate):
    for vehicle in vehicles:
        if vehicle.plate == plate:
            return vehicle
    return None
