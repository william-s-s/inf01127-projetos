from django import forms
from .models import User, Manager, ParkingSpace, Vehicle, Rental

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password', 'address', 'phone']
        widgets = {
            'password': forms.PasswordInput
        }
    
    def is_valid(self):
        if not User.validate_data(self.data):
            return False
        return super().is_valid()

class ManagerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Manager
        fields = ['name', 'username', 'email', 'password', 'address', 'phone', 'manager_code']
        widgets = {
            'password': forms.PasswordInput
        }

    def is_valid(self):
        if not Manager.validate_data(self.data):
            return False
        
        return super().is_valid()

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

    def is_valid(self):
        if not Vehicle.validate_data(self.data):
            return False
        return super().is_valid()
    
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
        fields = ['vehicle', 'payment_method']
        ignore = ['entry_time', 'exit_time', 'position']

    def __init__(self, *args, **kwargs):
        self.temp_data = {
            'entry_time': kwargs.pop('entry_time'),
            'exit_time': kwargs.pop('exit_time'),
            'position': kwargs.pop('position')
        }
        super().__init__(*args, **kwargs)

    def is_valid(self):
        data = self.data.copy()
        data.update(self.temp_data)
        if not Rental.validate_data(data):
            return False
        return super().is_valid()
    
    def save(self, commit=True):
        rental = super().save(commit=False)
        rental.entry_time = self.temp_data['entry_time']
        rental.exit_time = self.temp_data['exit_time']
        rental.parking_space = ParkingSpace.objects.get(position=self.temp_data['position'])
        if commit:
            rental.save()
        return rental

class RentalTimeForm(forms.Form):
    entry_time = forms.DateTimeField(label='Entry time', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    exit_time = forms.DateTimeField(label='Exit time', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    widgets = {
        'entry_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        'exit_time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
    }