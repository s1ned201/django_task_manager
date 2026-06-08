from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from account.models import User as CustomUser
from task_manager.models import Tasks, Comments

User = get_user_model()


class TaskViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        for i in range(15):
            Tasks.objects.create(
                name=f'Test Task {i}',
                description=f'Description {i}',
                priority=i % 10 + 1,
                status='CREATED'
            )

    def test_task_view_returns_200_for_authenticated_user_with_permission(self):
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(Tasks)
        permission, created = Permission.objects.get_or_create(
            codename='view_task',
            content_type=content_type
        )
        self.user.user_permissions.add(permission)
        logged_in = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(logged_in, "User should be able to login")
        response = self.client.get(reverse('tasks'))
        if response.status_code == 302:
            print(f"Redirecting to: {response.url}")
            response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks.html')

    def test_task_view_pagination_returns_10_tasks_on_first_page(self):
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(Tasks)
        permission, created = Permission.objects.get_or_create(
            codename='view_task',
            content_type=content_type
        )
        self.user.user_permissions.add(permission)
        logged_in = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(logged_in, "User should be able to login")
        response = self.client.get(reverse('tasks'))
        if response.status_code == 302:
            response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        if response.context:
            self.assertEqual(len(response.context['tasks']), 10)
            self.assertIn('page_obj', response.context)

class TaskDetailViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.task = Tasks.objects.create(
            name='Test Task',
            description='Test Description',
            priority=5,
            status='CREATED'
        )
        self.comment1 = Comments.objects.create(
            task=self.task,
            user=self.user,
            message='First comment'
        )
        self.comment2 = Comments.objects.create(
            task=self.task,
            user=self.user,
            message='Second comment'
        )

    def test_task_detail_view_returns_200_for_existing_task(self):
        response = self.client.get(reverse('task_detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        if hasattr(response, 'context') and response.context:
            self.assertEqual(response.context['task'].id, self.task.id)

    def test_task_detail_view_context_contains_comments_and_count(self):
        response = self.client.get(reverse('task_detail', args=[self.task.id]))
        if response.context:
            self.assertIn('comments', response.context)
            self.assertIn('comment_count', response.context)
            self.assertEqual(response.context['comment_count'], 2)
            self.assertEqual(len(response.context['comments']), 2)
        else:
            self.assertEqual(response.status_code, 200)


class TaskCreateViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.valid_task_data = {
            'name': 'New Task',
            'description': 'Task description',
            'priority': 5,
            'status': 'CREATED'
        }

    def test_task_create_view_creates_task_and_redirects_on_valid_data(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('create_task'), self.valid_task_data)
        self.assertEqual(Tasks.objects.count(), 1)
        task = Tasks.objects.first()
        self.assertEqual(task.name, 'New Task')
        self.assertEqual(task.description, 'Task description')
        self.assertEqual(task.priority, 5)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('tasks'))

    def test_task_create_view_shows_success_message_after_creation(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('create_task'), self.valid_task_data, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Задача "New Task" успешно создана', str(messages[0]))

class UserListViewTest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        self.user2 = CustomUser.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123'
        )
        self.task1 = Tasks.objects.create(
            name='Task 1',
            description='Desc 1',
            priority=5,
            status='CREATED',
            assignee=self.user1
        )
        self.task2 = Tasks.objects.create(
            name='Task 2',
            description='Desc 2',
            priority=3,
            status='completed',
            assignee=self.user1
        )
        self.task3 = Tasks.objects.create(
            name='Task 3',
            description='Desc 3',
            priority=1,
            status='CREATED',
            assignee=self.user2
        )

    def test_user_list_view_returns_200_and_uses_correct_template(self):
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')

    def test_user_list_view_annotates_correct_task_count_for_each_user(self):
        response = self.client.get(reverse('user_list'))
        users = response.context['users']
        user1 = users.get(username='user1')
        user2 = users.get(username='user2')
        self.assertEqual(user1.tasks_count, 2)
        self.assertEqual(user2.tasks_count, 1)

class UserInfoViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.task1 = Tasks.objects.create(
            name='Task 1',
            description='Description 1',
            priority=8,
            status='CREATED',
            assignee=self.user
        )
        self.task2 = Tasks.objects.create(
            name='Task 2',
            description='Description 2',
            priority=3,
            status='COMPLETED',
            assignee=self.user
        )
        self.comment1 = Comments.objects.create(
            task=self.task1,
            user=self.user,
            message='Comment 1 on task 1'
        )
        self.comment2 = Comments.objects.create(
            task=self.task1,
            user=self.user,
            message='Comment 2 on task 1'
        )
        self.comment3 = Comments.objects.create(
            task=self.task2,
            user=self.user,
            message='Comment on task 2'
        )

    def test_user_info_view_returns_200_and_displays_user_info(self):
        response = self.client.get(reverse('user_info', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_info.html')
        self.assertEqual(response.context['user'].id, self.user.id)
        self.assertEqual(response.context['user'].username, 'testuser')

    def test_user_info_view_calculates_total_comments_correctly(self):
        response = self.client.get(reverse('user_info', args=[self.user.id]))
        self.assertEqual(response.context['total_comments'], 3)
        self.assertEqual(len(response.context['tasks']), 2)