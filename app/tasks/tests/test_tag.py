from core.models import Tag, Task
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from tasks import urls
from tasks.serializers import TagSerializer

TAG_URL = reverse('tasks:tag-list')


def create_user(email='user@example.com', password='testpass123'):
    return get_user_model().objects.create_user(email=email, password=password)


class PublicTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_get_tags(self):
        Tag.objects.create(user=self.user, name='a1')
        Tag.objects.create(user=self.user, name='a2')
        res = self.client.get(TAG_URL)
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_users_tags(self):
        other_user = create_user(email='other_user@example.com')
        tag = Tag.objects.create(user=self.user, name='a1')
        Tag.objects.create(user=other_user, name='b1')

        res = self.client.get(TAG_URL)
        tags = Tag.objects.filter(user=self.user)
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.data[0]['name'], tag.name)
