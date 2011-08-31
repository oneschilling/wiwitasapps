import unittest
from django.test.client import Client
from courses.models import Course, Group, Registration, Semester
from courses.allocation import RandomCourseAllocator
from django.contrib.auth.models import User
from courses.registration import Registrator

class CoursesTestDataMixin:    
    def make_test_data(self):
        self.semester = Semester.objects.create(
            type = 'ws',
            year = 2011,
            current = True,
        )
        
        self.course = Course.objects.create(
            name = 'Testkurs',
            slug = 'tk',
            description = '',
            end_of_preference_phase = '2006-10-25',
            start_of_registration_phase = '2006-10-25',
            semester = self.semester,
            active = True,
        )
        
        self.group1 = Group.objects.create(
            name = 'Testgroup 1',
            slug= 'tg1',
            description = '',
            capacity = 1,
            place = '',
            first_date = '2006-10-25',
            last_date = '2006-10-25',
            rhythm = 'we',
            starting_time = '10:10',
            ending_time = '10:10',
            course = self.course
        )
        
        self.group2 = Group.objects.create(
            name = 'Testgroup 2',
            slug= 'tg2',
            description = '',
            capacity = 1,
            place = '',
            first_date = '2006-10-25',
            last_date = '2006-10-25',
            rhythm = 'we',
            starting_time = '10:10',
            ending_time = '10:10',
            course = self.course
        )
        
        self.user1 = User.objects.create_user('john1', 'lennon1@thebeatles.com', 'john1password')
        self.user2 = User.objects.create_user('john2', 'lennon2@thebeatles.com', 'john2password')
    
    def delete_test_data(self):
        Semester.objects.all().delete()
        Course.objects.all().delete()
        Group.objects.all().delete()
        User.objects.all().delete()
        


class CourseTestCase(unittest.TestCase):
    def setUp(self):
        self.testadmin = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        
    def testName(self):
        self.assertEqual(self.testadmin.username, "john")


class ViewTestCase(unittest.TestCase, CoursesTestDataMixin):
    def setUp(self):
        self.client = Client()
        self.make_test_data()
    
    def tearDown(self):
        self.delete_test_data()
        
    def test_course_list(self):
        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, 200)
        
        self.client.login(username='john1', password='john1password')
        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, 200)
        
    def test_course_list_my(self):
        response = self.client.get('/courses/my/')
        self.assertEqual(response.status_code, 302)
        
        self.client.login(username='john1', password='john1password')
        response = self.client.get('/courses/my/')
        self.assertEqual(response.status_code, 200)
        
    def test_course_details(self):
        response = self.client.get('/courses/tk/')
        self.assertEqual(response.status_code, 302)
        
        self.client.login(username='john1', password='john1password')
        response = self.client.get('/courses/tk/')
        self.assertEqual(response.status_code, 200)
    
    def test_group_details(self):
        response = self.client.get('/courses/tk/tg1/')
        self.assertEqual(response.status_code, 302)
        
        self.client.login(username='john1', password='john1password')
        response = self.client.get('/courses/tk/tg1/')
        self.assertEqual(response.status_code, 200)
    
    def test_create_preferences(self):
        response = self.client.get('/courses/tk/preferences/')
        self.assertEqual(response.status_code, 302)
        
        self.client.login(username='john1', password='john1password')
        response = self.client.get('/courses/tk/preferences/')
        self.assertEqual(response.status_code, 200)

class RegistratorTestCase(unittest.TestCase, CoursesTestDataMixin):
    
    def setUp(self):
        self.make_test_data()
        
        self.registrator = Registrator()
        
    def tearDown(self):
        self.delete_test_data()
    
    def test_user_registration(self):
        registration, created = self.registrator.register_user_for_group(self.user1, self.group1)
        self.assertNotEqual(registration, None)
        self.assertTrue(created)
    
    def test_already_registered_for_group(self):
        registration1, created1 = self.registrator.register_user_for_group(self.user1, self.group1)
        self.assertNotEqual(registration1, None)
        self.assertTrue(created1)
        registration2, created2 = self.registrator.register_user_for_group(self.user1, self.group1)
        self.assertNotEqual(registration2, None)
        self.assertFalse(created2)
        
    def test_already_registered_for_course(self):
        registration1, created1 = self.registrator.register_user_for_group(self.user1, self.group1)
        self.assertTrue(created1)
        self.assertNotEqual(registration1, None)
        registration2, created2 = self.registrator.register_user_for_group(self.user1, self.group2)
        self.assertFalse(created2)
        self.assertNotEqual(registration2, None)
    
    def test_group_full_registration(self):
        registration1, created1 = self.registrator.register_user_for_group(self.user1, self.group1)
        self.assertTrue(created1)
        self.assertNotEqual(registration1, None)
        registration2, created2 = self.registrator.register_user_for_group(self.user2, self.group1)
        self.assertFalse(created2)
        self.assertEqual(registration2, None)


class CourseAllocationTestCase(unittest.TestCase):
    
    class MockPreference:
        def __init__(self, user_id, preference, group_id, group_capacity):
            self.user_id = user_id
            self.preference = preference
            self.group_id = group_id
            self.group_capacity = group_capacity
            
    preferences = [
        MockPreference(1, 1, 1, 2),
        MockPreference(1, 2, 2, 2),
        MockPreference(1, 3, 3, 2),
        MockPreference(1, 4, 4, 2),
        MockPreference(1, 5, 5, 2),
        MockPreference(2, 1, 1, 2),
        MockPreference(2, 2, 2, 2),
        MockPreference(2, 3, 3, 2),
        MockPreference(2, 4, 4, 2),
        MockPreference(2, 5, 5, 2),
        MockPreference(3, 1, 1, 2),
        MockPreference(3, 2, 2, 2),
        MockPreference(3, 3, 3, 2),
        MockPreference(3, 4, 4, 2),
        MockPreference(3, 5, 5, 2),
        MockPreference(4, 1, 1, 2),
        MockPreference(5, 1, 1, 2),
        MockPreference(6, 1, 1, 2),
        MockPreference(7, 1, 1, 2),

    ]

    def setUp(self):
        self.allocator = RandomCourseAllocator(list(self.preferences))
        self.allocation = self.allocator.get_allocation()
        pass
    
    def test_number_of_allocations(self):
        number_of_users = len(set([p.user_id for p in self.preferences]))
        self.assertEqual(len(self.allocation), number_of_users)
    
    def test_all_users_got_a_group(self):
        users = set([p.user_id for p in self.preferences])
        for user in users:
            self.assertTrue(user in self.allocation)
            
    def test_to_much_users(self):
        preferences = self.preferences + [
            self.MockPreference(8, 1, 1, 2),
            self.MockPreference(9, 1, 1, 2),
            self.MockPreference(10, 1, 1, 2),
            self.MockPreference(11, 1, 1, 2),
        ]
        allocator = RandomCourseAllocator(list(preferences))
        self.assertRaises(ValueError, allocator.get_allocation)
    