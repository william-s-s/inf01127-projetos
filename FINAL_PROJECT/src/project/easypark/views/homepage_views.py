from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from ..models import User, Manager
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

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                manager = Manager.objects.get(username=username)
                if manager:
                    form.add_error('username', 'Invalid username')
                    return render(
                        request, 
                        'easypark/index.html',
                        {'form': form}
                    )
            except:
                try:
                        user = User.objects.get(username=username)
                except:
                    form.add_error('username', 'Invalid username')
                    return render(
                        request, 
                        'easypark/index.html',
                        {'form': form}
                    )

                try:
                    validate_password(password, user.password)
                except:
                    form.add_error('password', 'Invalid password')
                    return render(
                        request, 
                        'easypark/index.html',
                        {'form': form}
                    )
                
                return HttpResponseRedirect(
                    reverse('easypark:user-home', args=(user.username,))
                )
    else:
        form = LoginForm()
    return render(
        request, 
        'easypark/index.html', 
        {'form': form}
    )

def login_manager(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                manager = Manager.objects.get(username=username)
            except:
                form.add_error('username', 'Invalid username')
                return render(
                    request, 
                    'easypark/index.html', 
                    {'form': form}
                )
            
            try:
                validate_password(password, manager.password)
            except:
                form.add_error('password', 'Invalid password')
                return render(
                    request, 
                    'easypark/index.html',
                    {'form': form}
                )
            
            return HttpResponseRedirect(
                reverse('easypark:manager-home', args=(manager.username,))
            )
    else:
        form = LoginForm()
    return render(
        request, 
        'easypark/index.html',
        {'form': form}
    )