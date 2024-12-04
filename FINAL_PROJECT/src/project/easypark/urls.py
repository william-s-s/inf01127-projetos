from django.urls import path

from . import views

app_name = 'easypark'

urlpatterns = [
    path('', views.index, name='index'),
    path('register_user/', views.register_user, name='register_user'),
    path('register_manager/', views.register_manager, name='register_manager'),
    path('login/', views.login, name='login'),
    path('parking_spaces/', views.list_parking_spaces, name='list_parking_spaces'),
    path('add_parking_space/', views.add_parking_space, name='add_parking_space'),
    path('vehicles/', views.list_vehicles, name='list_vehicles'),
    path('add_vehicle/', views.add_vehicle, name='add_vehicle'),
    path('rentals/', views.list_rentals, name='list_rentals'),
    path('add_rental/', views.add_rental, name='add_rental'),
    path('rental/<int:rental_id>/confirm_payment/', views.confirm_payment, name='confirm_payment'),
    path('rental/<int:rental_id>/finish_rental/', views.finish_rental, name='finish_rental')    
]