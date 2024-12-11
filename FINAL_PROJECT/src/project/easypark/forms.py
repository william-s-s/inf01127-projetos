from django import forms
from .models import User, Manager, ParkingSpace, Vehicle, Rental
import re

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

    def _check_license_plate(self, license_plate):
        return bool(re.match(r'^[A-Z]{3}\d{4}$', license_plate))

    def is_valid(self):
        license_plate = self.data['license_plate']
        if not self._check_license_plate(license_plate):
            self.add_error('license_plate', 'Invalid license plate')
            return False
        model = self.data['model']
        if not model.isascii():
            self.add_error('model', 'Model must be ASCII')
            return False
        color = self.data['color']
        if not color.isascii():
            self.add_error('color', 'Color must be ASCII')
            return False
        return True
    
    def save(self, owner, commit=True):
        vehicle = super().save(commit=False)
        vehicle.owner = owner
        vehicle.license_plate = vehicle.license_plate.upper()
        if commit:
            vehicle.save()
        return vehicle

class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['parking_space', 'vehicle', 'entry_time', 'exit_time', 'payment_method']
        widgets = {
            'entry_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'exit_time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def is_valid(self):
        entry_time = self.data['entry_time']
        exit_time = self.data['exit_time']

        if entry_time and exit_time and entry_time >= exit_time:
            self.add_error(None, 'Entry time must be before exit time')
            return False
        return super().is_valid()




    

