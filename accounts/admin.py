from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.urls import path
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.contrib.admin.models import LogEntry
from django.utils.translation import gettext as _

from products.models import Product
from products.admin import ProductAdmin
from orders.models import Order
from orders.admin import OrderAdmin

class CustomAdminSite(admin.AdminSite):
    """
    ALL the logic for the custom admin site views is here. 
    TODO: probably move it to separate files, so it doesn't get so messy.
    """
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_view(self.index), name='index'),
            path('history/', self.admin_view(self.order_history_view), name='history'),
            path('shop/', self.admin_view(self.shop_view), name='shop'),
            path('history/<int:pk>/', self.admin_view(self.order_details_view), name='order_details'),
        ]
        return custom_urls + urls

    def has_permission(self, request):
        return request.user.is_authenticated

    def index(self, request, extra_context=None):
        log_entries = LogEntry.objects.all()  # log entries are needed!!!
        
        # Load the standard Django admin index for superusers, with all powers
        if request.user.is_superuser:
            return super().index(request, extra_context=extra_context)

        # For admin and regular users, provide custom context
        if request.user.is_admin_user():  
            extra_context = {
                'title': 'Admin User Dashboard',
                'log_entries': log_entries, # log entries are needed, if not error.
                # has_permission is needed to display correct Header in the template.
                'has_permission': self.has_permission(request), 
            }
            return TemplateResponse(request, 'admin/admin_dashboard.html', extra_context)
        # For regular users
        else:
            extra_context = {
                'title': 'User Dashboard',
                'log_entries': log_entries, # log entries are needed, if not error.
                'has_permission': self.has_permission(request), #IMPORTANT!
            }

        # Render the default admin index but with custom context
        return TemplateResponse(request, 'admin/regular_dashboard.html', extra_context)
    
    def order_history_view(self, request, extra_context=None):
        user_orders = Order.objects.filter(client=request.user)
        context = {
            **self.each_context(request),
            'title': _('Order History'),
            'subtitle': None,
            'app_label': 'orders',  
            'user_orders': user_orders,
            'has_permission': self.has_permission(request), #IMPORTANT!
        }
        context.update(extra_context or {})
        return TemplateResponse(request, 'admin/order_history.html', context)
    
    def order_details_view(self, request, pk, extra_context=None):
        order = Order.objects.get(pk=pk, client=request.user)
        context = {
            **self.each_context(request),
            'order': order, #TODO: handle case when order is not found.
        }
        return TemplateResponse(request, 'admin/order_details.html', context)
    
    def shop_view(self, request, extra_context=None):
        # products = Product.objects.all()
        context = {
            **self.each_context(request),
            'title': _('Shop'),
            'subtitle': None,
            'app_label': 'products',  
            # 'products': products,   # fetching is done through api atm.
            'has_permission': self.has_permission(request),
        }
        context.update(extra_context or {})
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
