from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import Product,Category,Supplier,Inventory,ProductSupplier
from django.contrib.auth.decorators import login_required,permission_required
# Create your views here.
def product_list(request):
    products=Product.objects.all()
    context={
        "products":products
    }
    return render(request,"product_list.html",context)

def single_product(request,pk):
    product = get_object_or_404(Product, id=pk)
    context={
        "product":product
    }
    return render(request,"single_product.html",context)

@login_required
@permission_required("products.add_product", raise_exception=True)
def create_product(request):
    if request.method=="POST":
        name=request.POST.get("name")
        desc=request.POST.get("desc")
        cost_price=request.POST.get("mrp")
        selling_price=request.POST.get("selling_price")
        category_id=request.POST.get("category")

        category=Category.objects.get(id=category_id)

        Product.objects.create(name=name,desc=desc,mrp=cost_price,selling_price=selling_price,category=category)
        return HttpResponse("Product created succesfully")
    categories=Category.objects.all()

    context={
        "categories":categories
    }
    return render(request,"create_product.html",context)

@login_required
@permission_required("products.change_product",raise_exception=True)
def product_update(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("desc")
        category_id = request.POST.get("category")
        cost_price = request.POST.get("mrp")
        selling_price = request.POST.get("selling_price")

        category = Category.objects.get(id=category_id)

        product.name = name
        product.desc = description
        product.category = category
        product.mrp = cost_price
        product.selling_price = selling_price

        product.save()
        return HttpResponse("Product updated successfully")
    
    categories = Category.objects.all()
    context={
        "product": product,
        "categories": categories
    }
    return render(request,"product_update.html",context)

@login_required
@permission_required("products.delete_product",raise_exception=True)
def product_delete(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == "POST":
        product.delete()
        return redirect("products_list")
    context={
        "product":product
    }
    return render(request, "product_delete.html", context)


def category_list(request):
    category=Category.objects.all()
    context={
        "category":category
    }
    return render(request,"categories_list.html",context)


def category_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if Category.objects.filter(name=name).exists():
            return HttpResponse("Category already exists")

        Category.objects.create(name=name)
        return HttpResponse("Category created successfully")
    return render(request, "category_create.html")


def category_update(request, pk):
    category = get_object_or_404(Category, id=pk)
    if request.method == "POST":
        name = request.POST.get("name")

        if Category.objects.filter(name=name).exclude(id=pk).exists():
            return HttpResponse("Category already exists")
        
        category.name = name
        category.save()
        return HttpResponse("Category updated successfully")
    context={
        "category":category
    }
    return render(request,"category_update.html",context)


def category_delete(request, pk):
    category = get_object_or_404(Category, id=pk)
    if request.method == "POST":
        category.delete()
        return redirect("category_list")
    context={
        "category":category
    }
    return render( request,"category_delete.html",context)

# CATEGORIES CRUD
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request,"suppliers_list.html",{"suppliers": suppliers})


def supplier_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        if Supplier.objects.filter(name=name).exists():
            return HttpResponse("Supplier already exists")

        Supplier.objects.create(name=name,email=email,phone=phone,address=address)
        return redirect("supplier_list")
    return render(request, "supplier_create.html")


def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, id=pk)
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        if Supplier.objects.filter(name=name).exclude(id=pk).exists():
            return HttpResponse("Supplier already exists")

        supplier.name = name
        supplier.email = email
        supplier.phone = phone
        supplier.address = address

        supplier.save()
        return redirect("supplier_list")
    return render(request,"supplier_update.html",{"supplier": supplier})


def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, id=pk)
    if request.method == "POST":
        supplier.delete()
        return redirect("supplier_list")

    return render(request,"supplier_delete.html",{"supplier": supplier})

#INVENTORY LIST
def inventory_list(request):
    inventories = Inventory.objects.select_related("product").all()
    return render(request,"inventory_list.html",{"inventories": inventories})

def inventory_create(request):
    if request.method == "POST":
        product_id = request.POST.get("product")
        stock_quantity = request.POST.get("stock_quantity")
        reorder_level = request.POST.get("reorder_level")

        product = Product.objects.get(id=product_id)

        if Inventory.objects.filter(product=product).exists():
            return HttpResponse("Inventory already exists for this product")

        Inventory.objects.create(product=product,stock_quantity=stock_quantity,reorder_level=reorder_level)
        return HttpResponse("Inventory created successfully")
    
    products = Product.objects.all()
    return render(request,"inventory_create.html",{"products": products})

def inventory_update(request, pk):
    inventory = get_object_or_404(Inventory, id=pk)
    if request.method == "POST":
        stock_quantity = request.POST.get("stock_quantity")
        reorder_level = request.POST.get("reorder_level")

        inventory.stock_quantity = stock_quantity
        inventory.reorder_level = reorder_level
        inventory.save()
        return HttpResponse("Inventory updated successfully")
    return render(request,"inventory_update.html",{"inventory": inventory})

#-->PRODUCT SUPPLIER RELATION
def product_supplier_create(request):
    if request.method == "POST":
        product_id = request.POST.get("product")
        supplier_id = request.POST.get("supplier")

        product = Product.objects.get(id=product_id)
        supplier = Supplier.objects.get(id=supplier_id)

        if ProductSupplier.objects.filter(product=product,supplier=supplier).exists():
            return HttpResponse("This supplier is already associated with this product")

        ProductSupplier.objects.create(product=product,supplier=supplier)
        return HttpResponse("Supplier associated with product successfully")

    products = Product.objects.all()
    suppliers = Supplier.objects.all()
    return render(request,"product_supplier_create.html",{"products": products,"suppliers": suppliers})