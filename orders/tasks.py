from celery import shared_task
from django.db import transaction
from .models import Order
from products.models import Product

@shared_task
def process_order(order_id):
    order = Order.objects.get(id=order_id)
    products_data = order.products

    with transaction.atomic():
        total = 0
        for product_data in products_data:
            product = Product.objects.select_for_update().get(id=product_data['product_id'])
            amount = product_data['quantity']

            if product.stock < amount:
                order.status = 'failed'
                order.save()
                return f"Not enough stock for {product.name}"

            product.stock -= amount
            product.save()

            total += product.price * amount

        order.total = total
        order.status = 'completed'
        order.save()

    return f"Order {order_id} processed successfully"
