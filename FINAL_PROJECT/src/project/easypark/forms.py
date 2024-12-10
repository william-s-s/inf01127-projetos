from django import forms
from .models import User, Manager, ParkingSpace, Vehicle, Rental

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password', 'address', 'phone']
        widgets = {
            'password': forms.PasswordInput
        }

class ManagerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Manager
        fields = ['name', 'username', 'email', 'password', 'address', 'phone', 'manager_code']
        widgets = {
            'password': forms.PasswordInput
        }

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    widgets = {
        'password': forms.PasswordInput
    }

class ParkingSpaceForm(forms.ModelForm):
    class Meta:
        model = ParkingSpace
        fields = ['size', 'position', 'price', 'electric_charging', 'handicapped', 'covered']
        widgets = {
            'position': forms.TextInput(attrs={'placeholder': 'A001'}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'electric_charging': forms.CheckboxInput,
            'handicapped': forms.CheckboxInput,
            'covered': forms.CheckboxInput
        }

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['license_plate', 'model', 'color']
        widgets = {
            'license_plate': forms.TextInput(attrs={'placeholder': 'ABC1234'})
        }

class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['parking_space', 'vehicle', 'entry_time', 'exit_time', 'payment_method']
        widgets = {
            'entry_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'exit_time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

