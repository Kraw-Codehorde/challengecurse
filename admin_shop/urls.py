from django.urls import path, include
from accounts.admin import custom_admin_site

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('api/', include('products.urls')),  
    path('api/', include('orders.urls')),  
]
