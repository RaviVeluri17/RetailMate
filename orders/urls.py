from django.urls import path
from orders import views
urlpatterns=[
   path('cart/',views.cart,name="cart"),
   path("cart/add/<int:product_id>/",views.add_to_cart,name="add_to_cart"),
   path("<int:item_id>/cart_update/",views.update_cart,name="update_cart"),
   path("<int:item_id>/cart_remove/",views.remove_from_cart,name="remove_from_cart"),
]