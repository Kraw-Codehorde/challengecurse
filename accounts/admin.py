from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.urls import path
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.contrib.admin.models import LogEntry

from products.models import Product
from products.admin import ProductAdmin
from orders.models import Order
from orders.admin import OrderAdmin

class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_view(self.index), name='index'),
            path('history/', self.admin_view(self.order_history_view), name='history'),
            path('shop/', self.admin_view(self.shop_view), name='shop'),
        ]
        return custom_urls + urls

    def has_permission(self, request):
        return request.user.is_authenticated

    def index(self, request, extra_context=None):
        # Default context variables
        log_entries = LogEntry.objects.all()  # Get log entries if needed
        has_permission = self.has_permission(request)

        if request.user.is_superuser:
            # Load the standard Django admin index for superusers
            return super().index(request, extra_context=extra_context)

        # For admin and regular users, provide custom context
        if request.user.is_admin_user():  
            extra_context = {
                'title': 'Admin User Dashboard',
                'message': 'Welcome, Admin User! You have limited access.',
                'is_admin': True,
                'log_entries': log_entries,
                'has_permission': has_permission,
            }
            return TemplateResponse(request, 'admin/admin_dashboard.html', extra_context)
        else:
            extra_context = {
                'title': 'User Dashboard',
                'is_admin': False,
                'log_entries': log_entries,
                'has_permission': has_permission,
            }

        # Render the default admin index but with custom context
        return TemplateResponse(request, 'admin/regular_dashboard.html', extra_context)
    
    def order_history_view(self, request):
        user_orders = Order.objects.filter(client=request.user)
        context = {
            'user_orders': user_orders,
        }
        return TemplateResponse(request, 'admin/order_history.html', context)
    
    def shop_view(self, request):
        products = Product.objects.all()
        context = {
            'products': products,
        }
        return TemplateResponse(request, 'admin/products_shop.html', context)


custom_admin_site = CustomAdminSite(name='custom_admin')

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'user_type', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type',)}),
    )

custom_admin_site.register(CustomUser, CustomUserAdmin)


custom_admin_site.register(Product, ProductAdmin)


custom_admin_site.register(Order, OrderAdmin)
