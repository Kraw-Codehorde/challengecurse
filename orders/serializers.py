from rest_framework import serializers
from django.db import transaction
from .models import Order, Product

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['client', 'products', 'total', 'date']

    def create(self, validated_data):
        products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        
        with transaction.atomic():
            for product_data in products:
                product = Product.objects.get(id=product_data['product_id'])
                amount = product_data['quantity']

                if product.stock >= amount:
                    product.stock -= amount  # Deduct stock
                    product.save()           
                else:
                    raise serializers.ValidationError(f"Not enough stock for {product.name}")
            print('PRODUCTS TO BE', products)
            order.products = products
            order.save()

        return order
