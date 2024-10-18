import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product

# Create your tests here.

@pytest.mark.django_db
class TestProductModel:
    def test_product_creation(self):
        product = Product.objects.create(
            name='Test Product',
            description='This is a test product',
            price=9.99,
            stock=10
        )
        assert str(product) == 'Test Product'
        assert product.stock == 10

    def test_has_stock_method(self):
        product = Product.objects.create(
            name='Test Product',
            description='This is a test product',
            price=9.99,
            stock=5
        )
        assert product.has_stock(3)
        assert not product.has_stock(6)

@pytest.mark.django_db
class TestProductViewSet:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def admin_user(self):
        User = get_user_model()
        return User.objects.create_user('admin', 'admin@example.com', 'adminpass123', user_type=2)

    @pytest.fixture
    def regular_user(self):
        User = get_user_model()
        return User.objects.create_user('regular', 'regular@example.com', 'regularpass123')

    @pytest.fixture
    def product_data(self):
        return {
            'name': 'New Product',
            'description': 'A new test product',
            'price': 19.99,
            'stock': 50
        }

    def test_create_product_as_admin(self, api_client, admin_user, product_data):
        api_client.force_authenticate(user=admin_user)
        response = api_client.post('/api/products/', product_data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_product_as_regular_user(self, api_client, regular_user, product_data):
        api_client.force_authenticate(user=regular_user)
        response = api_client.post('/api/products/', product_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_products(self, api_client, regular_user):
        Product.objects.create(name='Test Product', description='Test', price=9.99, stock=10)
        api_client.force_authenticate(user=regular_user)
        response = api_client.get('/api/products/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

@pytest.mark.django_db
class TestProductPermission:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def admin_user(self):
        User = get_user_model()
        return User.objects.create_user('admin', 'admin@example.com', 'adminpass123', user_type=2)

    @pytest.fixture
    def regular_user(self):
        User = get_user_model()
        return User.objects.create_user('regular', 'regular@example.com', 'regularpass123')

    @pytest.fixture
    def product(self):
        return Product.objects.create(name='Test Product', description='Test', price=9.99, stock=10)

    def test_update_product_as_admin(self, api_client, admin_user, product):
        api_client.force_authenticate(user=admin_user)
        response = api_client.patch(f'/api/products/{product.id}/', {'price': 15})
        assert response.status_code == status.HTTP_200_OK
        product.refresh_from_db()
        assert product.price == 15

    def test_update_product_as_regular_user(self, api_client, regular_user, product):
        api_client.force_authenticate(user=regular_user)
        response = api_client.patch(f'/api/products/{product.id}/', {'price': 14.99})
        assert response.status_code == status.HTTP_403_FORBIDDEN
