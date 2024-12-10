from django.urls import path

from . import views

app_name = 'easypark'

urlpatterns = [
    path('', views.index, name='index'),
    path('register_user/', views.register_user, name='register_user'),
    path('register_manager/', views.register_manager, name='register_manager'),
    path('user_login/', views.user_login, name='user_login'),
    path('manager_login/', views.manager_login, name='manager_login'),
    path('parking_spaces/', views.list_parking_spaces, name='parking_spaces'),
    path('manager/add_parking_space/<int:manager_id>/', views.add_parking_space, name='add_parking_space'),
    path('manager/rentals/<int:manager_id>/', views.list_rentals, name='rentals'),
    path('user/user_home/<int:user_id>/', views.user_home, name='user_home'),
    path('user/user_vehicles/<int:user_id>/', views.list_user_vehicles, name='user_vehicles'),
    path('user/add_vehicle/<int:user_id>/', views.add_vehicle, name='add_vehicle'),
    path('user/user_rentals/<int:user_id>/', views.list_user_rentals, name='user_rentals'),
    path('user/add_rental/<int:user_id>/', views.add_rental, name='add_rental'),
    path('manager/manager_home/<int:manager_id>/', views.manager_home, name='manager_home')  
]