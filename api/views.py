from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from api.serializers import CustomerSerializer, InvoiceSerializer, ProductSerializer, InvoiceItemSerializer, ShoppingCartSerializer
from api.models import Customer, Invoice, Product, InvoiceItem, ShoppingCart
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


class health_check(APIView):
    """
    Endpoint used by ELB Target Group to check if ECS container is healty
    """

    def get(self, request):
        """
        Health check GET method returns always HTTP status = 200 (OK)
        """
        return Response({"message": "OK"}, status=200)


class CustomerViewSet(ModelViewSet):
    """
    CRUD endpoint for Customer management
    """
    permission_classes = (IsAuthenticated,)
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ProductViewSet(ModelViewSet):
    """
    CRUD endpoint for Product management
    """
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class InvoiceViewSet(ModelViewSet):
    """
    CRUD endpoint for Invoice management
    """
    permission_classes = (IsAuthenticated,)
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class InvoiceItemViewSet(ModelViewSet):
    """
    CRUD endpoint for Invoice's Item management
    """
    permission_classes = (IsAuthenticated,)
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer


class ShoppingCartViewSet(ModelViewSet):
    """
    CRUD endpoint for shopping cart management
    """
    permission_classes = (IsAuthenticated,)
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer


class AuthToken(APIView):
    """
    Authentication endpoint to get user's auth token
    """
    def post(self, request):
        """
        POST method requires a payload with username and password, like this:
        {
            "username": "your_username",
            "password": "your password"
        }
        Note: Use Django's administration console to create a user for you
        http://localhost:8000/admin
        """
        try:
            payload = request.data
            username = payload["username"] if "username" in payload else ""
            password = payload["password"] if "password" in payload else ""
            user = User.objects.get(username=username)
            if user.check_password(password):
                token = Token.objects.filter(user=user).first()
                if not token:
                    token = Token.objects.create(user=user)
                return Response({"message": "OK", "token": token.key}, status=200)
        except User.DoesNotExist:
            pass
        except Exception as e:
            print(str(e))
        return Response({"message": "Auth Invalid", "token": ""}, status=404)


class UpdateShoppingCart(APIView):
    """
    Endpoint for update user's shopping cart
    """
    def post(self, request):
        data = request.data
        cart = ShoppingCart.objects.filter(id=data["id"]).first()
        if cart:
            # checking if it's closed
            if cart.is_closed:
                return Response({"message": "Error! Cart already closed!", "cart": {}}, status=400)
        # else continues
        serializer = ShoppingCartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response({"message": "OK", "cart": serializer.data}, status=200)

