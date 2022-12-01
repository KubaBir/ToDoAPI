from core.models import Task
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from tasks.serializers import TaskSerializer

TASKS_URL = reverse('tasks:task-list')


def create_task(user, **params):
    defaults = {
        'name': 'Sample title',
        'remaining_time': 22,
        'description': 'Sample description',
    }
    defaults.update(params)
    task = Task.objects.create(user=user, **defaults)
    return task


class PrivateAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_tasks(self):
        create_task(user=self.user)
        create_task(user=self.user)
        other_user = get_user_model().objects.create_user(
            email='other_user@example.com',
            password='testpass123'
        )
        create_task(user=other_user, name='essa')
        res = self.client.get(TASKS_URL)
        tasks = Task.objects.filter(user=self.user)
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)
