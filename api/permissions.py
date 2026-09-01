from rest_framework.permissions import BasePermission

class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # Everyone authenticated can read
        if request.method == "GET":
            return True

        # Only Staff/Admin can modify
        return (
            request.user.is_staff
            or request.user.groups.filter(name="Staff").exists()
            or request.user.groups.filter(name="Admin").exists()
        )

class IsCustomer(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and not request.user.is_staff
            and request.user.groups.filter(name="Customer").exists()
        )