
from api.views import UpdateShoppingCart
from django.urls import path, include
from rest_framework.generics import UpdateAPIView
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet, basename='customer')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'invoices', views.InvoiceViewSet, basename='invoice')
router.register(r'invoiceitems', views.InvoiceItemViewSet, basename='invoiceitem')
router.register(r'shoppingcarts', views.ShoppingCartViewSet, basename='shoppingcart')

urlpatterns = [
    path('health-check', views.health_check.as_view(), name="health-check"),
    path('update-shoppingcart', views.UpdateShoppingCart.as_view(), name="update-shoppingcart"),
    path('', include(router.urls)),
]