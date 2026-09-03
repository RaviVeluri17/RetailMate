from rest_framework import serializers
from products.models import Product,Category,Supplier,Inventory
from orders.models import CartItem,Order,OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=["id","name","desc","mrp","selling_price","expiry_date","category"]

    def validate(self, data):
        mrp = data.get("mrp")
        selling_price = data.get("selling_price")
        if mrp is not None and selling_price is not None:
            if selling_price > mrp:
                raise serializers.ValidationError("Selling price cannot be greater than MRP.")
        return data

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=["id","name"]

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model=Supplier
        fields="__all__"

class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        fields = "__all__"

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields="__all__"
        read_only_fields=["customer"]

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ["id","customer","status","total_amount","created_at","updated_at","items",]
        read_only_fields = ["customer","status","total_amount","created_at","updated_at","items",]

    def get_items(self, obj):
        items = obj.orderitem_set.all()
        return OrderItemSerializer(items, many=True).data