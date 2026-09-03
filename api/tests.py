from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from products.models import Product, Category,Inventory
from orders.models import CartItem, Order
from django.test.utils import CaptureQueriesContext
from django.db import connection

class ProductAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = User.objects.create_user(username="customer",password="test123")
        self.staff = User.objects.create_user(username="staff",password="test123")
        staff_group = Group.objects.create(name="Staff")
        self.staff.groups.add(staff_group)
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Wireless Mouse",
            desc="2.4GHz wireless mouse",
            mrp=1000,
            selling_price=700,
            category=self.category
        )

    def test_customer_can_view_products(self):
        self.client.force_authenticate(user=self.customer)
        response = self.client.get(
            "/api/products/"
        )
        self.assertEqual(response.status_code,200)

    def test_unauthenticated_user_cannot_view_products(self):
        response = self.client.get(
            "/api/products/"
        )
        self.assertIn(response.status_code, [401, 403])

    def test_customer_cannot_create_product(self):
        self.client.force_authenticate(user=self.customer)
        data = {
            "name": "Keyboard",
            "desc": "Mechanical keyboard",
            "mrp": "3000.00",
            "selling_price": "2500.00",
            "category": self.category.id
        }
        response = self.client.post("/api/products/",data,format="json")
        self.assertEqual(response.status_code,403)

    def test_staff_can_create_product(self):
        self.client.force_authenticate(user=self.staff)
        data = {
            "name": "Keyboard",
            "desc": "Mechanical keyboard",
            "mrp": "3000.00",
            "selling_price": "2500.00",
            "category": self.category.id
        }
        response = self.client.post("/api/products/",data,format="json")
        self.assertEqual(response.status_code,201)

    def test_selling_price_cannot_exceed_mrp(self):
        self.client.force_authenticate(
            user=self.staff
        )
        data = {
            "name": "Keyboard",
            "desc": "Mechanical keyboard",
            "mrp": "2000.00",
            "selling_price": "2500.00",
            "category": self.category.id
        }
        response = self.client.post("/api/products/",data,format="json")
        self.assertEqual(response.status_code,400)

class OrderAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = User.objects.create_user(username="customer",password="test123")
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Wireless Mouse",
            desc="2.4GHz wireless mouse",
            mrp=1000,
            selling_price=700,
            category=self.category
        )
        self.inventory = Inventory.objects.create(product=self.product,stock_quantity=10,reorder_level=5)
        self.client.force_authenticate(user=self.customer)

    def test_create_order(self):
        CartItem.objects.create(customer=self.customer,product=self.product,quantity=2)
        response = self.client.post("/api/orders/",{},format="json")
        self.assertEqual(response.status_code,201)
        self.assertEqual(Order.objects.count(),1)

    def test_order_reduces_inventory(self):
        CartItem.objects.create(customer=self.customer,product=self.product,quantity=3)
        self.client.post("/api/orders/",{},format="json")
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.stock_quantity,7)

    def test_cart_is_cleared_after_order(self):
        CartItem.objects.create(customer=self.customer,product=self.product,quantity=2)
        self.client.post("/api/orders/",{},format="json")
        self.assertEqual(CartItem.objects.filter(customer=self.customer).count(),0)

    def test_empty_cart_cannot_create_order(self):
        response = self.client.post("/api/orders/",{},format="json")
        self.assertEqual(response.status_code,400)
        self.assertEqual(Order.objects.count(),0)

    def test_insufficient_stock_cannot_create_order(self):
        CartItem.objects.create(customer=self.customer,product=self.product,quantity=20)
        response = self.client.post("/api/orders/",{},format="json")
        self.assertEqual(response.status_code,400)
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.stock_quantity,10)
        self.assertEqual(Order.objects.count(),0)