from django import forms
from .models import User, Manager, ParkingSpace, Vehicle, Rental

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password', 'address', 'phone']

class ManagerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Manager
        fields = ['name', 'username', 'email', 'password', 'address', 'phone', 'manager_code']

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class ParkingSpaceForm(forms.ModelForm):
    class Meta:
        model = ParkingSpace
        fields = ['size', 'position', 'price', 'electric_charging', 'handicapped', 'covered']

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['license_plate', 'model', 'color', 'owner']

class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['parking_space', 'vehicle', 'entry_time', 'exit_time', 'payment_method']

