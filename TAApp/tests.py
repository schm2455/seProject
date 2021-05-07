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
        pass
    def test_courses_description(self):
        pass
    def test_courses_project_manager(self):
        pass
    def test_courses_instructors(self):
        pass
    def test_courses_instructor_TA(self):
        pass
    #Test Lab Model
    def test_lab_name(self):
        pass
    def test_lab_description(self):
        pass
    def test_lab_project_manager(self):
        pass
    def test_lab_TA(self):
        pass
    def test_lab_for_course(self):
        pass



class TestViews(TestCase):
    @classmethod
    def setUp(cls):
        number_of_administrators = 5;
        for admin_id in range(number_of_administrators):
            Administrator.objects.create(name=f'Admin {admin_id}', password=f'Password{admin_id}')
    #Test Login Views

    #Test Admin_Home Views

    #Test Courses Views

    #Test Register Views

    #Test TA_Home Views

    def test_post_login(self):
        print("Start post login")
        for i in range(4):
            user = 'name' + str(i)
            self.name.append(user)
            password = self.credentials.post(user)
            self.assertIsNotNone(password)
            self.password.append(password)
            print("Password length = ", len(self.password))
            print(self.password)
            print("Username length = ", len(self.name))
            print(self.name)
            print("\n Finish set \n")
class TestAdminHome(TestCase):
    adminData = Admin_home()
    TA = []
    course = []
    assignment = []
    def test_get_admin_home(self):
        print("Start get for admin_home")
        length = len(self.course)
        for i in range(6):
            if i < length:
                self.assertEqual(self.course[i], self.adminData.get(self.course[i]))
            else:
                print("There's no more courses in the database")
                self.assertEqual("There is no such course", self.course[i])
class TestCourses(TestCase):
    course = Courses()
    name = []
    instructorTA = []
    description = []
    def test_get_courses(self):
        print("Start get for courses")
        length = len(self.name)
        for i in range(6):
            if i < length:
                self.assertEqual(self.name[i], self.course.get(self.name[i]))
            else:
                print("There are no more courses in the database")
                self.assertEqual("There is no such name", self.name[i])
class TestRegister(TestCase):
    register = Register()
    name = []
    password = []
    def test_get_register(self):
        print("Start get for courses")
        print("Testing name...")
        length = len(self.name)
        for i in range(4):
            if i < length:
                self.assertEqual(self.name[i], self.register.get(self.name[i]))
            else:
                print("There were no more people to register in the database")
                self.assertEqual("There is no such name", self.name[i])
        print("Testing password...")
        length = len(self.password)
        for i in range(4):
            if i < length:
                self.assertEqual(self.password[i], self.register.get(self.password[i]))
            else:
                print("There were no more people to register in the database")
                self.assertEqual("There is no such password", self.password[i])
    def test_post_register(self):
        print("Start post TestRegister")
        for i in range(4):
            name = 'name' + str(i)
            self.username.append(name)
            password = self.register.post(name)
            self.assertIsNotNone(password)
            self.password.append(password)
            print("Password length = ", len(self.password))
            print(self.password)
            print("Username length = ", len(self.username))
            print(self.username)
            print("\n Finish set \n")
class TA_home(TestCase):
    taHome = CreateTA()

    def test_post_ta_home(self):
        print("Start post TA_home")
        print("\n Finish post TA_home\n")
    def test_get_ta_home(self):
        print("Start get TA_home")
        print("\n Finish get TA_home\n")



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



