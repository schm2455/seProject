from django.test import TestCase, Client
from .models import Administrator, Instructor, TA, Course, Lab
from .views import Login, Admin_home, Courses, Register, CreateTA



#Unit Tests
class TestModels(TestCase):
    def setUp(self):
        administrator = Administrator.objects.create(name='admin', password='admin')
        instructor = Instructor.objects.create(name="instructor", project_manager=administrator)
        instructorTA = TA.objects.create(name="TA", project_manager=instructor)
        course = Course.objects.create(name = "course", description="A course", project_manager=administrator, instructor=instructor, instructorTA=instructorTA)
        lab = Lab.objects.create(name='lab', description='lab for course', project_manager=instructor,labTA=instructorTA,labForCourse=course)

    #Test Administrator Model
    def test_admin_name(self):
        admin = Administrator.objects.get(id=1)
        response = admin._meta.get_field('name').verbose_name
        self.assertEqual(response, 'name')
    def test_admin_password(self):
        admin=Administrator.objects.get(id=1)
        response = admin._meta.get_field('password').verbose_name
        self.assertEqual(response, 'password')
    def test_admin_role(self):
        admin=Administrator.objects.get(id=1)
        response = admin._meta.get_field('role').verbose_name
        self.assertEqual(response, 'Admin')

    #Test Instructor Model
    def test_instructor_name(self):
        instructor1 = Instructor.objects.get(id=1)
        response = instructor1._meta.get_field('name').verbose_name
        self.assertEqual(response,'name')
    def test_instructor_project_manager(self):
        instructor1 = Instructor.objects.get(id=1)
        response = instructor1._meta.get_field('project_manager').verbose_name
        self.assertEqual(response,'project manager')

    #Test TA Model
    def test_TA_name(self):
        instructorTA1 = TA.objects.get(id=1)
        response = instructorTA1._meta.get_field('name').verbose_name
        self.assertEqual(response, 'name')
    def test_TA_project_manager(self):
        instructorTA1 = TA.objects.get(id=1)
        response = instructorTA1._meta.get_field('project_manager').verbose_name
        self.assertEqual(response, 'project manager')
    #Test Courses Model
    def test_courses_name(self):
        course = Course.objects.get(id=1)
        expected_course_name = f'{course.name}'
        self.assertEqual(expected_course_name, 'course')
    def test_courses_description(self):
        course = Course.objects.get(id=1)
        expected_course_description = f'{course.description}'
        self.assertEqual(expected_course_description, "A course")
    def test_courses_project_manager(self):
        course = Course.objects.get(id=1)
        admin = Administrator.objects.get(id=1)
        expected_course_project_manager = f'{course.project_manager}'
        self.assertEqual(expected_course_project_manager, str(admin.name))
    def test_courses_instructors(self):
        course = Course.objects.get(id=1)
        instructor = Instructor.objects.get(id=1)
        expected_course_instructor = f'{course.instructor}'
        self.assertEqual(expected_course_instructor, str(instructor.name))
    def test_courses_instructor_TA(self):
        course = Course.objects.get(id=1)
        instructorTA = TA.objects.get(id=1)
        expected_course_TA = f'{course.instructorTA}'
        self.assertEqual(expected_course_TA, str(instructorTA.name))
    #Test Lab Model
    def test_lab_name(self):
        lab = Lab.objects.get(id=1)
        expected_lab_name = f'{lab.name}'
        self.assertEqual(expected_lab_name, str('lab'))
    def test_lab_description(self):
        lab = Lab.objects.get(id=1)
        expected_lab_description = f'{lab.description}'
        self.assertEqual(expected_lab_description, "lab for course")
    def test_lab_project_manager(self):
        lab = Lab.objects.get(id=1)
        project_manager = Instructor.objects.get(id=1)
        expected_lab_project_manager = f'{lab.project_manager}'
        self.assertEqual(expected_lab_project_manager, str(project_manager.name))
    def test_lab_TA(self):
        lab = Lab.objects.get(id=1)
        lab_TA = TA.objects.get(id=1)
        expected_lab_TA = f'{lab.labTA}'
        self.assertEqual(expected_lab_TA, str(lab_TA.name))
    def test_lab_for_course(self):
        lab = Lab.objects.get(id=1)
        lab_for_course = Course.objects.get(id=1)
        expected_lab_for_course = f'{lab.labForCourse}'
        self.assertEqual(expected_lab_for_course, str(lab_for_course.name))

