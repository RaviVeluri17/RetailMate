from products.models import Product,Category,Supplier,Inventory
from orders.models import CartItem,Order
from .serializers import ProductSerializer,CategorySerializer,SupplierSerializer,InventorySerializer,CartItemSerializer,OrderSerializer
from .permissions import IsStaffOrReadOnly,IsCustomer
from rest_framework.viewsets import ModelViewSet,ViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from orders.services import place_order


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields=["category"]
    search_fields=["name","desc"]
    ordering_fields=["name","mrp","selling_price"]

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]

class SupplierViewSet(ModelViewSet):
    queryset=Supplier.objects.all()
    serializer_class=SupplierSerializer
    permission_classes=[IsStaffOrReadOnly]

class InventoryViewSet(ModelViewSet):
    queryset=Inventory.objects.all()
    serializer_class=InventorySerializer
    permission_classes=[IsStaffOrReadOnly]

class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsCustomer]
    def get_queryset(self):
        return CartItem.objects.filter(customer=self.request.user)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get("product")
        quantity = request.data.get("quantity")
        if not product_id or not quantity:
            return Response({"error": "Product and quantity are required."},status=status.HTTP_400_BAD_REQUEST)
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            return Response({"error": "Quantity must be a positive integer."},status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item = CartItem.objects.get(customer=request.user,product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()

        except CartItem.DoesNotExist:
            serializer = self.get_serializer(data={"product": product_id,"quantity": quantity})
            serializer.is_valid(raise_exception=True)
            cart_item = serializer.save(customer=request.user)
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class OrderViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        orders = Order.objects.filter(customer=request.user)
        serializer = OrderSerializer(orders,many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            order = Order.objects.get(id=pk,customer=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def create(self, request):
        try:
            order = place_order(request.user)
        except ValueError as e:
            return Response({"error": str(e)},status=status.HTTP_400_BAD_REQUEST)
        serializer = OrderSerializer(order)
        return Response(serializer.data,status=status.HTTP_201_CREATED)