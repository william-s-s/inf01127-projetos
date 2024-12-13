from django.shortcuts import render

from ..models import User, Vehicle, Rental, ParkingSpace
from ..forms import VehicleForm, RentalForm

def user_home(request, username):
    return render(
        request, 
        'easypark/user/home.html', 
        {'username': username}
    )

def list_user_vehicles(request, username):
    user = User.objects.get(username=username)
    vehicles = Vehicle.objects.filter(owner=user)
    return render(
        request, 
        'easypark/user/vehicles.html', 
        {'vehicles': vehicles, 'username': username}
    )

def add_vehicle(request, username):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=username)
            form.save(owner=user)
            vehicles = Vehicle.objects.filter(owner=user)
            return render(
                request, 
                'easypark/user/vehicles.html', 
                {'username': username, 'vehicles': vehicles}
            )
    else:
        form = VehicleForm()
    return render(
        request, 
        'easypark/user/vehicles/add-vehicle.html', 
        {'form': form, 'username': username}
    )

def add_rental(request, username, position):
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            form.save(position=position)
            user = User.objects.get(username=username)
            vehicles = Vehicle.objects.filter(owner=user)
            rentals = Rental.objects.filter(vehicle__in=vehicles)
            return render(
                request, 
                'easypark/user/rentals.html', 
                {'rentals': rentals, 'username': username}
            )
    else:
        form = RentalForm()
    return render(
        request, 
        'easypark/user/rentals/add-rental.html', 
        {'form': form, 'username': username}
    )

def list_user_rentals(request, username):
    user = User.objects.get(username=username)
    vehicles = Vehicle.objects.filter(owner=user)
    rentals = Rental.objects.filter(vehicle__in=vehicles)
    return render(
        request,
        'easypark/user/rentals.html',
        {'rentals': rentals, 'username': username}
    )

def list_parking_spaces(request, username):
    parking_spaces = ParkingSpace.objects.all()
    return render(
        request, 
        'easypark/user/parking-spaces.html', 
        {'username': username, 'parking_spaces': parking_spaces}
    )