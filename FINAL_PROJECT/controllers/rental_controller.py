from data.storage import parking_lots, rentals, test_user
from models.rental import Rental, PaymentMethod

def is_lot_available(lot, start_date, end_date):
    for reservation in lot.reservations:
        if start_date >= reservation[0] and start_date <= reservation[1] or \
           end_date >= reservation[0] and end_date <= reservation[1]:
            return False
    return True

def list_available_parking_lots(start_date, end_date):
    available_lots = []
    for lot in parking_lots.values():
        if is_lot_available(lot, start_date, end_date):
            available_lots.append(lot)
    return available_lots

def rent_parking_lot(lot_id, start_date, end_date, vehicle_plate, 
                     payment_method: PaymentMethod = PaymentMethod.CASH):
    if lot_id not in parking_lots:
        return None
    if not is_lot_available(parking_lots[lot_id], start_date, end_date):
        return None

    parking_lot = parking_lots[lot_id]
    parking_lot.reservations.append((start_date, end_date))

    rental = Rental(
        user=test_user,
        parking_lot=parking_lot,
        start_date=start_date,
        end_date=end_date,
        vehicle_plate=vehicle_plate,
        payment_method=payment_method
    )
    rentals.append(rental)
    return rental

def get_user_rentals():
    return rentals
