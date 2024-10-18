import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Order
from products.models import Product

@pytest.mark.django_db
class TestOrderModel:
    @pytest.fixture
    def user(self, create_groups):
        User = get_user_model()
        return User.objects.create_user('testuser', 'test@example.com', 'testpass123')

    @pytest.fixture
    def product(self):
        return Product.objects.create(name='Test Product', description='Test', price=9.99, stock=10)

    def test_order_creation(self, user, product):
        order = Order.objects.create(
            client=user,
            total=19.98,
            products=[{'product_id': product.id, 'quantity': 2}]
        )
        assert str(order) == f"Order {order.id} by testuser"
        assert order.total == 19.98

@pytest.mark.django_db
class TestOrderViewSet:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def user(self, create_groups):
        User = get_user_model()
        return User.objects.create_user('testuser', 'test@example.com', 'testpass123')

    @pytest.fixture
    def product(self):
        return Product.objects.create(name='Test Product', description='Test', price=9.99, stock=10)

    @pytest.fixture
    def order_data(self, product):
        return {
            'products': [{'product_id': product.id, 'quantity': 2}]
        }

    def test_create_order(self, api_client, user, product, order_data):
        api_client.force_authenticate(user=user)
        response = api_client.post('/api/orders/', order_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Order.objects.count() == 1
        product.refresh_from_db()
        assert product.stock == 8

    def test_create_order_insufficient_stock(self, api_client, user, product, order_data):
        api_client.force_authenticate(user=user)
        order_data['products'][0]['quantity'] = 15
        response = api_client.post('/api/orders/', order_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Order.objects.count() == 0
        product.refresh_from_db()
        assert product.stock == 10

    def test_list_user_orders(self, api_client, user, product):
        api_client.force_authenticate(user=user)
        Order.objects.create(client=user, total=19.98, products=[{'product_id': product.id, 'quantity': 2}])
        response = api_client.get('/api/orders/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

@pytest.mark.django_db
class TestOrderSerializer:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        User = get_user_model()
        return User.objects.create_user('testuser', 'test@example.com', 'testpass123')

    @pytest.fixture
    def product(self):
        return Product.objects.create(name='Test Product', description='Test', price=10, stock=10)

    def test_order_serializer_create(self, api_client, user, product):
        api_client.force_authenticate(user=user)
        order_data = {
            'products': [{'product_id': product.id, 'quantity': 2}]
        }
        response = api_client.post('/api/orders/', order_data, format='json')
        print('response', response.data)
        assert response.status_code == status.HTTP_201_CREATED
        order = Order.objects.get(id=response.data['id'])
        assert order.total == 20
        product.refresh_from_db()
        assert product.stock == 8
