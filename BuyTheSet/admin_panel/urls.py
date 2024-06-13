from django.urls import path
from . import views

urlpatterns = [
    path('', views.PanelView.as_view(), name='admin-panel'),
    path('products/', views.ProductView.as_view(), name='admin-products'),
]