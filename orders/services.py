from django.db import transaction

from products.models import Inventory
from .models import Order, OrderItem, CartItem

def place_order(customer):
    with transaction.atomic():
        cart_items = CartItem.objects.filter(customer=customer).select_related("product")

        if not cart_items.exists():
            raise ValueError("Cart is empty")

        total = 0
        order = Order.objects.create(customer=customer,status="PENDING",total_amount=0)

        for cart_item in cart_items:
            product = cart_item.product

            inventory = Inventory.objects.select_for_update().get(product=product)

            stock = inventory.stock_quantity
            quantity = cart_item.quantity

            if quantity > stock:
                raise ValueError(f"Not enough stock for {product.name}")

            price = product.selling_price
            item_total = quantity * price

            OrderItem.objects.create(order=order,product=product,quantity=quantity,price=price)

            inventory.stock_quantity = stock - quantity
            inventory.save()

            total += item_total
        order.total_amount = total
        order.save()
        cart_items.delete()
    return order