#Test Login Views
class TestLoginViews(TestCase):
    @classmethod
    def setUp(cls):
        user = Administrator.objects.create(name="Admin", password="12345")
        user.save()

    def test_login_url_works(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_login_get(self):
        pass
    def test_login_pass_admin(self):
        pass
    def test_login_pass_instructor(self):
        pass
    def test_login_pass_TA(self):
        pass
    def test_login_bad_password(self):
        pass
    def test_login_no_user_found(self):
        pass

#Test Admin_Home Views
class TestAdminHomeViews(TestCase):
    def setUp(self):
        admin = Administrator.objects.create(name="Admin", password="Admin")
    def test_admin_page_can_open(self):
        response = self.client.get('/admin_home/')
        self.assertEqual(response.status_code, 200)
    def test_admin_page_get(self):
        pass
#Test Courses Views
class TestCourseViews(TestCase):
    def setUp(self):
        admin = Administrator.objects.create(name='Admin', password='Admin')
        instructor = Instructor.objects.create(name='Instructor', project_manager=admin)
        instructorTA = TA.objects.create(name='TA', project_manager=instructor)
        course = Course.objects.create(name='Course', description='A course', project_manager=admin, instructor=instructor, instructorTA=instructorTA)
    def test_course_page_can_open(self):
        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, 200)
    def test_course_get(self):
        pass
    def test_course_if_admin(self):
        pass
    def test_course_if_instructor(self):
        pass
    def test_course_if_neither_admin_nor_instructor(self):
        pass
