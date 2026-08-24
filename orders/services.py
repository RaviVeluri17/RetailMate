from django.db import transaction

from products.models import Inventory
from .models import Order,OrderItem

def place_order(customer, product, quantity):
    with transaction.atomic():
        inventory = Inventory.objects.get(product=product)
        stock = inventory.stock_quantity
        if quantity > stock:
            raise ValueError("Quantity exceeds available stock")
    
        price = product.selling_price
        total = quantity * price
        order = Order.objects.create(customer=customer, status="PENDING", total_amount=total)
        OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
        inventory.stock_quantity = stock - quantity
        inventory.save()
    return order