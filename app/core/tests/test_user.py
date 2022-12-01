from core import models
from django.contrib.auth import get_user_model
from django.test import TestCase


def create_user(email='user@example.com', password='testpass123'):
    return get_user_model().objects.create_user(email, password)


class UserTests(TestCase):

    def test_create_user_success(self):
        email = 'user@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create(
            email=email,
            password=password
        )
        self.assertEqual(email, user.email)
        self.assertEqual(password, user.password)

    def test_no_email_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')
