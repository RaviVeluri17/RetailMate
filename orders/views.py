from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from .models import Order,OrderItem,CartItem
from products.models import Product
from .services import place_order
from django.http import HttpResponse
# Create your views here.

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


@login_required
def checkout(request):
    if request.method == "POST":
        try:
            order = place_order(request.user)
        except ValueError as e:
            return render(request,"cart.html",{"error": str(e)})
        return redirect("order_success",order_id=order.id)
    return render(request,"checkout.html")

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order,id=order_id,customer=request.user)
    context={
        "order":order
    }
    return render(request,"order_success.html",context)

@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user).order_by("-created_at")
    context={
        "orders":orders
    }
    return render(request,"order_history.html",context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order,id=order_id,customer=request.user)
    items = order.orderitem_set.select_related("product").all()

    for item in items:
        item.item_total = item.quantity * item.price

    context={
        "order": order,
        "items": items
    }
    return render(request,"order_detail.html",context)

@login_required
@permission_required("orders.view_order",raise_exception=True)
def staff_order_list(request):
    orders = Order.objects.select_related("customer").order_by("-created_at")
    context={
        "orders":orders
    }
    return render(request, "staff_order_list.html",context)

@login_required
@permission_required("orders.change_order",raise_exception=True)
def staff_order_update(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        new_status = request.POST.get("status")
        allowed_transitions = {
            "PENDING": ["CONFIRMED", "CANCELLED"],
            "CONFIRMED": ["PROCESSING", "CANCELLED"],
            "PROCESSING": ["SHIPPED", "CANCELLED"],
            "SHIPPED": ["DELIVERED"],
            "DELIVERED": [],
            "CANCELLED": []
        }
        if new_status not in allowed_transitions[order.status]:
            return HttpResponse(f"Cannot change order from "f"{order.status} to {new_status}")
        order.status = new_status
        order.save()
        return HttpResponse("Order status updated successfully")
    context={
        "order":order
    }
    return render(request,"staff_order_update.html",context)