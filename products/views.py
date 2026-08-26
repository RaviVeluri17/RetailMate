from django.shortcuts import render,HttpResponse,redirect
from .models import Product,Category
# Create your views here.
def product_list(request):
    products=Product.objects.all()
    context={
        "products":products
    }
    return render(request,"product_list.html",context)

def single_product(request,pk):
    product=Product.objects.get(id=pk)
    context={
        "product":product
    }
    return render(request,"single_product.html",context)

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


def product_update(request, pk):
    product = Product.objects.get(id=pk)
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

def product_delete(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        product.delete()
        return redirect("products_list")
    context={
        "product":product
    }
    return render(request, "product_delete.html", context)