#Test Register Views
class TestRegisterViews(TestCase):
    def setUp(self):
        admin = Administrator.objects.create(name="Admin", password="Admin")
    def test_register_page_can_open(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
    def test_new_user_added_successfully(self):
        pass
    def test_user_already_exists(self):
        pass
#Test Create TA
class TestCreateTA(TestCase):
    def setUp(self):
        admin = Administrator.objects.create(name='Admin', password='Admin')
        instructor = Instructor.objects.create(name='Instructor', project_manager=admin)
    def test_create_TA_page_opens(self):
        response = self.client.post('/TAs/')
        self.assertEqual(response.status_code, 200)
    def test_TA_already_exists(self):
        pass
    def test_TA_successfully_created_TA(self):
        pass
    def test_TA_Instructor_exists(self):
        pass
    def test_user_is_admin(self):
        pass
    def test_user_is_instructor(self):
        pass
#Test TA_Home Views
class TestTAHomeViews(TestCase):
    def setUp(self):
        admin = Administrator.objects.create(name="Admin", password="Admin")
        instructor = Instructor.objects.create(name="instructor", project_manager=admin)
        instructorTA = TA.objects.create(name="TA", project_manager=instructor)
    def test_TA_home_page_can_open(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
    def test_TA_home_get(self):
        pass
#Test Instructor Home View
class TestInstructorHomeView(TestCase):
    def setUp(self):
        admin = Administrator.objects.create(name='Admin', password='Admin')
        instructor = Instructor.objects.create(name='Instructor', project_manager=admin)
    def test_instructor_home_page_opens(self):
        response = self.client.get('/instructors/')
        self.assertEqual(response.status_code, 200)
    def test_instructor_get(self):
        pass
#Test Create Instructor
class TestCreateInstructor(TestCase):
    def setUp(self):
        admin = Administrator.objects.create(name='Admin', password='Admin')
    def test_create_instructor_page_opens(self):
        response = self.client.get('/instructors/')
        self.assertEqual(response.status_code, 200)
    def test_create_instructor_get(self):
        pass
    def test_instructor_already_exists(self):
        pass
    def test_instructor_created_successfully(self):
        pass


#Acceptance Tests
class TestAdminLogin(TestCase):
    client = None

    def setUp(self):
        self.client = Client();

        admin = Administrator(name="admin", password="admin")
        admin.save()

    def test_successful_login(self):
        response = self.client.post("/", {"name": "admin", "password": "admin"}, follow=True)
        self.assertEqual(response.context['user'], "admin", "User didn't properly log in")

    def test_existing_user(self):
        response = self.client.post("/", {"name": "admin", "password": "anotherPassword"}, follow=True)
        self.assertFalse(response.context['user'], "No such user.", "The password for admin is admin, not anotherPassword")

    def test_invalid_user(self):
        response = self.client.post("/", {"name": "invalid-user", "password": "invalid-password"}, follow=True)
        self.assertEqual(response.context['message'], "No such user.", "The user isn't in the database")

    def test_success(self):
        response = self.client.get('/admin_home/')
        self.assertEqual(response.status_code, 200, "The home page was not loaded properly")

class TestRegisterAccount(TestCase):
    client = None
    def setUp(self):
        self.client = Client()
        admin = Administrator(name="admin", password="admin")
        admin.save()
    def test_register_page_opens(self):
        response = self.client.get('//register/')
        self.assertEqual(response.status_code, 200)
    def test_successful_register_user(self):
        self.client.post("/register/",{"name":"someUser", 'password':"1234"})
        response2 = self.client.post("/",{'name':"someUser", 'password':"1234"})
        self.assertEqual(response2.status_code, 200, "User was not added properly after registering")
    def test_register_with_same_email(self):
        response = self.client.post('/register/',{"name":"admin", 'password': "admin1"})
        self.assertEqual(response.status_code, 405, "The admin user is already a user in the database")

class TestAddCourse(TestCase):
    client = None
    courses = None
    def setUp(self):
        self.client = Client()
        self.courses = {"potter":["math", "science"], "hagrid":["art","history"]}

        for i in self.courses.keys():
            admin = Administrator(name="admin"+i, password="admin"+i)
            admin.save()
            instructor = Instructor(name="instructor"+i, project_manager=admin)
            instructor.save()
            technicalAssistant = TA(name="TA"+i, project_manager=instructor)
            technicalAssistant.save()
            for j in self.courses[i]:
                Courses(name="test"+j, description="example"+j, project_manager=admin, instructor=instructor, instructorTA=technicalAssistant).save()
    def test_course_added(self):
        session = self.client.session
        session["name"] = "potter"
        session.save()
        response = self.client.post("/courses/", {"name":"new course", "instructor":"instructor", "instructorTA":"TA", "description":"example" }, follow=True)
        self.assertListEqual(["math","science","new course"], response.context["courses"], "The course wasn't added successfully")
    def test_bad_name(self):
        response = self.client.post("/courses/", {"name":"", "instructor":"instructor", "instructorTA":"TA", "description":"example"}, follow=True)
        self.assertFalse(response.context["name"], "", "The course was added when it wasn't supposed to be")
    def test_bad_description(self):
        response = self.client.post("/courses/", {"name":"test", "instructor":"instructor", "instructorTA":"TA", "description":""}, follow=True)
        self.assertFalse(response.context["desc"], "", "The course was added when it wasn't supposed to be")
    def test_bad_instructor(self):
        response = self.client.post("/courses/", {"name": "test", "instructor": "Superman", "instructorTA": "TA", "description": "example"}, follow=True)
        self.assertFalse(response.context["instructor"], "Superman", "Superman is not an instructor within the database")
    def test_bad_TA(self):
        response = self.client.post("/courses/", {"name": "test", "instructor": "instructor", "instructorTA": "Hamburglar","description": "example"}, follow=True)
        self.assertEqual(response.context['message'], "TA doesn't exist", "Hamburglar is not a TA within the database")



