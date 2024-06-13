from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('check-product-availablity/', views.check_product_availability, name='check_product_availability'),
    path('save-order/', views.save_order, name='save_order'),
    path('save-shipping-info/', views.save_shipping_info, name='save_shipping_info'),
    path('success/', views.payment_success, name='payment_success'),
]