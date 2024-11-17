from data.storage import parking_spaces, rentals, test_user
from models.rental import Rental, PaymentMethod

def is_space_available(parking_space, start_time, end_time):
    for reservation in parking_space.reservations:
        if start_time >= reservation[0] and start_time <= reservation[1] or \
           end_time >= reservation[0] and end_time <= reservation[1]:
            return False
    return True

def list_available_spaces(start_time, end_time):
    available_spaces = []
    for space in parking_spaces.values():
        if is_space_available(space, start_time, end_time):
            available_spaces.append(space)
    return available_spaces

def rent_parking_space(parking_space, start_time, end_time, vehicle_plate, payment_method):
    if not is_space_available(parking_space, start_time, end_time):
        return None

    parking_space.reservations.append((start_time, end_time))
    
    rental = Rental(
        user=test_user,
        parking_space=parking_space,
        start_time=start_time,
        end_time=end_time,
        vehicle_plate=vehicle_plate,
        payment_method=payment_method
    )
    rentals.append(rental)
    return rental

def get_user_rentals():
    return rentals

# The plate must have one of the following formats: ABC1234 or ABC1D23
def validate_plate(vehicle_plate):
    if len(vehicle_plate) != 7:
        return False
    if not vehicle_plate[:3].isalpha():
        return False
    if not vehicle_plate[3].isdigit():
        return False
    if not vehicle_plate[4].isalnum():
        return False
    if not vehicle_plate[5:7].isdigit():
        return False
    return True