from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from ..models import User, Vehicle, Rental, ParkingSpace
from ..forms import VehicleForm, RentalForm, RentalTimeForm
from ..utils.converters import DateConverter

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

def add_rental(request, username, entry_time, exit_time, position):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        form = RentalForm(
            request.POST, 
            entry_time=entry_time, 
            exit_time=exit_time, 
            position=position,
            user=user
        )
        if form.is_valid():
            form.save()
            vehicles = Vehicle.objects.filter(owner=user)
            rentals = Rental.objects.filter(vehicle__in=vehicles)
            return render(
                request, 
                'easypark/user/rentals.html', 
                {'rentals': rentals, 'username': username}
            )
    else:
        form = RentalForm(
            entry_time=entry_time, 
            exit_time=exit_time, 
            position=position,
            user=user
        )
    return render(
        request, 
        'easypark/user/rentals/add-rental.html', 
        {'form': form, 'username': username, 'entry_time': entry_time, 
         'exit_time': exit_time, 'position': position}
    )

def enter_rental_time(request, username):
    if request.method == 'POST':
        form = RentalTimeForm(request.POST)
        if form.is_valid():
            entry_time = form.cleaned_data['entry_time']
            exit_time = form.cleaned_data['exit_time']
            return HttpResponseRedirect(
                reverse('easypark:available-spaces', args=(username, entry_time, exit_time))
            )
    else:
        form = RentalTimeForm()
    return render(
        request, 
        'easypark/user/rentals/enter-rental-time.html', 
        {'form': form, 'username': username}
    )

def available_spaces(request, username, entry_time, exit_time):
    spaces = ParkingSpace.objects.all()

    for space in spaces:
        space.is_available_flag = space.is_available(entry_time, exit_time)  # Add a flag for the template

    entry_time_url = DateConverter.to_url(entry_time)
    exit_time_url = DateConverter.to_url(exit_time)

    # Group spaces by letter (A, B, C, D)
    grouped_spaces = {}
    for space in spaces:
        letter = space.position[0]  # 'A', 'B', etc.
        if letter not in grouped_spaces:
            grouped_spaces[letter] = []
        grouped_spaces[letter].append(space)

    # Sort spaces numerically within each group
    for letter, spaces in grouped_spaces.items():
        grouped_spaces[letter] = sorted(spaces, key=lambda x: int(x.position[1:]))  # Sort by the numeric part

    template_name = 'easypark/user/rentals/available-spaces.html'
    context = {
        'entry_time': entry_time_url,
        'exit_time': exit_time_url,
        'parking_spaces': grouped_spaces,
        'username': username
    }
    return render(request, template_name, context)

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

def remove_vehicle(request, username, vehicle_id):
    user = User.objects.get(username=username)
    vehicle = Vehicle.objects.get(id=vehicle_id)
    vehicle.delete()
    vehicles = Vehicle.objects.filter(owner=user)
    return render(
        request, 
        'easypark/user/vehicles.html', 
        {'username': username, 'vehicles': vehicles}
    )