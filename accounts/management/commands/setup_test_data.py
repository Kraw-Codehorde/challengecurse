from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates test users and products'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test users...')
        
        # Create superuser
        if not User.objects.filter(username='super').exists():
            User.objects.create_superuser('super', 'super@example.com', 'super')
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user('admin', 'admin@example.com', 'admin')
            admin_user.user_type = 2  # Set as admin
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Admin user created successfully'))
        
        # Create client user
        if not User.objects.filter(username='client').exists():
            User.objects.create_user('client', 'client@example.com', 'client')
            self.stdout.write(self.style.SUCCESS('Client user created successfully'))
        
        self.stdout.write('Creating mock products...')
        
        # Create mock products
        products = [
            {'name': 'Laptop', 'description': 'High-performance laptop', 'price': 1000, 'stock': 10},
            {'name': 'Smartphone', 'description': 'Latest model smartphone', 'price': 700, 'stock': 20},
            {'name': 'Headphones', 'description': 'Noise-cancelling headphones', 'price': 200, 'stock': 30},
            {'name': 'Tablet', 'description': '10-inch tablet', 'price': 300, 'stock': 15},
            {'name': 'Smartwatch', 'description': 'Fitness tracking smartwatch', 'price': 150, 'stock': 25},
        ]
        
        for product_data in products:
            Product.objects.get_or_create(name=product_data['name'], defaults=product_data)
        
        self.stdout.write(self.style.SUCCESS('Mock products created successfully'))
