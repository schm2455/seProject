from unittest.mock import Mock

from django.contrib.messages.storage import session
from django.test import TestCase, Client
from django.urls import reverse

from .models import Administrator, Instructor, TA, Course, Lab, MyUser
from .views import Login, Admin_home, Courses, Register, CreateTA, direct, valid



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
class BaseTest(TestCase):
    def setUp(self):
        self.register_url=reverse('register')
        self.login_url=reverse('login')
        self.admin_home_url=reverse('admin_home')
        self.courses = reverse('courses')
        self.instructor_home_url=reverse('instructor_home')
        self.edit_courses_url=reverse('edit_courses')
        self.create_TA_url=reverse('create_TA')
        self.TA_home_url=reverse('TA_home')
        self.create_instructor_url=reverse('create_instructor')
        self.assign_TA=reverse('assign_TA')
        self.go_back=reverse('go_back')
        self.make_assignment=reverse('make_assignment')
        self.this_course_page=reverse('this_course')
        self.delete_course=reverse('delete_course')
        self.admin={
            'name':'admin',
            'password':'admin',
            'job':'Admin'
        }
        self.instructor={
            'name':'instructor',
            'password':'instructor',
            'job':'Instructor'
        }
        self.TA={
            'name':'TA',
            'password':'TA',
            'job':'TA'
        }
        self.user_already_active={
            'name':'admin',
            'password':'bad password',
            'job':'Admin'
        }
        self.user_does_not_select_job={
            'name':'test user',
            'password': 'password',
            'job':'Select...'
        }
        return super().setUp()


#Test Register Views
class RegisterTest(BaseTest):
    def test_can_view_page(self):
        response = self.client.post(self.register_url, self.admin, format="test/html")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'register.html')
    def test_can_register_admin(self):
        response = self.client.post(self.register_url,self.admin, format='test/html')
        self.assertEqual(response.status_code, 200)
    def test_can_register_instructor(self):
        response = self.client.post(self.register_url,self.instructor, format='test/html')
        self.assertEqual(response.status_code, 302)
    def test_can_register_TA(self):
        response = self.client.post(self.register_url, self.TA, format='test/html')
        self.assertEqual(response.status_code, 302)
    def test_user_already_registered(self):
        self.client.post(self.register_url, self.admin, format='test/html')
        response = self.client.post(self.register_url, self.user_already_active, format='test/html')
        self.assertEqual(response.context['message'], "Please try again!")
    def test_user_does_not_select_job(self):
        response = self.client.post(self.register_url, self.user_does_not_select_job, format='test/html')
        self.assertEqual(response.context['message'], 'Duplicate user')


