from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Order, OrderItem, CartItem
from products.models import Product
from .services import place_order


@login_required
def cart(request):
    items = CartItem.objects.filter(
        customer=request.user
    ).select_related("product")

    total = 0

    for item in items:
        item.item_total = item.quantity * item.product.selling_price
        total += item.item_total

    return render(
        request,
        "cart.html",
        {
            "items": items,
            "total": total,
        },
    )


@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        messages.error(request, "Invalid quantity.")
        return redirect("product_details", product_id)

    if quantity < 1:
        messages.error(request, "Quantity must be at least 1.")
        return redirect("product_details", product_id)

    cart_item, created = CartItem.objects.get_or_create(
        customer=request.user,
        product=product,
        defaults={"quantity": quantity},
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save(update_fields=["quantity"])

    messages.success(request, f"{product.name} added to your cart.")
    return redirect("cart")


@login_required
@require_POST
def update_cart(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        customer=request.user,
    )

    try:
        quantity = int(request.POST.get("quantity"))
    except (TypeError, ValueError):
        messages.error(request, "Invalid quantity.")
        return redirect("cart")

    if quantity < 1:
        item.delete()
        messages.success(request, "Item removed from your cart.")
    else:
        item.quantity = quantity
        item.save(update_fields=["quantity"])
        messages.success(request, "Cart updated.")

    return redirect("cart")


@login_required
@require_POST
def remove_from_cart(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        customer=request.user,
    )

    item.delete()

    messages.success(request, "Item removed from your cart.")
    return redirect("cart")


@login_required
def checkout(request):
    if request.method == "POST":
        try:
            order = place_order(request.user)
        except ValueError as e:
            items = CartItem.objects.filter(
                customer=request.user
            ).select_related("product")

            total = 0

            for item in items:
                item.item_total = item.quantity * item.product.selling_price
                total += item.item_total

            return render(
                request,
                "cart.html",
                {
                    "items": items,
                    "total": total,
                    "error": str(e),
                },
            )

        messages.success(request, "Your order has been placed successfully.")
        return redirect("order_success", order_id=order.id)

    return render(request, "checkout.html")


@login_required
def order_success(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user,
    )

    return render(
        request,
        "order_success.html",
        {
            "order": order,
        },
    )


@login_required
def order_history(request):
    orders = (
        Order.objects
        .filter(customer=request.user)
        .order_by("-created_at")
    )

    return render(
        request,
        "order_history.html",
        {
            "orders": orders,
        },
    )


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user,
    )

    items = (
        order.orderitem_set
        .select_related("product")
        .all()
    )

    for item in items:
        item.item_total = item.quantity * item.price

    return render(
        request,
        "order_detail.html",
        {
            "order": order,
            "items": items,
        },
    )


@login_required
@permission_required("orders.view_order", raise_exception=True)
def staff_order_list(request):
    orders = (
        Order.objects
        .select_related("customer")
        .order_by("-created_at")
    )

    return render(
        request,
        "staff_order_list.html",
        {
            "orders": orders,
        },
    )


@login_required
@permission_required("orders.change_order", raise_exception=True)
def staff_order_update(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    allowed_transitions = {
        "PENDING": ["CONFIRMED", "CANCELLED"],
        "CONFIRMED": ["PROCESSING", "CANCELLED"],
        "PROCESSING": ["SHIPPED", "CANCELLED"],
        "SHIPPED": ["DELIVERED"],
        "DELIVERED": [],
        "CANCELLED": [],
    }

    valid_next_statuses = allowed_transitions.get(order.status, [])

    if request.method == "POST":
        new_status = request.POST.get("status")

        if new_status not in valid_next_statuses:
            messages.error(
                request,
                f"Cannot change order from {order.status} to {new_status}.",
            )
            return redirect(
                "staff_order_update",
                order_id=order.id,
            )

        order.status = new_status
        order.save(update_fields=["status", "updated_at"])

        messages.success(
            request,
            f"Order #{order.id} status updated to {new_status}.",
        )

        return redirect("staff_order_list")

    return render(
        request,
        "staff_order_update.html",
        {
            "order": order,
            "valid_next_statuses": valid_next_statuses,
        },
    )