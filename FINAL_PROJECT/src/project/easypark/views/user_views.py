from django.shortcuts import render

from ..models import User, Vehicle, Rental, ParkingSpace
from ..forms import VehicleForm, RentalForm, RentalTimeForm

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

def enter_rental_time(request, username):
    if request.method == 'POST':
        form = RentalTimeForm(request.POST)
        if form.is_valid():
            entry_time = form.cleaned_data['entry_time']
            exit_time = form.cleaned_data['exit_time']
            spaces = ParkingSpace.get_available_spaces(entry_time, exit_time)
            return render(
                request, 
                'easypark/user/rentals/available-spaces.html', 
                {'entry_time': entry_time, 'exit_time': exit_time, 'parking_spaces': spaces, 'username': username}
            )
    else:
        form = RentalTimeForm()
    return render(
        request, 
        'easypark/user/rentals/enter-rental-time.html', 
        {'form': form, 'username': username}
    )

def available_spaces(request, username, entry_time, exit_time):
    spaces = ParkingSpace.get_available_spaces(entry_time, exit_time)
    return render(
        request, 
        'easypark/user/rentals/available-spaces.html', 
        {'entry_time': entry_time, 'exit_time': exit_time, 'parking_spaces': spaces, 'username': username}
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