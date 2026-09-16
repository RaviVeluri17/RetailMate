from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Product, Category, Supplier, Inventory, ProductSupplier


@login_required
def product_list(request):
    products = Product.objects.select_related("category").all()
    return render(request,"products/product_list.html",{"products": products})

@login_required
def single_product(request, pk):
    product = get_object_or_404(Product.objects.select_related("category"),id=pk)
    return render(request,"single_product.html",{"product": product})

@login_required
@permission_required("products.add_product", raise_exception=True)
def create_product(request):
    categories = Category.objects.all()

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        desc = request.POST.get("desc", "").strip()
        mrp = request.POST.get("mrp")
        selling_price = request.POST.get("selling_price")
        category_id = request.POST.get("category")

        if not name or not desc or not mrp or not selling_price or not category_id:
            return render(request,"create_product.html",{"categories": categories,"error": "All required fields must be filled."})

        try:
            mrp = float(mrp)
            selling_price = float(selling_price)
        except ValueError:
            return render(request,"create_product.html",{"categories": categories,"error": "MRP and selling price must be valid numbers."})

        if mrp < 0 or selling_price < 0:
            return render(request,"create_product.html",{"categories": categories,"error": "Prices cannot be negative."})

        if selling_price > mrp:
            return render(request,"create_product.html",{"categories": categories,"error": "Selling price cannot be greater than MRP."})

        category = get_object_or_404(Category, id=category_id)
        Product.objects.create(name=name,desc=desc,mrp=mrp,selling_price=selling_price,category=category)
        messages.success(request, "Product created successfully.")
        return redirect("products_list")
    return render(request,"create_product.html",{"categories": categories})


@login_required
@permission_required("products.change_product", raise_exception=True)
def product_update(request, pk):
    product = get_object_or_404(Product, id=pk)
    categories = Category.objects.all()

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("desc", "").strip()
        category_id = request.POST.get("category")
        mrp = request.POST.get("mrp")
        selling_price = request.POST.get("selling_price")

        if not name or not description or not mrp or not selling_price or not category_id:
            return render(request,"product_update.html",{"product": product,"categories": categories,"error": "All required fields must be filled."})

        try:
            mrp = float(mrp)
            selling_price = float(selling_price)
        except ValueError:
            return render(request,"product_update.html",{"product": product,"categories": categories,"error": "MRP and selling price must be valid numbers."})

        if mrp < 0 or selling_price < 0:
            return render(request,"product_update.html",{"product": product,"categories": categories,"error": "Prices cannot be negative."})

        if selling_price > mrp:
            return render(request,"product_update.html",{"product": product,"categories": categories,"error": "Selling price cannot be greater than MRP."})

        category = get_object_or_404(Category, id=category_id)

        product.name = name
        product.desc = description
        product.category = category
        product.mrp = mrp
        product.selling_price = selling_price
        product.save()

        messages.success(request, "Product updated successfully.")
        return redirect("products_list")
    return render(request,"product_update.html",{"product": product,"categories": categories})


@login_required
@permission_required("products.delete_product", raise_exception=True)
def product_delete(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect("products_list")
    return render(request,"product_delete.html",{"product": product})


# CATEGORIES
@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request,"categories_list.html",{"category": categories})

@login_required
@permission_required("products.add_category", raise_exception=True)
def category_create(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()

        if not name or not description:
            return render(request,"category_create.html",{"error": "Name and description are required."})

        if Category.objects.filter(name=name).exists():
            return render(request,"category_create.html",{"error": "Category already exists."})

        Category.objects.create(name=name,description=description)
        messages.success(request, "Category created successfully.")
        return redirect("category_list")
    return render(request, "category_create.html")


@login_required
@permission_required("products.change_category", raise_exception=True)
def category_update(request, pk):
    category = get_object_or_404(Category, id=pk)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()

        if not name or not description:
            return render(request,"category_update.html",{"category": category,"error": "Name and description are required."})

        if Category.objects.filter(name=name).exclude(id=pk).exists():
            return render(request,"category_update.html",{"category": category,"error": "Category already exists."})

        category.name = name
        category.description = description
        category.save()

        messages.success(request, "Category updated successfully.")
        return redirect("category_list")

    return render(request,"category_update.html",{"category": category})


@login_required
@permission_required("products.delete_category", raise_exception=True)
def category_delete(request, pk):
    category = get_object_or_404(Category, id=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect("category_list")
    return render(request,"category_delete.html",{"category": category})

# ----> SUPPLIERS
@login_required
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request,"suppliers_list.html",{"suppliers": suppliers})

@login_required
@permission_required("products.add_supplier", raise_exception=True)
def supplier_create(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()

        if not name or not email or not phone or not address:
            return render(request,"supplier_create.html",{"error": "All fields are required."})

        if Supplier.objects.filter(name=name).exists():
            return render(request,"supplier_create.html",{"error": "Supplier already exists."})

        Supplier.objects.create(name=name,email=email,phone=phone,address=address)
        messages.success(request, "Supplier created successfully.")
        return redirect("supplier_list")
    return render(request, "supplier_create.html")


@login_required
@permission_required("products.change_supplier", raise_exception=True)
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, id=pk)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()

        if not name or not email or not phone or not address:
            return render(request,"supplier_update.html",{"supplier": supplier,"error": "All fields are required."})

        if Supplier.objects.filter(name=name).exclude(id=pk).exists():
            return render(request,"supplier_update.html",{"supplier": supplier,"error": "Supplier already exists."})

        supplier.name = name
        supplier.email = email
        supplier.phone = phone
        supplier.address = address
        supplier.save()
        messages.success(request, "Supplier updated successfully.")
        return redirect("supplier_list")
    return render(request,"supplier_update.html",{"supplier": supplier})


@login_required
@permission_required("products.delete_supplier", raise_exception=True)
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, id=pk)

    if request.method == "POST":
        supplier.delete()
        messages.success(request, "Supplier deleted successfully.")
        return redirect("supplier_list")
    return render(request,"supplier_delete.html",{"supplier": supplier})


