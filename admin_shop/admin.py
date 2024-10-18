# from django.contrib.admin import AdminSite
# from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin

# class CustomAdminSite(AdminSite):
#     def has_permission(self, request):
#         return request.user.is_active

# class CustomUserAdmin(UserAdmin):
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if not request.user.is_superuser:
#             return qs.filter(id=request.user.id)
#         return qs

# custom_admin_site = CustomAdminSite(name='customadmin')
# custom_admin_site.register(User, CustomUserAdmin)
