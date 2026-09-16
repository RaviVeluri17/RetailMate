from django.shortcuts import render,redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def create_user(username, email, password):
    user = User.objects.create_user(username=username, email=email, password=password)
    return user

def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not username:
            return render(request,"register.html",{"error": "Username is required"})

        if not email:
            return render(request,"register.html",{"error": "Email is required"})

        if password != confirm_password:
            return render(request,"register.html",{"error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request,"register.html",{"error": "Username already exists"})

        try:
            validate_password(password)
        except ValidationError as e:
            return render(request,"register.html",{"error": e.messages[0]})

        new_user = create_user(username, email, password)

        customer_group = Group.objects.filter(name="Customer").first()
        if customer_group:
            new_user.groups.add(customer_group)

        messages.success(request, "Account created successfully. Please sign in.")
        return redirect("login")
    return render(request, "register.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        authenticated_user = authenticate(request,username=username,password=password)

        if authenticated_user:
            login(request, authenticated_user)

            if authenticated_user.has_perm("products.add_product"):
                return redirect("staff_dashboard")
            return redirect("products_list")
        return render(request,"login.html",{"error": "Invalid username or password"})
    return render(request, "login.html")

@login_required
def profile(request):
    return render(request, "profile.html")

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been signed out.")
    return redirect("login")

@login_required
def staff_dashboard(request):
    if not request.user.has_perm("products.add_product"):
        return render(request,"staff_dashboard.html",{"unauthorized": True},status=403)
    return render(request, "staff_dashboard.html")