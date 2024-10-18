import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

# Create your tests here.

@pytest.mark.django_db
class TestCustomUserModel:
    def test_create_client(self):
        User = get_user_model()
        client = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        assert client.username == 'testuser'
        assert client.email == 'test@example.com'
        assert client.is_active
        assert client.is_staff    #because of admin implementations, all clients are staff
        assert not client.is_superuser
        assert client.user_type == 1  # Regular user
        assert client.groups.filter(name='Regular User').exists()

    def test_create_superuser(self):
        User = get_user_model()
        super_user = User.objects.create_superuser(username='super', email='super@example.com', password='superpass123')
        assert super_user.username == 'super'
        assert super_user.email == 'super@example.com'
        assert super_user.is_active
        assert super_user.is_staff
        assert super_user.is_superuser
        assert super_user.user_type == 1  # In superusers user_type is 1 by default
        assert super_user.groups.filter(name='Regular User').exists()

    def test_create_admin(self):
        User = get_user_model()
        admin = User.objects.create_user(username='admin', email='admin@example.com', password='adminpass123', 
                                         user_type=2)
        assert admin.username == 'admin'
        assert admin.email == 'admin@example.com'
        assert admin.is_active
        assert admin.is_staff
        assert not admin.is_superuser
        assert admin.user_type == 2  
        assert admin.groups.filter(name='Admin').exists()

    def test_user_is_admin_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        admin_user = User.objects.create_user(username='adminuser', email='admin@example.com', password='adminpass123', user_type=2)
        assert not user.is_admin_user()
        assert admin_user.is_admin_user()

@pytest.mark.django_db
def test_groups_exist():
    assert Group.objects.filter(name='Admin').exists()
    assert Group.objects.filter(name='Regular User').exists()

@pytest.mark.django_db
class TestUserSignal:
    def test_user_assigned_to_group_on_creation(self):
        User = get_user_model()
        regular_user = User.objects.create_user(username='regular', email='regular@example.com', password='regularpass123')
        admin_user = User.objects.create_user(username='admin', email='admin@example.com', password='adminpass123', user_type=2)

        assert regular_user.groups.filter(name='Regular User').exists()
        assert admin_user.groups.filter(name='Admin').exists()
