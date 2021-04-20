from django.test import TestCase, Client
from .models import MyUser

class TestLogin(TestCase):
    client = None
    def setUp(self):
        self.client = Client();

        admin = MyUser(name = "admin", password="admin")
        admin.save()
    def test_successful_login(self):
        response = self.client.post("/login/", {"name":"admin", "password":"admin"})
        self.assertEqual(response.context['name'], "admin", "The name is not passed from login")
    def test_existing_user(self):
        response = self.client.post("/login/", {"name":"admin", "password":"anotherPassword"})
        self.assertFalse(response.context['password'], "incorrect", "The password for admin is admin, not anotherPassword")