#Test Login Views
class TestLoginView(BaseTest):
    def test_login_url_works(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
    def test_login_pass_admin(self):
        self.client.post(self.register_url, self.admin, format='test/html')
        admin = MyUser.objects.filter(name=self.admin['name']).first()
        admin.save()
        response = self.client.post(self.login_url, self.admin, format='text/html')
        self.assertEqual(response.status_code, 302)
    def test_login_pass_instructor(self):
        self.client.post(self.register_url, self.instructor, format='test/html')
        instructor = Instructor.objects.filter(name=self.instructor['name']).first()
        instructor.save()
        response = self.client.post(self.login_url, self.instructor, format='text/html')
        self.assertEqual(response.status_code, 302)
    def test_login_pass_TA(self):
        self.client.post(self.register_url, self.TA, format='test/html')
        instructorTA = TA.objects.filter(name=self.TA['name']).first()
        instructorTA.save()
        response = self.client.post(self.login_url, self.TA, format='text/html')
        self.assertEqual(response.status_code,302)
    def test_login_bad_password(self):
        self.client.post(self.register_url, self.admin, format='text/html')
        response = self.client.post(self.login_url, self.user_already_active, format='text/html')
        self.assertEqual(response.context['message'], "Bad Password")
    def test_login_no_user_found(self):
        response = self.client.post(self.login_url, self.admin, format='text/html')
        self.assertEqual(response.context['message'], "No Such User")

#Test Direct Method
class TestDirectMethod(BaseTest):
    def test_admin_role(self):
        admin=Administrator.objects.create(name="Admin", password="Admin")
        response=direct(admin.job)
        self.assertEqual(response.status_code, 302)
    def test_instructor_role(self):
        admin=Administrator.objects.create(name="Admin", password="Admin")
        instructor=Instructor.objects.create(name="Instructor", project_manager=admin)
        response=direct(instructor.role)
        self.assertEqual(response.status_code, 302)
    def test_TA_role(self):
        admin=Administrator.objects.create(name="Admin", password="Admin")
        instructor=Instructor.objects.create(name="Instructor", project_manager=admin)
        instructorTA=TA.objects.create(name="TA", project_manager=instructor)
        response=direct(instructorTA.role)
        self.assertEqual(response.status_code, 302)
#Test Valid Method
class TestValidMethod(BaseTest):
    def test_expected_admin_role(self):
        admin=Administrator.objects.create(name="Admin", password="Admin")
        response=valid(admin.job, "Admin")
        self.assertEqual(response, True)
    def test_expected_instructor_role(self):
        admin=Administrator.objects.create(name="Admin", password="Admin")
        instructor=Instructor.objects.create(name="Instructor", project_manager=admin)
        response=valid(instructor.role, "Instructor")
        self.assertEqual(response, True)
    def test_expected_TA_role(self):
        admin=Administrator.objects.create(name="Admin", password="Admin")
        instructor=Instructor.objects.create(name="Instructor", project_manager=admin)
        instructorTA=TA.objects.create(name="TA", project_manager=instructor)
        response=valid(instructorTA.role, "TA")
        self.assertEqual(response, True)
#Test Admin Home Views
class TestAdminHomeViews(BaseTest):
    def test_admin_page_get_logged_in_user(self):
        self.client.post(self.register_url, self.admin, format='text/html')
        self.client.post(self.login_url, self.admin, format='text/html')
        response = self.client.get(self.admin_home_url)
        self.assertEqual(response.status_code, 200)
    def test_admin_page_load_TA_list(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        self.client.post(self.register_url, data={'name':testAdmin.name, 'password':testAdmin.password, 'job':testAdmin.job}, format='text/html')
        self.client.post(self.login_url, data={'name':testAdmin.name, 'password':testAdmin.password}, format='text/html')
        testInstructor = Instructor.objects.create(name="Instructor", project_manager=testAdmin)
        testInstructor.save()
        testTA = TA.objects.create(name="TA", project_manager=testInstructor)
        testTA.save()
        response = self.client.get(self.admin_home_url)
        self.assertEqual(response.context['TAs'], ["TA"])
    def test_admin_page_load_instructor_list(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        self.client.post(self.register_url,data={'name': testAdmin.name, 'password': testAdmin.password, 'job': testAdmin.job}, format='text/html')
        self.client.post(self.login_url, data={'name': testAdmin.name, 'password': testAdmin.password}, format='text/html')
        testInstructor = Instructor.objects.create(name="Instructor", project_manager=testAdmin)
        testInstructor.save()
        response = self.client.get(self.admin_home_url)
        self.assertEqual(response.context['instructors'], ["Instructor"], "Instructors for TA did not load properly")
    def test_admin_page_load_course_list(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        testInstructor = Instructor.objects.create(name="Instructor", project_manager=testAdmin)
        testInstructor.save()
        testTA = TA.objects.create(name="TA", project_manager=testInstructor)
        testTA.save()
        testCourse = Course.objects.create(name="Course", description="Course Description", project_manager=testAdmin, instructor=testInstructor, instructorTA=testTA)
        testCourse.save()
        self.client.post(self.register_url, data={'name': testAdmin.name, 'password': testAdmin.password, 'job': testAdmin.job}, format='text/html')
        self.client.post(self.login_url, data={'name': testAdmin.name, 'password': testAdmin.password}, format='text/html')
        response = self.client.get(self.admin_home_url)
        self.assertIn(testCourse,response.context['courses'], "Courses did not load properly")



#Test Courses Views
class TestCourseViews(BaseTest):
    def test_admin_access_course_page(self):
        self.client.post(self.register_url, self.admin, format='text/html')
        self.client.post(self.login_url, self.admin, format='text/html')
        response = self.client.get(self.courses)
        self.assertEqual(response.status_code, 200)
    def test_instructor_access_course_page(self):
        self.client.post(self.register_url, self.instructor, format='text/html')
        self.client.post(self.login_url, self.instructor, format='text/html')
        response = self.client.get(self.courses)
        self.assertEqual(response.status_code,200)
    def test_TA_can_not_use_courses(self):
        self.client.post(self.register_url, self.TA, format='text/html')
        self.client.post(self.login_url, self.TA, format='text/html')
        response = self.client.get(self.courses, self.TA, format='text/html')
        self.assertEqual(response.context['message'], "unauthorized access")
    def test_admin_can_create_course(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        testInstructor = Instructor.objects.create(name="Instructor", project_manager=testAdmin)
        testInstructor.save()
        testTA = TA.objects.create(name="TA", project_manager=testInstructor)
        testTA.save()
        testCourse = Course.objects.create(name="Course", description="Course Description", project_manager=testAdmin, instructor=testInstructor, instructorTA=testTA)
        testCourse.save()
        self.client.post(self.register_url, data={'name': testAdmin.name, 'password': testAdmin.password, 'job': testAdmin.job}, format='text/html')
        self.client.post(self.login_url, data={'name': testAdmin.name, 'password': testAdmin.password}, format='text/html')
        response = self.client.post(self.courses, data={'name': testCourse.name, 'instructorchoice':testInstructor.name, 'tachoice':testTA.name, 'description':testCourse.description}, format='text/html')
        self.assertEqual(response.status_code, 302)
    def test_instructor_can_create_course(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        testInstructor = Instructor.objects.create(name="Instructor", project_manager=testAdmin)
        testInstructor.save()
        otherInstructor = Instructor.objects.create(name="Instructor2", project_manager=testAdmin)
        testTA = TA.objects.create(name="TA", project_manager=testInstructor)
        testTA.save()
        testCourse = Course.objects.create(name="Course", description="Course Description", project_manager=testAdmin, instructor=testInstructor, instructorTA=testTA)
        testCourse.save()
        self.client.post(self.register_url, data={'name':testInstructor.name, 'password':"Instructor", 'job':testInstructor.role}, format='text/html')
        response = self.client.post(self.login_url, data={'name':testInstructor.name, 'password':"Instructor"}, format='text/html')
        self.assertEqual(response.status_code, 302)
        createCourseResponse = self.client.post(self.courses, data={'name':testCourse.name, 'instructorchoice':otherInstructor.name, 'tachoice':testTA.name, 'description':testCourse.description})
        self.assertEqual(createCourseResponse.status_code, 302)


#Test Edit Courses
class TestEditCourses(BaseTest):
    def test_edit_page_opens(self):
        self.client.post(self.register_url, self.admin, format='text/html')
        self.client.post(self.login_url, self.admin, format='text/html')
        response = self.client.get(self.edit_courses_url)
        self.assertEqual(response.status_code, 200)
    def test_admin_correct_courses(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        testInstructor = Instructor.objects.create(name="Instructor", project_manager=testAdmin)
        testInstructor.save()
        testTA = TA.objects.create(name="TA", project_manager=testInstructor)
        testTA.save()
        testCourse = Course.objects.create(name="Course", description="Course Description", project_manager=testAdmin, instructor=testInstructor, instructorTA=testTA)
        testCourse.save()
        self.client.post(self.register_url, data={'name':testAdmin.name, 'password':testAdmin.password, 'job':"Admin"})
        self.client.post(self.login_url, data={'name':testAdmin.name, 'password':testAdmin.password})
        response = self.client.get(self.edit_courses_url)
        self.assertIn(testCourse,response.context['courses'])
    def test_admin_correct_instructors(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        testInstructor = Instructor.objects.create(name="Instructor", project_manager=testAdmin)
        testInstructor.save()
        testTA = TA.objects.create(name="TA", project_manager=testInstructor)
        testTA.save()
        testCourse = Course.objects.create(name="Course", description="Course Description", project_manager=testAdmin, instructor=testInstructor, instructorTA=testTA)
        testCourse.save()
        self.client.post(self.register_url, data={'name': testAdmin.name, 'password': testAdmin.password, 'job': "Admin"})
        self.client.post(self.login_url, data={'name': testAdmin.name, 'password': testAdmin.password})
        response = self.client.get(self.edit_courses_url)
        self.assertIn(testInstructor, response.context['instructors'])
    def test_admin_correct_TA(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        testInstructor = Instructor.objects.create(name="Instructor", project_manager=testAdmin)
        testInstructor.save()
        testTA = TA.objects.create(name="TA", project_manager=testInstructor)
        testTA.save()
        testCourse = Course.objects.create(name="Course", description="Course Description", project_manager=testAdmin, instructor=testInstructor, instructorTA=testTA)
        testCourse.save()
        self.client.post(self.register_url, data={'name': testAdmin.name, 'password': testAdmin.password, 'job': "Admin"})
        self.client.post(self.login_url, data={'name': testAdmin.name, 'password': testAdmin.password})
        response = self.client.get(self.edit_courses_url)
        self.assertIn(testTA, response.context['tachoices'])
    def test_instructor_sign_in(self):
        self.client.post(self.register_url, self.instructor, format="text/html")
        self.client.post(self.login_url, self.instructor, format="text/html")
        response = self.client.get(self.edit_courses_url)
        self.assertEqual(response.context['message'], "unauthorized access")
    def test_TA_sign_in(self):
        self.client.post(self.register_url, self.TA, format="text/html")
        self.client.post(self.login_url, self.TA, format="text/html")
        response = self.client.get(self.edit_courses_url)
        self.assertEqual(response.context['message'], "unauthorized access")

#Test Create TA
class TestCreateTA(BaseTest):
    def test_admin_open_create_TA(self):
        self.client.post(self.register_url, self.admin, format="text/html")
        self.client.post(self.login_url, self.admin, format="text/html")
        response = self.client.get(self.create_TA_url)
        self.assertEqual(response.status_code, 200)
    def test_instructor_open_create_TA(self):
        self.client.post(self.register_url, self.instructor, format="text/html")
        self.client.post(self.login_url, self.instructor, format="text/html")
        response = self.client.get(self.create_TA_url)
        self.assertEqual(response.status_code, 200)
    def test_TA_open_create_TA(self):
        self.client.post(self.register_url, self.TA, format="text/html")
        self.client.post(self.login_url, self.TA, format="text/html")
        response = self.client.get(self.create_TA_url)
        self.assertEqual(response.context['message'], "unauthorized access")
    def test_admin_create_TA(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        testInstructor = Instructor.objects.create(name="Instructor", project_manager=testAdmin)
        testInstructor.save()
        self.client.post(self.register_url, data={'name':testAdmin.name, 'password':testAdmin.password, 'job':"Admin"}, format="text/html")
        self.client.post(self.login_url, data={'name':testAdmin.name, 'password':testAdmin.password}, format="text/html")
        response=self.client.post(self.create_TA_url, data={'name':"testTA", 'instructorchoice':testInstructor,'password':"testTA"}, format="text/html")
        self.assertEqual(response.status_code, 302)
    def test_instructor_create_TA(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        testInstructor = Instructor.objects.create(name="Instructor", project_manager=testAdmin)
        testInstructor.save()
        anotherInstructor=Instructor.objects.create(name="Instructor2", project_manager=testAdmin)
        anotherInstructor.save()
        self.client.post(self.register_url, data={'name':testInstructor.name, 'password':"password", 'job':"Instructor"}, format="text/html")
        self.client.post(self.login_url, data={'name':testInstructor.name, 'password':"password"}, format="text/hmtl")
        response=self.client.post(self.create_TA_url, data={'name':"testTA", 'instructorchoice':anotherInstructor.name, 'password':"password"}, format="text/html")
        self.assertEqual(response.status_code, 302)
    def test_user_did_not_fill_in_the_box(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        testInstructor = Instructor.objects.create(name="Instructor", project_manager=testAdmin)
        testInstructor.save()
        self.client.post(self.register_url, data={'name':testAdmin.name, 'password':testAdmin.password, 'job':"Admin"}, format="text/html")
        self.client.post(self.login_url, data={'name':testAdmin.name, 'password':testAdmin.password}, format="text/html")
        self.client.post(self.create_TA_url, data={'name':"", 'instructorchoice':testInstructor.name,'password':"testTA"}, format="text/html")
        response = self.client.get(self.create_TA_url)
        messages=list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Please fill all the boxes")
    def test_TA_is_already_added(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        testInstructor = Instructor.objects.create(name="Instructor", project_manager=testAdmin)
        testInstructor.save()
        testTA = TA.objects.create(name="TA", project_manager=testInstructor)
        testTA.save()
        self.client.post(self.register_url, data={'name':testAdmin.name, 'password':testAdmin.password, 'job':"Admin"}, format="text/html")
        self.client.post(self.login_url, data={'name':testAdmin.name, 'password':testAdmin.password}, format="text/html")
        self.client.post(self.create_TA_url, data={'name':testTA.name, 'instructorchoice':testInstructor.name,'password':"testTA"}, format="text/html")
        response = self.client.get(self.create_TA_url)
        messages=list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "TA already exists")
#Test TA_Home Views
class TestTAHomeViews(BaseTest):
    def test_TA_home_page_can_open(self):
        self.client.post(self.register_url, self.TA, format="text/html")
        self.client.post(self.login_url, self.TA, format="text/html")
        response=self.client.get(self.TA_home_url)
        self.assertEqual(response.status_code,200)
    def test_page_loads_labs(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        testInstructor = Instructor.objects.create(name="testInstructor", project_manager=testAdmin)
        testInstructor.save()
        testTA = TA.objects.create(name="testTA", project_manager=testInstructor)
        testTA.save()
        testCourse = Course.objects.create(name="Course", description="Course Description", project_manager=testAdmin, instructor=testInstructor, instructorTA=testTA)
        testCourse.save()
        testLab = Lab.objects.create(name="Lab", description="Description for Lab", project_manager=testInstructor, labTA=testTA, labForCourse=testCourse)
        testLab.save()
        self.client.post(self.register_url, data={'name':testTA.name, 'password':"Password", 'job':"TA"}, format="text/html")
        response=self.client.post(self.login_url, data={'name':testTA.name, 'password':"Password"}, format="text/html")
        self.assertEqual(response.status_code, 302)
        loadsLabsResponse=self.client.get(self.TA_home_url, )
        self.assertIn(testLab, loadsLabsResponse.context['labs'])
#Test Instructor Home View
class TestInstructorHomeView(BaseTest):
    def test_instructor_can_access(self):
        self.client.post(self.register_url, self.instructor, format='text/html')
        self.client.post(self.login_url, self.instructor, format='text/html')
        response = self.client.get(self.instructor_home_url)
        self.assertEqual(response.status_code, 200)
    def test_instructor_correct_fields(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        testInstructor = Instructor.objects.create(name="testInstructor", project_manager=testAdmin)
        testInstructor.save()
        #otherInstructor = Instructor.objects.create(name="otherInstructor", project_manager=testAdmin)
        #otherInstructor.save()
        testTA = TA.objects.create(name="testTA", project_manager=testInstructor)
        testTA.save()
        testCourse = Course.objects.create(name="Course", description="Course Description", project_manager=testAdmin, instructor=testInstructor, instructorTA=testTA)
        testCourse.save()
        self.client.post(self.register_url, data={'name': testInstructor.name, 'password': "password", 'job': "Instructor"}, format="text/html")
        self.client.post(self.login_url, data={'name': testInstructor.name, 'password': "password"}, format="text/hmtl")
        self.client.post(self.instructor_home_url, data={'name':testInstructor.name})
        response=self.client.get(self.instructor_home_url)
        self.assertEqual(response.status_code, 200)
        #response=self.client.get(self.instructor_home_url, data={'name':testInstructor.name})
        #self.assertIn(testTA.name, response.context['TAs'])
        #self.assertIn(otherInstructor.name, response.context['instructors'])
        #self.assertIn(testCourse.name, response.context['courses'])
#Test Create Instructor
class TestCreateInstructor(BaseTest):
    def test_admin_has_access_to_create_instructor(self):
        self.client.post(self.register_url, self.admin, format='text/html')
        self.client.post(self.login_url, self.admin, format='text/html')
        response=self.client.post(self.create_instructor_url)
        self.assertEqual(response.status_code, 302)
    def test_instructor_has_access_to_create_instructor(self):
        self.client.post(self.register_url, self.instructor, format='text/html')
        self.client.post(self.login_url, self.instructor, format='text/html')
        response=self.client.post(self.create_instructor_url)
        self.assertEqual(response.status_code, 302)
    def test_admin_add_instructor_success(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        self.client.post(self.register_url, data={'name': testAdmin.name, 'password': testAdmin.password, 'job': "Admin"}, format="text/html")
        self.client.post(self.login_url, data={'name': testAdmin.name, 'password': testAdmin.password}, format="text/html")
        response = self.client.post(self.create_instructor_url, data={'name': testAdmin.name, 'instructor': "Instructor2", 'password':"Instructor2"})
        self.assertEqual(response.status_code, 302)
    def test_instructor_add_instructor_success(self):
        self.client.post(self.register_url, self.instructor, format="text/html")
        self.client.post(self.login_url, self.instructor, format="text/html")
        response = self.client.post(self.create_instructor_url, data={'name':self.instructor, 'instructor':"TestInstructor", 'password':"TestInstructor"})
        self.assertEqual(response.status_code, 302)
    def test_fields_were_not_filled_in(self):
        self.client.post(self.register_url, self.instructor, format="text/html")
        self.client.post(self.login_url, self.instructor, format="text/html")
        self.client.post(self.create_instructor_url, data={'name':self.instructor, 'instructor': "", 'password':"Password"})
        response=self.client.get(self.create_instructor_url)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Please fill all the boxes")
    def test_instructor_already_exists(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        testInstructor = Instructor.objects.create(name="testInstructor", project_manager=testAdmin)
        testInstructor.save()
        self.client.post(self.register_url, data={'name': testAdmin.name, 'password': testAdmin.password, 'job': "Admin"}, format="text/html")
        self.client.post(self.login_url, data={'name': testAdmin.name, 'password': testAdmin.password}, format="text/html")
        self.client.post(self.create_instructor_url, data={'name':testAdmin.name, 'instructor':"testInstructor", 'password':"Password"})
        response=self.client.get(self.create_instructor_url)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Instructor already exists")

#Test Assign TA Views
class TestAssignTAs(BaseTest):
    def test_admin_is_able_to_access_assign_TA_page(self):
        self.client.post(self.register_url, self.admin, format="text/html")
        self.client.post(self.login_url, self.admin, format="text/html")
        response=self.client.get(self.assign_TA)
        self.assertEqual(response.status_code, 200)
    def test_instructor_is_able_to_access_assign_TA_page(self):
        self.client.post(self.register_url, self.instructor, format="text/html")
        self.client.post(self.login_url, self.instructor, format="text/html")
        response=self.client.get(self.assign_TA)
        self.assertEqual(response.status_code, 200)
    def test_admin_can_assign_TA(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        testInstructor = Instructor.objects.create(name="testInstructor", project_manager=testAdmin)
        testInstructor.save()
        testTA = TA.objects.create(name="testTA", project_manager=testInstructor)
        testTA.save()
        testCourse = Course.objects.create(name="Course", description="Course Description", project_manager=testAdmin, instructor=testInstructor, instructorTA=testTA)
        testCourse.save()
        testLab = Lab.objects.create(name="Lab", description="Description for Lab", project_manager=testInstructor, labTA=testTA, labForCourse=testCourse)
        testLab.save()
        self.client.post(self.register_url, data={'name': testAdmin.name, 'password': testAdmin.password, 'job': "Admin"}, format="text/html")
        self.client.post(self.login_url, data={'name': testAdmin.name, 'password': testAdmin.password}, format="text/html")
        self.client.post(self.assign_TA, data={'coursechoice': testCourse.name, 'tachoice':testTA.name, 'lab':testLab.name})
        response=self.client.get(self.assign_TA)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Successfully assigned TA to Lab")
    def test_instructor_can_assign_TA(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        testInstructor = Instructor.objects.create(name="testInstructor", project_manager=testAdmin)
        testInstructor.save()
        testTA = TA.objects.create(name="testTA", project_manager=testInstructor)
        testTA.save()
        testCourse = Course.objects.create(name="Course", description="Course Description", project_manager=testAdmin, instructor=testInstructor, instructorTA=testTA)
        testCourse.save()
        testLab = Lab.objects.create(name="Lab", description="Description for Lab", project_manager=testInstructor, labTA=testTA, labForCourse=testCourse)
        testLab.save()
        self.client.post(self.register_url, data={'name': testInstructor.name, 'password': "Password", 'job': "Instructor"}, format="text/html")
        self.client.post(self.login_url, data={'name': testInstructor.name, 'password': "Password"}, format="text/html")
        self.client.post(self.assign_TA, data={'coursechoice': testCourse.name, 'tachoice':testTA.name, 'lab':testLab.name})
        response=self.client.get(self.assign_TA)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Successfully assigned TA to Lab")
    def test_boxes_are_not_filled_in(self):
        self.client.post(self.register_url, self.instructor, format="format/html")
        self.client.post(self.login_url, self.instructor, format="format/html")
        self.client.post(self.assign_TA, data={'coursechoice': "Select...", 'tachoice': "Select...", 'lab': ""})
        response=self.client.get(self.assign_TA)
        messages=list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Please fill all the boxes")
class TestGoBack(BaseTest):
    def test_go_back_works(self):
        self.client.post(self.register_url, self.admin, format="format/html")
        self.client.post(self.login_url, self.admin, format="format/html")
        response=self.client.get(self.go_back)
        self.assertEqual(response.status_code, 302)
class TestMakeAssignment(BaseTest):
    def test_admin_can_create_assignment(self):
        self.client.post(self.register_url, self.admin, format="format/html")
        self.client.post(self.login_url, self.admin, format="format/html")
        response=self.client.get(self.make_assignment)
        self.assertEqual(response.status_code, 200)
    def test_instructor_can_create_assignment(self):
        self.client.post(self.register_url, self.instructor, format="format/html")
        self.client.post(self.login_url, self.instructor, format="format/html")
        response=self.client.get(self.make_assignment)
        self.assertEqual(response.status_code, 200)
    def test_TA_can_create_assignment(self):
        self.client.post(self.register_url, self.TA, format="format/html")
        self.client.post(self.login_url, self.TA, format="format/html")
        response=self.client.get(self.make_assignment)
        self.assertEqual(response.status_code,200)
    def test_successfully_added_course(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        testInstructor = Instructor.objects.create(name="testInstructor", project_manager=testAdmin)
        testInstructor.save()
        testTA = TA.objects.create(name="testTA", project_manager=testInstructor)
        testTA.save()
        self.client.post(self.register_url, data={'name': testAdmin.name, 'password': testAdmin.password, 'job': "Admin"}, format="text/html")
        self.client.post(self.login_url, data={'name': testAdmin.name, 'password': testAdmin.password}, format="text/html")
        self.client.post(self.make_assignment, data={'name':testAdmin.name, 'tachoice': testTA, 'assignment': "Assignment #1", 'name': "Math"})
        response=self.client.get(self.make_assignment)
        messages=list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Success")


class TestThisCourse(BaseTest):
    def test_this_course_page_returns_correct_info(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        testInstructor = Instructor.objects.create(name="testInstructor", project_manager=testAdmin)
        testInstructor.save()
        testTA = TA.objects.create(name="testTA", project_manager=testInstructor)
        testTA.save()
        testCourse = Course.objects.create(name="Course", description="Course Description", project_manager=testAdmin, instructor=testInstructor, instructorTA=testTA)
        testCourse.save()
        self.client.post(self.register_url, data={'name': testAdmin.name, 'password': testAdmin.password, 'job': "Admin"}, format="text/html")
        self.client.post(self.login_url, data={'name': testAdmin.name, 'password': testAdmin.password}, format="text/html")
        self.client.post(self.courses, data={'name':testCourse.name, 'instructorchoice':testCourse.instructor, 'tachoice':testCourse.instructorTA,'description':testCourse.description})
        response=self.client.get(self.this_course_page, data={'name':testCourse.name})
        self.assertEqual(response.context['inst'], "testInstructor")
        self.assertEqual(response.context['tadude'], "testTA")
        self.assertEqual(response.context['desc'], "Course Description")
        self.assertEqual(response.context['name'], "Course")

class TestDeleteCourse(BaseTest):
    def test_admin_can_access_page(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        testInstructor = Instructor.objects.create(name="testInstructor", project_manager=testAdmin)
        testInstructor.save()
        testTA = TA.objects.create(name="testTA", project_manager=testInstructor)
        testTA.save()
        testCourse = Course.objects.create(name="Course", description="Course Description", project_manager=testAdmin, instructor=testInstructor, instructorTA=testTA)
        testCourse.save()
        self.client.post(self.register_url, data={'name': testAdmin.name, 'password': testAdmin.password, 'job': "Admin"}, format="text/html")
        self.client.post(self.login_url, data={'name': testAdmin.name, 'password': testAdmin.password}, format="text/html")
        response=self.client.get(self.delete_course)
        self.assertEqual(response.status_code, 200)
        self.assertIn(testCourse.name, response.context['courses'])
    def test_instructor_can_access_page(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        testInstructor = Instructor.objects.create(name="testInstructor", project_manager=testAdmin)
        testInstructor.save()
        testTA = TA.objects.create(name="testTA", project_manager=testInstructor)
        testTA.save()
        testCourse = Course.objects.create(name="Course", description="Course Description", project_manager=testAdmin, instructor=testInstructor, instructorTA=testTA)
        testCourse.save()
        self.client.post(self.register_url, data={'name': testInstructor.name, 'password': "testInstructor", 'job': "Instructor"}, format="text/html")
        self.client.post(self.login_url, data={'name': testInstructor.name, 'password': "testInstructor"}, format="text/html")
        response=self.client.get(self.delete_course)
        self.assertEqual(response.status_code, 200)
        self.assertIn(testCourse.name, response.context['courses'])
    def test_successfull_course_deleted(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        testInstructor = Instructor.objects.create(name="testInstructor", project_manager=testAdmin)
        testInstructor.save()
        testTA = TA.objects.create(name="testTA", project_manager=testInstructor)
        testTA.save()
        testCourse = Course.objects.create(name="Course", description="Course Description", project_manager=testAdmin, instructor=testInstructor, instructorTA=testTA)
        testCourse.save()
        self.client.post(self.register_url, data={'name': testAdmin.name, 'password': testAdmin.password, 'job': "Admin"}, format="text/html")
        self.client.post(self.login_url, data={'name': testAdmin.name, 'password': testAdmin.password}, format="text/html")
        self.client.post(self.delete_course, data={'coursechoice':testCourse.name})
        response=self.client.get(self.delete_course)
        messages=list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Successfully deleted course")
    def test_user_did_not_fill_in_all_boxes(self):
        testAdmin = Administrator.objects.create(name="test", password="test")
        testAdmin.save()
        testInstructor = Instructor.objects.create(name="testInstructor", project_manager=testAdmin)
        testInstructor.save()
        testTA = TA.objects.create(name="testTA", project_manager=testInstructor)
        testTA.save()
        testCourse = Course.objects.create(name="Course", description="Course Description", project_manager=testAdmin, instructor=testInstructor, instructorTA=testTA)
        testCourse.save()
        self.client.post(self.register_url, data={'name': testAdmin.name, 'password': testAdmin.password, 'job': "Admin"}, format="text/html")
        self.client.post(self.login_url, data={'name': testAdmin.name, 'password': testAdmin.password}, format="text/html")
        self.client.post(self.delete_course, data={'coursechoice':"Select..."})
        response=self.client.get(self.delete_course)
        messages=list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Please fill all the boxes")







