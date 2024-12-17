import re
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

    def is_available(self, entry_time, exit_time):
        rentals = Rental.objects.filter(parking_space=self, canceled=False)
        for rental in rentals:
            if entry_time < rental.exit_time and exit_time > rental.entry_time:
                return False
        return True
    
    @staticmethod
    def get_available_spaces(entry_time, exit_time):
        spaces = ParkingSpace.objects.all()
        available_spaces = []
        for space in spaces:
            if space.is_available(entry_time, exit_time):
                available_spaces.append(space)
        return available_spaces

    def __str__(self):
        size = "Medium" if self.size == 'M' else "Small" if self.size == 'S' else "Large"
        properties = []
        if self.electric_charging:
            properties.append('Electric charging')
        if self.handicapped:
            properties.append('Handicapped')
        if self.covered:
            properties.append('Covered')
        properties = properties if properties else ['None']
        return f'{self.position} | {size} | $ {self.price} | {", ".join(properties)}'

class User(models.Model):
    name = models.CharField('full name', max_length=200)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField('phone number', max_length=15, blank=True)

    @staticmethod
    def validate_data(data):
        username = data['username']
        password = data['password']
        phone = data['phone']
        return (
            bool(re.match(r'^[a-zA-Z0-9]+([_-]?[a-zA-Z0-9]){3,30}$', username)) and
            bool(re.match(r'(?=(.*[A-Za-z]){1,})(?=(.*[\d]){1,})(?!.*\s).{8,}$', password)) and
            bool(re.match(r'^\d{5,15}$', phone))
        )

    def __str__(self):
        return f'{self.username} | {self.email}'

class Manager(User):
    manager_code = models.CharField('manager code', max_length=6, unique=True) # 123456

    @staticmethod
    def validate_data(data):
        manager_code = data['manager_code']
        return (
            User.validate_data(data) and
            bool(re.match(r'^\d{6}$', manager_code))
        )

    def __str__(self):
        return f'{self.username} | {self.email} | {self.manager_code}'

class Vehicle(models.Model):
    license_plate = models.CharField('licence plate', max_length=7, unique=True) # ABC1234 or ABC1D23
    model = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    @staticmethod
    def validate_data(data):
        license_plate = data['license_plate']
        model = data['model']
        color = data['color']
        return (
            bool(re.match(r'^[A-Za-z]{3}\d{4}$', license_plate)) and
            bool(re.match(r'^[A-Za-z0-9 ]{1,200}$', model)) and
            bool(re.match(r'^[A-Za-z ]{1,200}$', color))
        )

    def __str__(self):
        return f'{self.license_plate} | {self.model} | {self.color}'

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

    @staticmethod
    def validate_data(data):
        entry_time = data['entry_time']
        exit_time = data['exit_time']
        return entry_time < exit_time

    def _calculate_total_price(self):
        if self.entry_time and self.exit_time and self.parking_space:
            duration = self.exit_time - self.entry_time
            hours = ceil(duration.total_seconds() / 3600)
            return round(hours * self.parking_space.price, 2)
        return 0.0
    
    def save(self, *args, **kwargs):
        self.total_price = self._calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        vehicle = self.vehicle.license_plate if self.vehicle else 'Deleted'
        parking_space = self.parking_space.position if self.parking_space else 'Deleted'
        entry_time = self.entry_time.strftime('%Y-%m-%d %H:%M')
        exit_time = self.exit_time.strftime('%Y-%m-%d %H:%M')
        return f'{parking_space} | {entry_time} - {exit_time} | {vehicle}'


