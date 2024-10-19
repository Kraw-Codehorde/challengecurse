from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from products.models import Product

class Command(BaseCommand):
    help = 'Creates default groups and permissions'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating groups...')

        # Create Regular User group
        regular_user_group, created = Group.objects.get_or_create(name='Regular User')
        if created:
            self.stdout.write(self.style.SUCCESS('Regular User group created'))
        else:
            self.stdout.write('Regular User group already exists')

        # Create Admin group
        admin_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            self.stdout.write(self.style.SUCCESS('Admin group created'))
        else:
            self.stdout.write('Admin group already exists')

        # Get all permissions for the Product model
        product_content_type = ContentType.objects.get_for_model(Product)
        product_permissions = Permission.objects.filter(content_type=product_content_type)

        # Assign permissions to Admin group
        admin_group.permissions.add(*product_permissions)
        self.stdout.write(self.style.SUCCESS('Permissions assigned to Admin group'))

        self.stdout.write(self.style.SUCCESS('Groups and permissions setup completed'))
