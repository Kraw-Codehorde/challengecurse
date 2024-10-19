from rest_framework import viewsets
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from .tasks import process_order

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        client = request.user
        products_data = request.data.get('products', [])
        
        order_data = {
            'client': client.id,
            'products': products_data,
        }
        
        serializer = self.get_serializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # Asynchronously process the order
        process_order.delay(order.id)
        
        return Response(serializer.data, status=201)
