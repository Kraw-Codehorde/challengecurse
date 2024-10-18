from django.urls import path, include
from accounts.admin import custom_admin_site

# Accounts are handled in the admin site for the time being.
urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('api/', include('products.urls')),  
    path('api/', include('orders.urls')),  
]
