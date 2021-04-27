from django.test import TestCase, Client
from TAApp.models import MyUser,Administrator, Course, Instructor, TA


class TestAdminLogin(TestCase):
    client = None

    def setUp(self):
        self.client = Client();

        admin = Administrator(name="admin", password="admin")
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

class TestAddCourse(TestCase):
    client = None

    def setUp(self):
        self.client = Client()
        admin = Administrator(name="admin", password="admin")
        admin.save()
        instructor = Instructor(name="instructor", project_manager="admin")
        instructor.save()
        technicalAssistant = TA(name="TA", project_manager="instructor")
        technicalAssistant.save()
        course = Course(name="test", description="example", project_manager="admin", instructor="instructor", instructorTA="TA")
        course.save()
    def test_course_added(self):
        response = self.client.post("/courses/", {"course-title":"test", "course-description":"example"})
        self.assertEqual(response.context["course-title"], "test", "The course wasn't added successfully")
    def test_bad_course(self):
        response = self.client.post("/courses/", {"course-title": "", "course-description":"example"})
        self.assertFalse(response.context["course-title"], "", "The course was added when it wasn't supposed to be")
        response1 = self.client.post("/courses/", {"course-title":"test", "course-description":""})
        self.assertFalse(response1.context["course-description"], "", "The course was added when it wasn't supposed to be")


