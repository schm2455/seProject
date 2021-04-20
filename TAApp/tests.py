from django.test import TestCase, Client
from TAApp.models import MyUser


class TestLogin(TestCase):
    client = None

    def setUp(self):
        self.client = Client();

        admin = MyUser(name="admin", password="admin")
        admin.save()

    def test_successful_login(self):
        response = self.client.post("/", {"name": "admin", "password": "admin"})
        self.assertEqual(response.context['name'], "admin", "The name is not passed from login")

    def test_existing_user(self):
        response = self.client.post("/", {"name": "admin", "password": "anotherPassword"})
        self.assertEqual(response.context['message'], "bad password",
                         "The password for admin is admin, not anotherPassword")

    def test_invalid_user(self):
        response = self.client.post("/", {"name": "invalid-user", "password": "invalid-password"})
        self.assertTrue(response.context['message'], "bad user", "The user isn't in the database")

    def test_success(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200, "The /things/ page was not loaded properly")
