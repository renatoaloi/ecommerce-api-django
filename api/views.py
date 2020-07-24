from api.serializers import CustomerSerializer, ProductSerializer
from api.models import Customer, Product
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

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
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ProductViewSet(ModelViewSet):
    """
    CRUD endpoint for Product management
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer