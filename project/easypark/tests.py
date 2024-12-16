from django.test import TestCase

from easypark.models import User, Manager, ParkingSpace, Vehicle, Rental

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            name='Alice', 
            username='alice', 
            email='alice@email.com', 
            password='password', 
            phone='1111111111111'
        )

    def test_user(self):
        user = User.objects.get(username='alice')
        self.assertEqual(user.name, 'Alice')
        self.assertEqual(user.email, 'alice@email.com')
        self.assertEqual(user.password, 'password')
        self.assertEqual(user.phone, '1111111111111')
    
class ManagerTestCase(TestCase):
    def setUp(self):
        Manager.objects.create(
            name='Mario', 
            username='mario', 
            email='mario@email.com', 
            password='password', 
            phone='2222222222222',
            manager_code='123456'
        )
        
    def test_manager(self):
        manager = Manager.objects.get(username='mario')
        self.assertEqual(manager.name, 'Mario')
        self.assertEqual(manager.email, 'mario@email.com')
        self.assertEqual(manager.password, 'password')
        self.assertEqual(manager.phone, '2222222222222')
        self.assertEqual(manager.manager_code, '123456')

class ParkingSpaceTestCase(TestCase):
    def setUp(self):
        ParkingSpace.objects.create(
            size='small', 
            position='A001', 
            price=10.00, 
            electric_charging=True, 
            handicapped=False, 
            covered=False
        )

    def test_parking_space(self):
        parking_space = ParkingSpace.objects.get(position='A001')
        self.assertEqual(parking_space.size, 'small')
        self.assertEqual(parking_space.price, 10.00)
        self.assertEqual(parking_space.electric_charging, True)
        self.assertEqual(parking_space.handicapped, False)
        self.assertEqual(parking_space.covered, False)

class VehicleTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(
            name='Charles', 
            username='charles',
            email='charles@email.com',
            password='password',
            phone='3333333333333'
        )
        Vehicle.objects.create(
            owner=user,
            license_plate='ABC1234',
            model='Toyota',
            color='Red'
        )

    def test_vehicle(self):
        vehicle = Vehicle.objects.get(license_plate='ABC1234')
        self.assertEqual(vehicle.owner.username, 'charles')
        self.assertEqual(vehicle.model, 'Toyota')
        self.assertEqual(vehicle.color, 'Red')

class RentalTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(
            name='Daniel', 
            username='daniel',
            email='daniel@email.com',
            password='password',
            phone='4444444444444'
        )
        vehicle = Vehicle.objects.create(
            owner=user,
            license_plate='ABC1234',
            model='Toyota',
            color='Red'
        )
        Rental.objects.create(
            vehicle=vehicle,
            start_date='2021-01-01',
            end_date='2021-01-02',
            payment_method='Cash'
        )

    def test_rental(self):
        rental = Rental.objects.get(vehicle__license_plate='ABC1234')
        self.assertEqual(rental.vehicle.owner.username, 'daniel')
        self.assertEqual(rental.start_date, '2021-01-01')
        self.assertEqual(rental.end_date, '2021-01-02')
        self.assertEqual(rental.payment_method, 'Cash')
