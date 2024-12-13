from django.contrib import admin

from .models import User, Manager, ParkingSpace, Vehicle, Rental

admin.site.register(User)
admin.site.register(Manager)
admin.site.register(ParkingSpace)
admin.site.register(Vehicle)
admin.site.register(Rental)