from django.urls import path
from products import views
urlpatterns=[
    path("product_list/",views.product_list,name="products_list"),
    path("product_details/<int:pk>/",views.single_product,name="product_details"),
    path("create_product",views.create_product,name="create_product"),
    path("<int:pk>/edit/",views.product_update,name="product_update"),
    path("<int:pk>/delete/",views.product_delete,name="product_delete"),
]