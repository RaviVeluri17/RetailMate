from django.urls import path
from accounts import views
urlpatterns=[
    path("register/",views.register,name="register"),
    path("login/",views.user_login,name="login"),
    path("profile/",views.profile,name="profile"),
    path("logout/",views.user_logout,name="logout"),
    path('staff/',views.staff_dashboard,name="staff_dashboard")
]