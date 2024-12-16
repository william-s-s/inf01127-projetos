from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from ..models import User, Manager, ParkingSpace
from ..forms import UserRegistrationForm, ManagerRegistrationForm, LoginForm

def index(request):
    return render(request, 'easypark/index.html')

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            form.save()
            return HttpResponseRedirect('/easypark/')
    else:
        form = UserRegistrationForm()
    return render(
        request, 
        'easypark/register-user.html', 
        {'form': form}
    )

def register_manager(request):
    if request.method == 'POST':
        form = ManagerRegistrationForm(request.POST)
        if form.is_valid():
            manager = form.save(commit=False)
            manager.password = make_password(form.cleaned_data['password'])
            form.save()
            return HttpResponseRedirect('/easypark/')
    else:
        form = ManagerRegistrationForm()
    return render(
        request, 
        'easypark/register-manager.html', 
        {'form': form}
    )
def login(request):
    if request.method == 'POST':
        
        user_type = request.POST.get('user_type')  # Get user_type from the form
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            if user_type == 'user':
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    form.add_error('username', 'Invalid username')
                    return render(request, 'easypark/login.html', {'form': form})
                
                if not user.check_password(password):
                    form.add_error('password', 'Invalid password')
                    return render(request, 'easypark/login.html', {'form': form})

                return HttpResponseRedirect(reverse('easypark:user-home', args=(user.username,)))

            elif user_type == 'manager':
                try:
                    manager = Manager.objects.get(username=username)
                except Manager.DoesNotExist:
                    form.add_error('username', 'Invalid username')
                    return render(request, 'easypark/login.html', {'form': form})

                if not manager.check_password(password):
                    form.add_error('password', 'Invalid password')
                    return render(request, 'easypark/login.html', {'form': form})

                return HttpResponseRedirect(reverse('easypark:manager-home', args=(manager.username,)))
    else:
        form = LoginForm()

    return render(request, 'easypark/login.html', {'form': form})
""""
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.get(username=username)

            if not user:
                form.add_error('username', 'Invalid username')
                return render(
                    request, 
                    'easypark/login-user.html', 
                    {'form': form}
                )

            try:
                validate_password(password, user.password)
            except:
                form.add_error('password', 'Invalid password')
                return render(
                    request, 
                    'easypark/login-user.html', 
                    {'form': form}
                )
            
            return HttpResponseRedirect(
                reverse('easypark:user-home', args=(user.username,))
            )
    else:
        form = LoginForm()
    return render(
        request, 
        'easypark/login-user.html', 
        {'form': form}
    )

def login_manager(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            manager = Manager.objects.get(username=username)

            if not manager:
                form.add_error('username', 'Invalid username')
                return render(
                    request, 
                    'easypark/login-manager.html', 
                    {'form': form}
                )
            
            try:
                validate_password(password, manager.password)
            except:
                form.add_error('password', 'Invalid password')
                return render(
                    request, 
                    'easypark/login-manager.html', 
                    {'form': form}
                )
            
            return HttpResponseRedirect(
                reverse('easypark:manager-home', args=(manager.username,))
            )
    else:
        form = LoginForm()
    return render(
        request, 
        'easypark/login-manager.html', 
        {'form': form}
    )
"""    