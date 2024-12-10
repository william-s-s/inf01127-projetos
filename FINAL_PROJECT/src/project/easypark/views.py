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

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.filter(username=username, password=password).first()
            if user:
                return HttpResponseRedirect(reverse('easypark:user_home', args=(user.id,)))
    else:
        form = LoginForm()
    return render(request, 'easypark/user_login.html', {'form': form})

def manager_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            manager = Manager.objects.filter(username=username, password=password).first()
            if manager:
                return HttpResponseRedirect(reverse('easypark:manager_home', args=(manager.id,)))
    else:
        form = LoginForm()
    return render(request, 'easypark/manager_login.html', {'form': form})

def list_parking_spaces(request):
    parking_spaces = ParkingSpace.objects.all()
    return render(request, 'easypark/parking_spaces.html', {'parking_spaces': parking_spaces})

def add_parking_space(request, manager_id):
    if request.method == 'POST':
        form = ParkingSpaceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('easypark:manager/manage_parking_spaces', args=(manager_id,)))
    else:
        form = ParkingSpaceForm()
    return render(request, 'easypark/manager/add_parking_space.html', {'form': form})

def manage_parking_spaces(request, manager_id):
    parking_spaces = ParkingSpace.objects.filter(manager=manager_id)
    return render(request, 'easypark/manager/manage_parking_spaces.html', {'parking_spaces': parking_spaces, 'manager_id': manager_id})

def list_user_vehicles(request, user_id):
    vehicles = Vehicle.objects.filter(owner=user_id)
    return render(request, 'easypark/user/user_vehicles.html', {'vehicles': vehicles, 'user_id': user_id})

def add_vehicle(request, user_id):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        form.instance.owner = User.objects.get(id=user_id)
        if form.is_valid():
            form.save()
            # List user vehicles
            vehicles = Vehicle.objects.filter(owner=user_id)
            return HttpResponseRedirect(reverse('easypark/user/user_vehicles:user', args=(user_id,)))
    else:
        form = VehicleForm()
    return render(request, 'easypark/user/add_vehicle.html', {'form': form, 'user_id': user_id})

def list_rentals(request, manager_id):
    rentals = Rental.objects.all()
    return render(request, 'easypark/rentals.html', {'rentals': rentals, 'manager_id': manager_id})

def list_user_rentals(request, user_id):
    vehicles = Vehicle.objects.filter(owner=user_id)
    rentals = Rental.objects.filter(vehicle__in=vehicles)
    return render(request, 'easypark/user/user_rentals.html', {'rentals': rentals, 'user_id': user_id})

def add_rental(request, user_id):
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            form.save()
            # List user rentals
            rentals = Rental.objects.filter(user=user_id)
            return render(request, 'easypark/user/user_rentals.html', {'rentals': rentals, 'user_id': user_id})
    else:
        form = RentalForm()
    return render(request, 'easypark/user/add_rental.html', {'form': form, 'user_id': user_id})

def user_home(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'easypark/user/user_home.html', {'user': user})

def manager_home(request, manager_id):
    manager = Manager.objects.get(id=manager_id)
    return render(request, 'easypark/manager/manager_home.html', {'manager': manager})

"""
def confirm_payment(request, rental_id):
    rental = Rental.objects.get(id=rental_id)
    rental.payment_confirmed = True
    rental.save()
    return HttpResponseRedirect('/easypark/manager/rentals/')

def finish_rental(request, rental_id):
    rental = Rental.objects.get(id=rental_id)
    rental.finished = True
    rental.save()
    return HttpResponseRedirect('/easypark/manager/rentals/')

def list_unconfirmed_payments(request):
    rentals = Rental.objects.filter(payment_confirmed=False)
    return render(request, 'easypark/list_unconfirmed_payments.html', {'rentals': rentals})

def list_unfinished_rentals(request):
    rentals = Rental.objects.filter(finished=False)
    return render(request, 'easypark/list_unfinished_rentals.html', {'rentals': rentals})
"""