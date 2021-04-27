from django.test import TestCase, Client
from django.urls import reverse
from TAApp.models import MyUser,Administrator, Course, Instructor, TA

class TestAdminLogin(TestCase):
    client = None

    def setUp(self):
        self.client = Client();

        admin = Administrator(name="admin", password="admin")
        admin.save()

    def test_successful_login(self):
        response = self.client.post("/", {"name": "admin", "password": "admin"}, follow=True)
        self.assertEqual(response.context['name'], "admin", "The name is not passed from login")

    def test_existing_user(self):
        response = self.client.post("/", {"name": "admin", "password": "anotherPassword"}, follow=True)
        self.assertEqual(response.context['message'], "bad password", "The password for admin is admin, not anotherPassword")

    def test_invalid_user(self):
        response = self.client.post("/", {"name": "invalid-user", "password": "invalid-password"}, follow=True)
        self.assertTrue(response.context['message'], "bad user", "The user isn't in the database")

    def test_success(self):
        response = self.client.get('/admin_home/')
        self.assertEqual(response.status_code, 200, "The home page was not loaded properly")
class TestRegisterAccount(TestCase):
    client = None
    def setUp(self):
        self.client = Client()
        admin = Administrator(name="admin", password="admin")
        admin.save()
        self.register_url = reverse('/register/')
    def test_register_page_opens(self):
        response = self.client.get(self.register_url)
        self.assertTemplateUsed(response.status_code, 200)
    def test_successful_register_user(self):
        response = self.client.post("/register/",{'name':"someUser", 'password':"1234"})
        self.assertEqual(response.context['name'], "someUser", "User was not added properly after registering")
    def test_register_with_same_email(self):
        response = self.client.post('/register/',{'name':"admin", 'password': "admin1"})
        self.assertEqual(response.status_code, 400, "The admin user is already a user in the database")
class TestAddCourse(TestCase):
    client = None
    def setUp(self):
        self.client = Client()
        admin = Administrator(name="admin", password="admin")
        admin.save()
        instructor = Instructor(name="instructor", project_manager=admin)
        instructor.save()
        technicalAssistant = TA(name="TA", project_manager=instructor)
        technicalAssistant.save()
        course = Course(name="test", description="example", project_manager=admin, instructor=instructor, instructorTA=technicalAssistant)
        course.save()
    def test_course_added(self):
        response = self.client.post("/courses/", {"name":"test", "instructor":"instructor", "instructorTA":"TA", "description":"example"}, follow=True)
        self.assertEqual(response.context["name"], "test", "The course wasn't added successfully")
    def test_bad_name(self):
        response = self.client.post("/courses/", {"name":"", "instructor":"instructor", "instructorTA":"TA", "description":"example"}, follow=True)
        self.assertFalse(response.context["name"], "", "The course was added when it wasn't supposed to be")
    def test_bad_description(self):
        response = self.client.post("/courses/", {"name":"test", "instructor":"instructor", "instructorTA":"TA", "description":""}, follow=True)
        self.assertFalse(response.context["description"], "", "The course was added when it wasn't supposed to be")
    def test_bad_instructor(self):
        response = self.client.post("/courses/", {"name": "test", "instructor": "Superman", "instructorTA": "TA", "description": "example"}, follow=True)
        self.assertFalse(response.context["instructor"], "Superman", "Superman is not an instructor within the database")
    def test_bad_TA(self):
        response = self.client.post("/courses/", {"name": "test", "instructor": "instructor", "instructorTA": "Hamburglar","description": "example"}, follow=True)
        self.assertFalse(response.context['instructorTA'], "Hamburglar", "Hamburglar is not a TA within the database")
class TestAddTA(TestCase):
    client=None
    def setUp(self):
        self.client = Client()


