from django.shortcuts import render

from ..models import Rental
from ..forms import ParkingSpaceForm

def add_parking_space(request, username):
    if request.method == 'POST':
        form = ParkingSpaceForm(request.POST)
        if form.is_valid():
            form.save()
            return render(
                request,
                'easypark/manager/home.html',
                {'username': username}
            )
    else:
        form = ParkingSpaceForm()
    return render(
        request, 
        'easypark/manager/add-parking-space.html', 
        {'form': form, 'username': username}
    )

def list_rentals(request, username):
    rentals = Rental.objects.all()
    return render(
        request,
        'easypark/manager/rentals.html', 
        {'rentals': rentals, 'username': username}
    )

def manager_home(request, username):
    return render(
        request,
        'easypark/manager/home.html',
        {'username': username}
    )

def confirm_payment(request, rental_id):
    rental = Rental.objects.get(id=rental_id)
    rental.payment_confirmed = True
    rental.save()
    current_manager = request.user
    rentals = Rental.objects.all()
    return render(
        request,
        'easypark/manager/rentals.html',
        {'rentals': rentals, 'username': current_manager.username}
    )

def cancel_rental(request, rental_id):
    rental = Rental.objects.get(id=rental_id)
    rental.delete()
    current_manager = request.user
    rentals = Rental.objects.all()
    return render(
        request,
        'easypark/manager/rentals.html',
        {'rentals': rentals, 'username': current_manager.username}
    )