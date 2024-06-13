from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


# URL configuration for Authentication and Token Management
urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token/', views.CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', views.VerifyTokenView.as_view(), name='token_verify'),
]


# Setup API Endpoints with Django Rest Framework DefaultRouter
router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'users', views.UserViewSet)
urlpatterns += router.urls