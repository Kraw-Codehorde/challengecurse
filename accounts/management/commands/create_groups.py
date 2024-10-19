from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from products.models import Product  # Adjust import based on your app structure

class Command(BaseCommand):
    help = 'Creates default groups and permissions'

    def handle(self, *args, **options):
        # Create admin group
        admin_group, admin_created = Group.objects.get_or_create(name='Admin')
        
        # Create regular user group
        regular_group, regular_created = Group.objects.get_or_create(name='Regular User')

        # Define permissions for admin
        product_content_type = ContentType.objects.get_for_model(Product)
        
        add_product_permission = Permission.objects.get(
            codename='add_product',
            content_type=product_content_type,
        )
        change_product_permission = Permission.objects.get(
            codename='change_product',
            content_type=product_content_type,
        )
        delete_product_permission = Permission.objects.get(
            codename='delete_product',
            content_type=product_content_type,
        )

        # Assign permissions to admin group
        admin_group.permissions.add(
            add_product_permission,
            change_product_permission,
            delete_product_permission
        )

        self.stdout.write(self.style.SUCCESS('Successfully created groups and assigned permissions'))

        # Assign admin group to users with user_type=2
        User = get_user_model()
        admin_users = User.objects.filter(user_type=2)
        for user in admin_users:
            user.groups.add(admin_group)
            user.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully assigned Admin group to {admin_users.count()} users'))
