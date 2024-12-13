from django.db import models
from math import ceil

class ParkingSpace(models.Model):
    class ParkingSpaceSize(models.TextChoices):
        SMALL = 'S', 'Small'
        MEDIUM = 'M', 'Medium'
        LARGE = 'L', 'Large'

    size = models.CharField(max_length=1, choices=ParkingSpaceSize.choices, default=ParkingSpaceSize.MEDIUM)
    position = models.CharField(max_length=4, unique=True) # A001, ..., Z999
    price = models.DecimalField('price per hour', max_digits=6, decimal_places=2)
    electric_charging = models.BooleanField('electric charging', default=False)
    handicapped = models.BooleanField(default=False)
    covered = models.BooleanField(default=False)

    def __str__(self):
        return self.position

class User(models.Model):
    name = models.CharField('full name', max_length=200)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField('phone number', max_length=15, blank=True)

    def __str__(self):
        return self.name

class Manager(User):
    manager_code = models.CharField('manager code', max_length=6, unique=True) # 123456

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    license_plate = models.CharField('licence plate', max_length=7, unique=True) # ABC1234 or ABC1D23
    model = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.license_plate

class Rental(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = 'CASH', 'Cash'
        PIX = 'PIX', 'Pix'

    parking_space = models.ForeignKey(ParkingSpace, on_delete=models.SET_NULL, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    entry_time = models.DateTimeField('entry time')
    exit_time = models.DateTimeField('exit time')
    total_price = models.DecimalField('total price', max_digits=8, decimal_places=2, default=0.0)
    payment_method = models.CharField(max_length=4, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    payment_confirmed = models.BooleanField('payment confirmed', default=False)
    canceled = models.BooleanField(default=False)

    def calculate_total_price(self):
        if self.entry_time and self.exit_time and self.parking_space:
            duration = self.exit_time - self.entry_time
            hours = ceil(duration.total_seconds() / 3600)
            return round(hours * self.parking_space.price, 2)
        return 0.0
    
    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        vehicle = self.vehicle.license_plate if self.vehicle else 'Deleted'
        parking_space = self.parking_space.position if self.parking_space else 'Deleted'
        return f'{parking_space} - {self.entry_time} - {self.exit_time} - {vehicle}'


