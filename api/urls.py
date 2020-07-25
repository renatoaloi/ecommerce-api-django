
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet, basename='customer')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'invoices', views.InvoiceViewSet, basename='invoice')
router.register(r'invoiceitems', views.InvoiceItemViewSet, basename='invoiceitem')

urlpatterns = [
    path('health-check', views.health_check.as_view(), name="health-check"),
    path('', include(router.urls)),
]