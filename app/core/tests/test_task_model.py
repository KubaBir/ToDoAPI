from core import models
from django.contrib.auth import get_user_model
from django.test import TestCase


class TestTasks(TestCase):

    def test_task_create(self):
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )

        task = models.Task.objects.create(
            user=user,
            name='test123',
            remaining_time=3,
            description='example'
        )
        self.assertEqual(task.name, str(task))

    def test_task_owned_by(self):
        user1 = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )
        user2 = get_user_model().objects.create_user(
            'test1@example.com',
            'testpass1234'
        )
        models.Task.objects.create(
            user=user1,
            name='test123',
            remaining_time=3,
            description='example'
        )
        models.Task.objects.create(
            user=user2,
            name='wrong',
            remaining_time=3,
            description='example'
        )
        res = models.Task.objects.filter(user=user1)
        self.assertEqual(len(res), 1)
