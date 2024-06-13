from django.contrib.auth.models import User
from store.models import Product
from rest_framework.permissions import IsAuthenticated, BasePermission


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='staff').exists()


def get_all_users():
    return User.objects.all()
    
    
def get_permissions(action):
    if action in ['update', 'partial_update', 'destroy']:
        permission_classes = [IsStaff]
    else:
        permission_classes = [IsAuthenticated]
    return [permission() for permission in permission_classes]
    

def get_all_products():
    return Product.objects.all()