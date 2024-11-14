from data.storage import parking_lots, rentals, test_user
from models.rental import Rental, PaymentMethod

def list_available_parking_lots():
    return [lot for lot in parking_lots.values() if lot.is_available]

def rent_parking_lot(lot_id, start_date, end_date, car_plate, 
                     payment_method: PaymentMethod = PaymentMethod.CASH):
    if lot_id not in parking_lots or not parking_lots[lot_id].is_available:
        return None
    
    parking_lot = parking_lots[lot_id]
    parking_lot.is_available = False
    rental = Rental(
        user=test_user,
        parking_lot=parking_lot,
        start_date=start_date,
        end_date=end_date,
        car_plate=car_plate,
        payment_method=payment_method
    )
    rentals.append(rental)
    return rental

def get_user_rentals():
    return rentals
