from icecream import ic
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from store.serializers import ProductSerializer
from .serializers import UserSerializer
from . import services


# Obtain JWT tokens and store them in httponly cookies.
class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.set_cookie('access_token', response.data['access'], httponly=True)
        response.set_cookie('refresh_token', response.data['refresh'], httponly=True)
        response.data = {'detail': 'success'}
        return response
    

# Refresh JWT tokens and store the new access token in an httponly cookie.
class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.set_cookie('access_token', response.data['access'], httponly=True)
        response.data = {'detail': 'success'}
        return response


# Verify the validity of the JWT token.
class VerifyTokenView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'detail': 'Token is valid'})


# ViewSet for viewing and editing User instances.
class UserViewSet(viewsets.ModelViewSet):
    queryset = services.get_all_users()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        return services.get_permissions(self.action)

    
# ViewSet for viewing and editing Product instances.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = services.get_all_products()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]