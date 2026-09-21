from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from products.models import Product, Category, Inventory
from orders.models import CartItem, Order, OrderItem

class ProductAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = User.objects.create_user(username="customer",password="test123")
        self.staff = User.objects.create_user(username="staff",password="test123")
        staff_group = Group.objects.create(name="Staff")
        self.staff.groups.add(staff_group)
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(name="Wireless Mouse",desc="2.4GHz wireless mouse",mrp=1000,selling_price=700,category=self.category)

    def test_customer_can_view_products(self):
        self.client.force_authenticate(user=self.customer)
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_cannot_view_products(self):
        response = self.client.get("/api/products/")
        self.assertIn(response.status_code, [401, 403])

    def test_customer_cannot_create_product(self):
        self.client.force_authenticate(user=self.customer)
        data = {"name": "Keyboard","desc": "Mechanical keyboard","mrp": "3000.00","selling_price": "2500.00","category": self.category.id}
        response = self.client.post("/api/products/",data,format="json")
        self.assertEqual(response.status_code, 403)

    def test_staff_can_create_product(self):
        self.client.force_authenticate(user=self.staff)
        data = {"name": "Keyboard","desc": "Mechanical keyboard","mrp": "3000.00","selling_price": "2500.00","category": self.category.id}
        response = self.client.post("/api/products/",data,format="json")
        self.assertEqual(response.status_code, 201)

    def test_selling_price_cannot_exceed_mrp(self):
        self.client.force_authenticate(user=self.staff)
        data = {"name": "Keyboard","desc": "Mechanical keyboard","mrp": "2000.00","selling_price": "2500.00","category": self.category.id}
        response = self.client.post("/api/products/",data,format="json")
        self.assertEqual(response.status_code, 400)

    def test_customer_cannot_update_product(self):
        self.client.force_authenticate(user=self.customer)
        response = self.client.patch(f"/api/products/{self.product.id}/",{"selling_price": "600.00"},format="json")
        self.assertEqual(response.status_code, 403)

    def test_customer_cannot_delete_product(self):
        self.client.force_authenticate(user=self.customer)
        response = self.client.delete(f"/api/products/{self.product.id}/")
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Product.objects.filter(id=self.product.id).exists())

    def test_staff_can_update_product(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.patch(f"/api/products/{self.product.id}/",{"selling_price": "600.00"},format="json")
        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(str(self.product.selling_price),"600.00")

class OrderAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = User.objects.create_user(username="customer",password="test123")
        customer_group = Group.objects.create(name="Customer")
        self.customer.groups.add(customer_group)
        self.other_customer = User.objects.create_user(username="other_customer",password="test123")
        self.other_customer.groups.add(customer_group)
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(name="Wireless Mouse",desc="2.4GHz wireless mouse",mrp=1000,selling_price=700,category=self.category)
        self.inventory = Inventory.objects.create(product=self.product,stock_quantity=10,reorder_level=5)
        self.client.force_authenticate(user=self.customer)

    def test_create_order(self):
        CartItem.objects.create(customer=self.customer,product=self.product,quantity=2)
        response = self.client.post("/api/orders/",{},format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)

    def test_order_reduces_inventory(self):
        CartItem.objects.create(customer=self.customer,product=self.product,quantity=3)
        self.client.post( "/api/orders/",{},format="json")
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.stock_quantity,7)

    def test_cart_is_cleared_after_order(self):
        CartItem.objects.create(customer=self.customer,product=self.product,quantity=2)
        self.client.post("/api/orders/",{},format="json")
        self.assertEqual(CartItem.objects.filter(customer=self.customer).count(),0)

    def test_empty_cart_cannot_create_order(self):
        response = self.client.post("/api/orders/",{},format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)

    def test_insufficient_stock_cannot_create_order(self):
        CartItem.objects.create(customer=self.customer,product=self.product,quantity=20)
        response = self.client.post("/api/orders/",{},format="json")
        self.assertEqual(response.status_code, 400)
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.stock_quantity,10)
        self.assertEqual(Order.objects.count(),0)

    def test_order_total_is_calculated_correctly(self):
        CartItem.objects.create(customer=self.customer,product=self.product,quantity=3)
        response = self.client.post("/api/orders/",{},format="json")
        self.assertEqual(response.status_code, 201)
        order = Order.objects.get(customer=self.customer)
        self.assertEqual(str(order.total_amount),"2100.00")

    def test_order_item_stores_selling_price(self):
        CartItem.objects.create(customer=self.customer,product=self.product,quantity=2)
        response = self.client.post("/api/orders/",{},format="json")
        self.assertEqual(response.status_code, 201)
        order = Order.objects.get(customer=self.customer)
        item = OrderItem.objects.get(order=order)
        self.assertEqual(str(item.price),"700.00")

    def test_customer_cannot_access_another_customers_order(self):
        other_order = Order.objects.create(customer=self.other_customer,status="PENDING",total_amount=700)
        response = self.client.get(f"/api/orders/{other_order.id}/")
        self.assertEqual( response.status_code, 404)

    def test_customer_cannot_access_another_customers_cart_item(self):
        other_cart_item = CartItem.objects.create(customer=self.other_customer,product=self.product,quantity=2)
        response = self.client.get(f"/api/cart/{other_cart_item.id}/")
        self.assertEqual(response.status_code,404)

    def test_adding_same_product_increases_cart_quantity(self):
        CartItem.objects.create(customer=self.customer,product=self.product,quantity=2)
        response = self.client.post("/api/cart/",{"product": self.product.id,"quantity": 3},format="json")
        self.assertEqual(response.status_code,201)
        cart_item = CartItem.objects.get(customer=self.customer,product=self.product)
        self.assertEqual(cart_item.quantity,5)

    def test_cart_rejects_invalid_quantity(self):
        response = self.client.post("/api/cart/",{"product": self.product.id,"quantity": 0},format="json")
        self.assertIn(response.status_code,[400, 422])
        self.assertFalse(CartItem.objects.filter(customer=self.customer,product=self.product).exists())

    def test_customer_cannot_change_cart_item_product(self):
        cart_item = CartItem.objects.create(customer=self.customer,product=self.product,quantity=2)
        another_product = Product.objects.create(name="Keyboard",desc="Mechanical keyboard",mrp=2000,selling_price=1500,category=self.category)
        response = self.client.patch(f"/api/cart/{cart_item.id}/",{"product": another_product.id},format="json")
        self.assertEqual(response.status_code, 200)
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.product_id, self.product.id)

    def test_customer_cannot_change_order_status(self):
        order = Order.objects.create(customer=self.customer,status="PENDING",total_amount=700)
        response = self.client.patch(f"/api/orders/{order.id}/status/",{"status": "DELIVERED"},format="json")
        self.assertEqual(response.status_code, 403)
        order.refresh_from_db()
        self.assertEqual(order.status, "PENDING")

    def test_customer_cannot_modify_order_fields(self):
        order = Order.objects.create(customer=self.customer,status="PENDING",total_amount=700)
        response = self.client.patch(f"/api/orders/{order.id}/",{"status": "DELIVERED","total_amount": 1},format="json")
        self.assertIn(response.status_code, [404, 405])
        order.refresh_from_db()
        self.assertEqual(order.status, "PENDING")
        self.assertEqual(str(order.total_amount), "700.00")