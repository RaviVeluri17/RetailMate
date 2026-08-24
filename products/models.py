from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=64)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    name=models.CharField(max_length=64)
    desc=models.TextField()
    mrp=models.DecimalField(max_digits=10,decimal_places=2)
    selling_price=models.DecimalField(max_digits=10,decimal_places=2)
    expiry_date=models.DateField(null=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.PROTECT)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Supplier(models.Model):
    name=models.CharField(max_length=64)
    email=models.EmailField()
    phone=models.CharField()
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

class ProductSupplier(models.Model):
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    supplier=models.ForeignKey(Supplier,on_delete=models.PROTECT)
    supply_price=models.DecimalField(max_digits=10,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)

class Inventory(models.Model):
    product=models.OneToOneField(Product,on_delete=models.PROTECT)
    stock_quantity=models.IntegerField()
    reorder_level=models.IntegerField()
    updated_at=models.DateTimeField(auto_now=True)