from django.db import models
from accounts.models import CustomUser
from products.models import Product
from django.utils import timezone

class Order(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.JSONField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order {self.id} by {self.client.username}"
