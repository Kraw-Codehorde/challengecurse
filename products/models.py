from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    def has_stock(self, amount):
        return self.stock >= amount