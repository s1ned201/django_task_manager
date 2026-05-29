from django.test import TestCase
from account.models import User
from task_manager.forms import TaskForm, UserCreateForm


class TestTaskForm(TestCase):

    def setUp(self):
        self.valid_task_data = {
            'name': 'Тестовая задача',
            'description': 'Это описание тестовой задачи',
            'priority': 10,
            'status': 'CREATED'
        }

    def test_valid_task_form(self):
        form = TaskForm(data=self.valid_task_data)
        self.assertTrue(form.is_valid())

    def test_empty_name_field(self):
        invalid_data = self.valid_task_data.copy()
        invalid_data['name'] = ''
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_high_priority_with_valid_description(self):
        valid_data = self.valid_task_data.copy()
        valid_data['priority'] = 8
        valid_data['description'] = 'Важное описание для задачи высокого приоритета'
        form = TaskForm(data=valid_data)
        self.assertTrue(form.is_valid())

    def test_priority_range_validation(self):
        invalid_data = self.valid_task_data.copy()
        invalid_data['priority'] = 0
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_priority_boundary_values(self):
        valid_data = self.valid_task_data.copy()
        valid_data['priority'] = 1
        valid_data['description'] = 'Описание для минимального приоритета'
        form = TaskForm(data=valid_data)
        self.assertTrue(form.is_valid())
        valid_data['priority'] = 10
        valid_data['description'] = 'Описание для максимального приоритета'
        form = TaskForm(data=valid_data)
        self.assertTrue(form.is_valid())

    def test_empty_description_low_priority(self):
        valid_data = self.valid_task_data.copy()
        valid_data['priority'] = 3
        valid_data['description'] = ''
        form = TaskForm(data=valid_data)
        self.assertTrue(form.is_valid())

    def test_status_field_choices(self):
        valid_data = self.valid_task_data.copy()
        valid_data['status'] = 'CREATED'
        form = TaskForm(data=valid_data)
        self.assertTrue(form.is_valid())
        invalid_data = self.valid_task_data.copy()
        invalid_data['status'] = 'invalid_status'
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())


class TestUserCreateForm(TestCase):

    def setUp(self):
        self.valid_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password_confirm': 'password123',
            'first_name': 'Тест',
            'last_name': 'Пользователь',
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
        }

    def test_valid_user_form(self):
        form = UserCreateForm(data=self.valid_user_data)
        self.assertTrue(form.is_valid())

    def test_username_required(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data['username'] = ''
        form = UserCreateForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_username_unique_validation(self):
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='pass123'
        )
        invalid_data = self.valid_user_data.copy()
        invalid_data['username'] = 'existinguser'
        form = UserCreateForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_email_required(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data['email'] = ''
        form = UserCreateForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_email_format_validation(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data['email'] = 'invalid-email'
        form = UserCreateForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_email_unique_validation(self):
        User.objects.create_user(
            username='user1',
            email='existing@example.com',
            password='pass123'
        )
        invalid_data = self.valid_user_data.copy()
        invalid_data['email'] = 'existing@example.com'
        form = UserCreateForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_password_minimum_length(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data['password'] = '1234567'
        invalid_data['password_confirm'] = '1234567'
        form = UserCreateForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

    def test_password_minimum_length_exactly_8(self):
        valid_data = self.valid_user_data.copy()
        valid_data['password'] = '12345678'
        valid_data['password_confirm'] = '12345678'
        form = UserCreateForm(data=valid_data)
        self.assertTrue(form.is_valid())

    def test_password_required(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data['password'] = ''
        form = UserCreateForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_password_confirm_required(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data['password_confirm'] = ''
        form = UserCreateForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password_confirm', form.errors)
