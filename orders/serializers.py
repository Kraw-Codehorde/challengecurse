from rest_framework import serializers
from django.db import transaction
from .models import Order, Product

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'client', 'products', 'total', 'date']

    def create(self, validated_data):
        products = validated_data.pop('products')

        # Check stock availability before creating the order
        for product_data in products:
            product = Product.objects.get(id=product_data['product_id'])
            amount = product_data['quantity']

            if product.stock < amount:
                raise serializers.ValidationError(f"Not enough stock for {product.name}")
        
        with transaction.atomic():
            # Now that stock is validated, create the order
            order = Order.objects.create(**validated_data)
            
            for product_data in products:
                product = Product.objects.get(id=product_data['product_id'])
                amount = product_data['quantity']
                
                product.stock -= amount  # Deduct stock
                product.save()

            order.products = products  # Assign the products to the order
            order.save()

        return order
