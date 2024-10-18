from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import AdminOrSuperuserPermission
from accounts.models import CustomUser

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed by regular users/clients, 
    or edited by admins/superusers.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, AdminOrSuperuserPermission]
        return super().get_permissions()