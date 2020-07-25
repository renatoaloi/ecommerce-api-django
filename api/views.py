from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from api.serializers import CustomerSerializer, InvoiceSerializer, ProductSerializer, InvoiceItemSerializer
from api.models import Customer, Invoice, Product, InvoiceItem


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


class InvoiceViewSet(ModelViewSet):
    """
    CRUD endpoint for Invoice management
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class InvoiceItemViewSet(ModelViewSet):
    """
    CRUD endpoint for Invoice's Item management
    """
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer
