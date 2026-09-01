from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet,CategoryViewSet,SupplierViewSet,InventoryViewSet,CartItemViewSet,OrderViewSet

router=DefaultRouter()
router.register("products",ProductViewSet,basename="product")
router.register("categories",CategoryViewSet,basename="category")
router.register("suppliers",SupplierViewSet,basename="supplier")
router.register("inventory",InventoryViewSet,basename="inventory")
router.register("cart",CartItemViewSet,basename="cart")
router.register("orders",OrderViewSet,basename="order")
urlpatterns=[
    path("", include(router.urls)),
]