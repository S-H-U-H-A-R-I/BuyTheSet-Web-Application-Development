from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.cart_add, name='cart_add'),
    path('items/', views.cart_items, name='cart_items'),
    path('delete/', views.cart_delete, name='cart_delete'),
    path('update/', views.cart_update, name='cart_update'),
]