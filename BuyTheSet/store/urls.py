from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('about/', views.about, name="about"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name='register'),
    path('update-password/', views.update_password, name='update_password'),
    path('update-user/', views.update_user, name='update_user'),
    # path('update-info/', views.update_info, name='update_info'),
    path('order-history/', views.order_history, name='order_history'),
    path('order/<int:order_id>/', views.order_details, name='order_details'),
    path('order/update/', views.update_order, name='update_order'),
    path('product/<int:pk>/', views.product, name='product'),
]

