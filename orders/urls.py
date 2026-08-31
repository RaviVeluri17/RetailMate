from django.urls import path
from orders import views
urlpatterns=[
   path('cart/',views.cart,name="cart"),
   path("cart/add/<int:product_id>/",views.add_to_cart,name="add_to_cart"),
   path("<int:item_id>/cart_update/",views.update_cart,name="update_cart"),
   path("<int:item_id>/cart_remove/",views.remove_from_cart,name="remove_from_cart"),
   path("checkout/",views.checkout,name="checkout"),
   path("<int:order_id>/oder_success/",views.order_success,name="order_success"),
   path("orders/",views.order_history,name="order_history"),
   path("orders/<int:order_id>/",views.order_detail,name="order_detail"),
   path("staff/orders/",views.staff_order_list,name="staff_order_list"),
   path("staff/orders/<int:order_id>/edit/",views.staff_order_update,name="staff_order_update"),
]