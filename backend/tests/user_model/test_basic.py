from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status  # noqa: F401
from core.permissions import is_in_group

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('token_obtain_pair')
EDIT_USER_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_superuser(**params):
    return get_user_model().objects.create_superuser(**params)


class CustomUserModelTests(TestCase):
    """Test UserManager in user models functions."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email="foo@test.com", password='testpassword')
        self.superuser = create_superuser(email="test@test.com", password="testpassword")

    def test_user_create(self):
        """Test that create_user function works"""
        self.assertEqual(self.user.email, 'foo@test.com')

    def test_create_super_user(self):
        """Test that create_superuser function works"""
        self.assertEqual(self.superuser.is_superuser, True)

    def test_createsuperuser_in_groups(self):
        """Test that created superuser is in admin and member groups"""
        admin_group = Group.objects.get(name="admin").user_set.filter(id=self.superuser.id).exists()
        member_group = Group.objects.get(name="member").user_set.filter(id=self.superuser.id).exists()
        self.assertTrue(member_group)
        self.assertTrue(admin_group)


class PermissionsTests(TestCase):
    """Set of tests for custom permission functions"""

    def setUp(self):
        self.client = APIClient()
        self.superuser = create_superuser(email="test@test.com", password="testpassword")

    def test_user_permission(self):
        """Test that user in a group is detected as such"""
        payload = {
            'email': 'foo@test.com',
            'password': 'testpassword',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(**res.data)
        check_group = is_in_group(user, "member")
        self.assertTrue(check_group)
