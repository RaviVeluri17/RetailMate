from django.urls import path
from products import views
urlpatterns=[
    path("product_list/",views.product_list,name="products_list"),
    path("product_details/<int:pk>/",views.single_product,name="product_details"),
    path("create_product/",views.create_product,name="create_product"),
    path("<int:pk>/edit/",views.product_update,name="product_update"),
    path("<int:pk>/delete/",views.product_delete,name="product_delete"),

    path("categories_list/",views.category_list,name="category_list"),
    path("category_create/",views.category_create,name="category_create"),
    path("<int:pk>/category_update/",views.category_update,name="category_update"),
    path("<int:pk>/category_delete/",views.category_delete,name="category_delete"),

    path("suppliers/",views.supplier_list,name="supplier_list"),
    path("suppliers_create/",views.supplier_create,name="supplier_create"),
    path("<int:pk>/suppliers_update/",views.supplier_update,name="supplier_update"),
    path("<int:pk>/suppliers_delete/",views.supplier_delete,name="supplier_delete"),

    path("inventory/",views.inventory_list,name="inventory_list"),
    path("inventory_create/",views.inventory_create,name="inventory_create"),
    path("<int:pk>/inventory_update/",views.inventory_update,name="inventory_update"),

    path("product_suppliers_create",views.product_supplier_create,name="product_supplier_create"),

]