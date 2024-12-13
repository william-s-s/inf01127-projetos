from django.urls import path

from .views import homepage_views, user_views, manager_views

app_name = 'easypark'

urlpatterns = [
    path('', homepage_views.index, name='index'),
    path('register-user/', homepage_views.register_user, name='register-user'),
    path('register-manager/', homepage_views.register_manager, name='register-manager'),
    path('login-user/', homepage_views.login_user, name='login-user'),
    path('login-manager/', homepage_views.login_manager, name='login-manager'),
    path('parking-spaces/', homepage_views.list_parking_spaces, name='list-parking-spaces'),
    path('user/home/<str:username>/', user_views.user_home, name='user-home'),
    path('user/vehicles/<str:username>/', user_views.list_user_vehicles, name='user-vehicles'),
    path('user/vehicles/add-vehicle/<str:username>/', user_views.add_vehicle, name='add-vehicle'),
    path('user/rentals/<str:username>/', user_views.list_user_rentals, name='user-rentals'),
    path('user/rentals/add-rental/<str:username>/', user_views.add_rental, name='add-rental'),
    path('manager/home/<str:username>/', manager_views.manager_home, name='manager-home'),
    path('manager/add-parking-space/<str:username>/', manager_views.add_parking_space, name='add-parking-space'),
    path('manager/rentals/<str:username>/', manager_views.list_rentals, name='manage-rentals'),
    path('manager/rentals/confirm/<int:rental_id>/', manager_views.confirm_payment, name='confirm-payment'),
    path('manager/rentals/cancel/<int:rental_id>/', manager_views.cancel_rental, name='cancel-rental')
]