from django.shortcuts import render

from ..models import Rental, ParkingSpace
from ..forms import ParkingSpaceForm

def add_parking_space(request, username):
    if request.method == 'POST':
        form = ParkingSpaceForm(request.POST)
        if form.is_valid():
            form.save()
            parking_spaces = ParkingSpace.objects.all()
            return render(
                request,
                'easypark/manager/parking-spaces.html',
                {'username': username, 'parking_spaces': parking_spaces}
            )
    else:
        form = ParkingSpaceForm()
    return render(
        request, 
        'easypark/manager/parking-spaces/add-space.html', 
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

def confirm_payment(request, username, rental_id):
    rental = Rental.objects.get(id=rental_id)
    rental.payment_confirmed = True
    rental.save()
    rentals = Rental.objects.all()
    return render(
        request,
        'easypark/manager/rentals.html',
        {'rentals': rentals, 'username': username}
    )

def cancel_rental(request, username, rental_id):
    rental = Rental.objects.get(id=rental_id)
    rental.canceled = True
    rental.save()
    rentals = Rental.objects.all()
    return render(
        request,
        'easypark/manager/rentals.html',
        {'rentals': rentals, 'username': username}
    )

def list_parking_spaces(request, username):
    parking_spaces = ParkingSpace.objects.all()
    return render(
        request, 
        'easypark/manager/parking-spaces.html', 
        {'username': username, 'parking_spaces': parking_spaces}
    )

def edit_parking_space(request, username, position):
    parking_space = ParkingSpace.objects.get(position=position)
    if request.method == 'POST':
        form = ParkingSpaceForm(request.POST, instance=parking_space)
        if form.is_valid():
            form.save()
            parking_spaces = ParkingSpace.objects.all()
            return render(
                request,
                'easypark/manager/parking-spaces.html',
                {'username': username, 'parking_spaces': parking_spaces}
            )
    else:
        form = ParkingSpaceForm(instance=parking_space)
    return render(
        request, 
        'easypark/manager/parking-spaces/edit-space.html', 
        {'form': form, 'username': username, 'position': position}
    )