# INVENTORY

@login_required
def inventory_list(request):
    inventories = Inventory.objects.select_related("product").all()
    return render(request,"inventory_list.html",{"inventories": inventories})

@login_required
@permission_required("products.add_inventory", raise_exception=True)
def inventory_create(request):
    products = Product.objects.all()

    if request.method == "POST":
        product_id = request.POST.get("product")
        stock_quantity = request.POST.get("stock_quantity")
        reorder_level = request.POST.get("reorder_level")

        if not product_id or stock_quantity is None or reorder_level is None:
            return render(request,"inventory_create.html",{"products": products,"error": "All fields are required."})

        try:
            stock_quantity = int(stock_quantity)
            reorder_level = int(reorder_level)
        except ValueError:
            return render(request,"inventory_create.html",{"products": products,"error": "Stock quantity and reorder level must be integers."})

        if stock_quantity < 0 or reorder_level < 0:
            return render(request,"inventory_create.html",{"products": products,"error": "Stock values cannot be negative."})

        product = get_object_or_404(Product, id=product_id)

        if Inventory.objects.filter(product=product).exists():
            return render(request,"inventory_create.html",{"products": products,"error": "Inventory already exists for this product."})

        Inventory.objects.create(product=product,stock_quantity=stock_quantity,reorder_level=reorder_level)

        messages.success(request, "Inventory created successfully.")
        return redirect("inventory_list")
    return render(request,"inventory_create.html",{"products": products})


@login_required
@permission_required("products.change_inventory", raise_exception=True)
def inventory_update(request, pk):
    inventory = get_object_or_404(Inventory, id=pk)

    if request.method == "POST":
        stock_quantity = request.POST.get("stock_quantity")
        reorder_level = request.POST.get("reorder_level")

        try:
            stock_quantity = int(stock_quantity)
            reorder_level = int(reorder_level)
        except (TypeError, ValueError):
            return render(request,"inventory_update.html",{"inventory": inventory,"error": "Stock quantity and reorder level must be integers."})

        if stock_quantity < 0 or reorder_level < 0:
            return render(
                request,"inventory_update.html",{"inventory": inventory,"error": "Stock values cannot be negative."})

        inventory.stock_quantity = stock_quantity
        inventory.reorder_level = reorder_level
        inventory.save()

        messages.success(request, "Inventory updated successfully.")
        return redirect("inventory_list")
    return render(request,"inventory_update.html",{"inventory": inventory})

# PRODUCT-SUPPLIER

@login_required
@permission_required("products.add_productsupplier", raise_exception=True)
def product_supplier_create(request):
    products = Product.objects.all()
    suppliers = Supplier.objects.all()

    if request.method == "POST":
        product_id = request.POST.get("product")
        supplier_id = request.POST.get("supplier")
        supply_price = request.POST.get("supply_price")

        if not product_id or not supplier_id or not supply_price:
            return render(request,"product_supplier_create.html",{"products": products,"suppliers": suppliers,"error": "All fields are required."})

        try:
            supply_price = float(supply_price)
        except ValueError:
            return render(request,"product_supplier_create.html",{"products": products,"suppliers": suppliers,"error": "Supply price must be a valid number."})

        if supply_price < 0:
            return render(request,"product_supplier_create.html",{"products": products,"suppliers": suppliers,"error": "Supply price cannot be negative."})

        product = get_object_or_404(Product, id=product_id)
        supplier = get_object_or_404(Supplier, id=supplier_id)

        if ProductSupplier.objects.filter(product=product,supplier=supplier).exists():
            return render(request,"product_supplier_create.html",{"products": products,"suppliers": suppliers,"error": "This supplier is already associated with this product."})

        ProductSupplier.objects.create(product=product,supplier=supplier,supply_price=supply_price)
        messages.success(request,"Supplier associated with product successfully.")
        return redirect("products_list")
    return render(request,"product_supplier_create.html",{"products": products,"suppliers": suppliers})