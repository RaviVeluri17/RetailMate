from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def create_user(username, email, password):
    user = User.objects.create_user(username=username, email=email, password=password)
    return user

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not username:
            return render(request, "register.html",{"error": "Username is required"})

        if password != confirm_password:
            return render(request,"register.html",{"error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request,"register.html",{"error": "Username already exists"})

        try:
            validate_password(password)
        except ValidationError as e:
            return render(request,"register.html",{"error": e.messages[0]})
        
        new_user = create_user(username,email,password)
        customer_group = Group.objects.get(name="Customer")
        new_user.groups.add(customer_group)

        return HttpResponse("Registration successful")
    return render(request,"register.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        authenticated_user = authenticate(request,username=username,password=password)

        if authenticated_user:
            login(request, authenticated_user)
            return HttpResponse("Login successful")
        return HttpResponse("Invalid username or password")
    return render(request, "login.html")

@login_required
def profile(request):
    return HttpResponse(f"Logged in as {request.user.username}")

def user_logout(request):
    logout(request)
    return HttpResponse("Logged out successfully")

@login_required
def staff_dashboard(request):
    if not request.user.has_perm("products.add_product"):
        return HttpResponse("You are not authorized to access this page.", status=403)

    return HttpResponse(f"Staff Dashboard - Welcome {request.user.username}")