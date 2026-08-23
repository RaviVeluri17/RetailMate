from django.db import models
from django.contrib.auth.models import User
from products.models import Product
# Create your models here.
class Order(models.Model):
    customer=models.ForeignKey(User,on_delete=models.PROTECT)
    choices=[
        ("PENDING","PENDING"),
        ("CONFIRMED","CONFIRMED"),
        ("PROCESSING","PROCESSING"),
        ("SHIPPED","SHIPPED"),
        ("DELIVERED","DELIVERED"),
        ("CANCELLED","CANCELLED")
    ]
    status=models.CharField(max_length=32,choices=choices)
    total_amount=models.DecimalField(max_digits=10,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)