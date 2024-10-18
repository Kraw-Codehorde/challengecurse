from rest_framework import viewsets
from rest_framework.response import Response
from .models import Order
from products.models import Product
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        client = request.user  
        products_data = request.data.get('products', [])
        
        total = sum(
            Product.objects.get(id=item['product_id']).price * item['quantity']
            for item in products_data
        )
        
        order_data = {
            'client': client.id,
            'products': products_data,
            'total': total
        }
        
        serializer = self.get_serializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=201)
