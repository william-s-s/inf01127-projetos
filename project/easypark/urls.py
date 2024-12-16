from django.urls import path, register_converter

from .views import homepage_views, user_views, manager_views
from .utils.converters import DateConverter

register_converter(DateConverter, 'date')

app_name = 'easypark'

urlpatterns = [
    path('', homepage_views.index, name='index'),
    path('register-user/', homepage_views.register_user, name='register-user'),
    path('register-manager/', homepage_views.register_manager, name='register-manager'),
    #path('login-user/', homepage_views.login_user, name='login-user'),
    #path('login-manager/', homepage_views.login_manager, name='login-manager'),
    path('login/', homepage_views.login, name='login'),
    path('user/home/<str:username>/', user_views.user_home, name='user-home'),
    path('user/parking-spaces/<str:username>/', user_views.list_parking_spaces, name='user-spaces'),
    path('user/vehicles/<str:username>/', user_views.list_user_vehicles, name='user-vehicles'),
    path('user/vehicles/add-vehicle/<str:username>/', user_views.add_vehicle, name='add-vehicle'),
    path('user/vehicles/remove-vehicle/<str:username>/<int:vehicle_id>/', user_views.remove_vehicle, name='remove-vehicle'),
    path('user/rentals/<str:username>/', user_views.list_user_rentals, name='user-rentals'),
    path('user/rentals/enter-rental-time/<str:username>/', user_views.enter_rental_time, name='enter-rental-time'),
    path('user/rentals/available-spaces/<str:username>/<date:entry_time>/<date:exit_time>/', user_views.available_spaces, name='available-spaces'),
    path('user/rentals/add-rental/<str:username>/<date:entry_time>/<date:exit_time>/<str:position>/', user_views.add_rental, name='add-rental'),
    path('manager/home/<str:username>/', manager_views.manager_home, name='manager-home'),
    path('manager/parking-spaces/<str:username>/', manager_views.list_parking_spaces, name='manager-spaces'),
    path('manager/parking-spaces/add-space/<str:username>/', manager_views.add_parking_space, name='add-space'),
    path('manager/parking-spaces/edit-space/<str:username>/<str:position>/', manager_views.edit_parking_space, name='edit-space'),
    path('manager/rentals/<str:username>/', manager_views.list_rentals, name='manager-rentals'),
    path('manager/rentals/confirm/<str:username>/<int:rental_id>/', manager_views.confirm_payment, name='confirm-payment'),
    path('manager/rentals/cancel/<str:username>/<int:rental_id>/', manager_views.cancel_rental, name='cancel-rental')
]