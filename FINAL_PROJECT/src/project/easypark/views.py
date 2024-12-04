from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.urls import reverse

from .models import User, Manager, ParkingSpace, Vehicle, Rental
from .forms import UserRegistrationForm, ManagerRegistrationForm, \
                   LoginForm, ParkingSpaceForm, VehicleForm, RentalForm

def index(request):
    return render(request, 'easypark/index.html')

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/easypark/')
    else:
        form = UserRegistrationForm()
    return render(request, 'easypark/register_user.html', {'form': form})

def register_manager(request):
    if request.method == 'POST':
        form = ManagerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/easypark/')
    else:
        form = ManagerRegistrationForm()
    return render(request, 'easypark/register_manager.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.filter(username=username, password=password).first()
            if user:
                return HttpResponseRedirect('/easypark/')
    else:
        form = LoginForm()
    return render(request, 'easypark/login.html', {'form': form})

def list_parking_spaces(request):
    parking_spaces = ParkingSpace.objects.all()
    return render(request, 'easypark/list_parking_spaces.html', {'parking_spaces': parking_spaces})

def add_parking_space(request):
    if request.method == 'POST':
        form = ParkingSpaceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/easypark/parking_spaces/')
    else:
        form = ParkingSpaceForm()
    return render(request, 'easypark/add_parking_space.html', {'form': form})

def list_vehicles(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'easypark/list_vehicles.html', {'vehicles': vehicles})

def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/easypark/vehicles/')
    else:
        form = VehicleForm()
    return render(request, 'easypark/add_vehicle.html', {'form': form})

def list_rentals(request):
    rentals = Rental.objects.all()
    return render(request, 'easypark/list_rentals.html', {'rentals': rentals})

def add_rental(request):
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/easypark/rentals/')
    else:
        form = RentalForm()
    return render(request, 'easypark/add_rental.html', {'form': form})

def confirm_payment(request, rental_id):
    rental = Rental.objects.get(id=rental_id)
    rental.payment_confirmed = True
    rental.save()
    return HttpResponseRedirect('/easypark/rentals/')

def finish_rental(request, rental_id):
    rental = Rental.objects.get(id=rental_id)
    rental.finished = True
    rental.save()
    return HttpResponseRedirect('/easypark/rentals/')

def list_user_rentals(request, user_id):
    user = User.objects.get(id=user_id)
    rentals = Rental.objects.filter(user=user)
    return render(request, 'easypark/list_user_rentals.html', {'user': user, 'rentals': rentals})

def list_space_rentals(request, space_id):
    space = ParkingSpace.objects.get(id=space_id)
    rentals = Rental.objects.filter(parking_space=space)
    return render(request, 'easypark/list_space_rentals.html', {'space': space, 'rentals': rentals})

def list_vehicle_rentals(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    rentals = Rental.objects.filter(vehicle=vehicle)
    return render(request, 'easypark/list_vehicle_rentals.html', {'vehicle': vehicle, 'rentals': rentals})

def list_unconfirmed_payments(request):
    rentals = Rental.objects.filter(payment_confirmed=False)
    return render(request, 'easypark/list_unconfirmed_payments.html', {'rentals': rentals})

def list_unfinished_rentals(request):
    rentals = Rental.objects.filter(finished=False)
    return render(request, 'easypark/list_unfinished_rentals.html', {'rentals': rentals})

def list_user_vehicles(request, user_id):
    user = User.objects.get(id=user_id)
    vehicles = Vehicle.objects.filter(owner=user)
    return render(request, 'easypark/list_user_vehicles.html', {'user': user, 'vehicles': vehicles})
