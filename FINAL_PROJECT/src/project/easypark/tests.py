from django.test import TestCase

from easypark.models import User, Manager, ParkingSpace, Vehicle, Rental

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(name='Alice', username='alice', email='alice@email.com', password='password', phone='1111111111111')

    def test_user(self):
        user = User.objects.get(username='alice')
        self.assertEqual(user.name, 'Alice')
        self.assertEqual(user.email, 'alice@email.com')
        self.assertEqual(user.password, 'password')
        self.assertEqual(user.phone, '1111111111111')
    
class ManagerTestCase(TestCase):
    def setUp(self):
        Manager.objects.create(name='Mario', username='mario', email='mario@email.com', password='password', phone='2222222222222',
                               manager_code='123456')
        
    def test_manager(self):
        manager = Manager.objects.get(username='mario')
        self.assertEqual(manager.name, 'Mario')
        self.assertEqual(manager.email, 'mario@email.com')
        self.assertEqual(manager.password, 'password')
        self.assertEqual(manager.phone, '2222222222222')
        self.assertEqual(manager.manager_code, '123456')
