from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image_link = models.TextField()
    price = models.FloatField()
    creation_date = models.DateTimeField(auto_now_add=True)


class Invoice(models.Model):
    customer = models.ForeignKey("Customer", related_name="customers", on_delete=models.DO_NOTHING)
    purchase_date = models.DateTimeField(auto_now_add=True)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey("Invoice", related_name="invoices", on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    product = models.ForeignKey("Product", related_name="products", on_delete=models.DO_NOTHING)
    amount_paid = models.FloatField()
    creation_date = models.DateTimeField(auto_now_add=True)
