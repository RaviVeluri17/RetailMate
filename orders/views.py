from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Order,OrderItem,CartItem
from products.models import Product
# Create your views here.

@login_required
@login_required
def cart(request):
    items = CartItem.objects.filter(customer=request.user).select_related("product")
    total = 0
    for item in items:
        item.item_total = item.quantity * item.product.selling_price
        total+=item.item_total

    return render(request,"cart.html",{"items": items,"total": total})

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    quantity = int(request.POST.get("quantity", 1))
    cart_item, created = CartItem.objects.get_or_create(customer=request.user,product=product,defaults={"quantity": quantity})

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return redirect("cart")

@login_required
def update_cart(request, item_id):
    item = CartItem.objects.get(id=item_id,customer=request.user)
    quantity = int(request.POST.get("quantity"))

    if quantity < 1:
        item.delete()
    else:
        item.quantity = quantity
        item.save()
    return redirect("cart")

@login_required
def remove_from_cart(request, item_id):
    item = CartItem.objects.get(id=item_id,customer=request.user)
    item.delete()
    return redirect("cart")