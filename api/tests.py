import datetime
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
import json

class TestEcommerceApi(TestCase):
    """
    This class contains tests for ecommerce API
    """

    #private
    def _create_model(self, model, data, fields):
        self.url = reverse("{}-list".format(model))
        response = self.client.post(self.url, data)
        if response.status_code == status.HTTP_201_CREATED:
            r_json = response.json()
            # check for the fields
            expected = {}
            original = {}
            for f in fields:
                original[f] = data[f]
                expected[f] = r_json[f]
            # trying a more pythonic way
            #fs = [{[f]: r_json[f]} for f in fields] #failed
            self.assertJSONEqual(
                json.dumps(expected, indent=4, sort_keys=True, default=str), 
                json.dumps(original, indent=4, sort_keys=True, default=str)
            )
            return r_json["id"]
        self.assertEqual(201, response.status_code)
        return None

    
    def _detail_model(self, model, data, id, fields):
        self.url = reverse("{}-detail".format(model), kwargs={'pk': id})
        response = self.client.get(self.url)
        if response.status_code == status.HTTP_200_OK:
            r_json = response.json()
            # check for the fields
            expected = {}
            original = {}
            for f in fields:
                original[f] = data[f]
                expected[f] = r_json[f]
            self.assertJSONEqual(
                json.dumps(expected, indent=4, sort_keys=True, default=str), 
                json.dumps(original, indent=4, sort_keys=True, default=str)
            )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
    

    def _update_model(self, model, id, data, data_names):
        self.url = reverse("{}-detail".format(model), kwargs={'pk': id})
        response = self.client.put(self.url, data, content_type="application/json")
        if response.status_code == status.HTTP_200_OK:
            r_json = response.json()
            # check if the name really changed
            for name in data_names:
                self.assertEqual(r_json[name], data[name])
        self.assertEqual(status.HTTP_200_OK, response.status_code)


    def _delete_model(self, model, id):
        self.url = reverse("{}-detail".format(model), kwargs={'pk': id})
        response = self.client.delete(self.url)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            # call detail again to check if it was really deleted
            self.url = reverse("{}-detail".format(model), kwargs={'pk': id})
            response_confirm = self.client.get(self.url)
            # response must be not found
            self.assertEqual(status.HTTP_404_NOT_FOUND, response_confirm.status_code)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)


    def setUp(self):
        """
        This method runs before execution of each test case
        """
        self.client = Client()
        # mockup's
        self.customer_data = {
            "name": "Create Test Case",
            "email": "create@test.case",
            "phone": "11967675454" 
        }
        self.product_data = {
            "name": "Tooth paste", 
            "description": "Protects the enamel", 
            "image_link": "https://en.wikipedia.org/wiki/Toothpaste#/media/File:Toothbrush,_Toothpaste,_Dental_Care_(571741)_(cropped).jpg", 
            "price": .99
        }
        self.invoice_data = {
            "customer_id": 0
        }
        self.invoice_item_data = {
            "invoice_id": 0,
            "product_id": 0,
            "quantity": 10,
            "amount_paid": 9.99
        }


    # Testing health check
    def test_health_check(self):
        """
        This test case checks if health check endpoint is responsive
        """
        self.url = reverse("health-check")
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)


    # Testing customer CRUD
    def test_customer_list(self):
        """
        This test case checks if customer list endpoint is working as expected
        """
        self.url = reverse("customer-list")
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)


    def test_customer_create(self):
        """
        This test case checks if customer create endpoint is working as expected
        """
        self._create_model("customer", self.customer_data, ["name", "email", "phone"])
    

    def test_customer_detail(self):
        """
        This test case checks if customer detail endpoint is working as expected
        """
        # first performing create
        id = self._create_model("customer", self.customer_data, ["name", "email", "phone"])
        if id:
            # then performing detail
            self._detail_model("customer", self.customer_data, id, ["name", "email", "phone"])
            
        self.assertIsNotNone(id)
    

    def test_customer_update(self):
        """
        This test case checks if customer update endpoint is working as expected
        """
        # first performe create
        id = self._create_model("customer", self.customer_data, ["name", "email", "phone"])
        if id:
            # then performe update
            data = { 
                "name": "Changed the name",
                "email": self.customer_data["email"],
                "phone": self.customer_data["phone"]
            }
            self._update_model("customer", id, data, ["name"])
        self.assertIsNotNone(id)
    

    def test_customer_delete(self):
        """
        This test case checks if customer delete endpoint is working as expected
        """
        # first performe create
        id = self._create_model("customer", self.customer_data, ["name", "email", "phone"])
        if id:
            # then performe delete
            self._delete_model("customer", id)
        self.assertIsNotNone(id)
    # END customer CRUD


    # Testing product CRUD
    def test_product_list(self):
        """
        This test case checks if product list endpoint is working as expected
        """
        self.url = reverse("product-list")
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)


    def test_product_create(self):
        """
        This test case checks if product create endpoint is working as expected
        """
        self._create_model("product", self.product_data, ["name", "description", "image_link", "price"])
    

    def test_product_detail(self):
        """
        This test case checks if product detail endpoint is working as expected
        """
        # first performing create
        id = self._create_model("product", self.product_data, ["name", "description", "image_link", "price"])
        if id:
            # then performing detail
            self._detail_model("product", self.product_data, id, ["name", "description", "image_link", "price"])
            
        self.assertIsNotNone(id)


    def test_product_update(self):
        """
        This test case checks if product update endpoint is working as expected
        """
        # first performe create
        id = self._create_model("product", self.product_data, ["name", "description", "image_link", "price"])
        if id:
            # then performe update
            data = { 
                "name": "Changed the name",
                "description": self.product_data["description"],
                "image_link": self.product_data["image_link"],
                "price": self.product_data["price"]
            }
            self._update_model("product", id, data, ["name"])
        self.assertIsNotNone(id)


    def test_product_delete(self):
        """
        This test case checks if product delete endpoint is working as expected
        """
        # first performe create
        id = self._create_model("product", self.product_data, ["name", "description", "image_link", "price"])
        if id:
            # then performe delete
            self._delete_model("product", id)
        self.assertIsNotNone(id)
    # END product CRUD


    # Testing invoice CRUD
    def test_invoice_list(self):
        """
        This test case checks if invoice list endpoint is working as expected
        """
        self.url = reverse("invoice-list")
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)


    def test_invoice_create(self):
        """
        This test case checks if invoice create endpoint is working as expected
        """
        # first we create a customer
        id = self._create_model("customer", self.customer_data, ["name", "email", "phone"])
        if id:
            # then we can create the invoice
            data = self.invoice_data
            data["customer_id"] = id
            self._create_model("invoice", data, [])
        self.assertIsNotNone(id)


    def test_invoice_detail(self):
        """
        This test case checks if invoice detail endpoint is working as expected
        """
        # first we create a customer
        id = self._create_model("customer", self.customer_data, ["name", "email", "phone"])
        if id:
            # then we can create the invoice
            data = self.invoice_data
            data["customer_id"] = id
            id_inv = self._create_model("invoice", data, [])
            if id_inv:
                # then performing detail
                self._detail_model("invoice", self.invoice_data, id, [])
            self.assertIsNotNone(id_inv)
        self.assertIsNotNone(id)


    def test_invoice_update(self):
        """
        This test case checks if invoice update endpoint is working as expected
        """
        # first we create a customer
        id = self._create_model("customer", self.customer_data, ["name", "email", "phone"])
        if id:
            # then we can create the invoice
            data = self.invoice_data
            data["customer_id"] = id
            id_inv = self._create_model("invoice", data, [])
            if id_inv:
                # create another customer
                id_other = self._create_model("customer", self.customer_data, ["name", "email", "phone"])
                if id_other:
                    # then performe update
                    data = self.invoice_data
                    data["customer_id"] = id_other
                    self._update_model("invoice", id, data, [])
                self.assertIsNotNone(id_other)
            self.assertIsNotNone(id_inv)
        self.assertIsNotNone(id)


    def test_product_delete(self):
        """
        This test case checks if product delete endpoint is working as expected
        """
        # first performe create
        id = self._create_model("product", self.product_data, ["name", "description", "image_link", "price"])
        if id:
            # then performe delete
            self._delete_model("product", id)
        self.assertIsNotNone(id)
    # END invoice CRUD


    # Testing invoice's item CRUD
    def test_invoice_item_list(self):
        """
        This test case checks if invoice's item list endpoint is working as expected
        """
        self.url = reverse("invoiceitem-list")
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)


    def test_invoice_item_create(self):
        """
        This test case checks if invoice's item create endpoint is working as expected
        """
        # first we create a customer
        id = self._create_model("customer", self.customer_data, ["name", "email", "phone"])
        if id:
            # then we create a invoice
            data = self.invoice_data
            data["customer_id"] = id
            id_inv = self._create_model("invoice", data, [])
            if id_inv:
                # then we create a product
                id_prod = self._create_model("product", self.product_data, ["name", "description", "image_link", "price"])
                if id_prod:
                    # then we can create the invoice's item
                    data = self.invoice_item_data
                    data["invoice_id"] = id_inv
                    data["product_id"] = id_prod
                    self._create_model("invoiceitem", data, ["quantity", "amount_paid"])
                self.assertIsNotNone(id_prod)
            self.assertIsNotNone(id_inv)
        self.assertIsNotNone(id)


    def test_invoice_item_detail(self):
        """
        This test case checks if invoice_item detail endpoint is working as expected
        """
        # first we create a customer
        id = self._create_model("customer", self.customer_data, ["name", "email", "phone"])
        if id:
            # then we create a invoice
            data = self.invoice_data
            data["customer_id"] = id
            id_inv = self._create_model("invoice", data, [])
            if id_inv:
                # then we create a product
                id_prod = self._create_model("product", self.product_data, [ "name", "description", "image_link", "price" ])
                if id_prod:
                    # then we can create the invoice's item
                    data = self.invoice_item_data
                    data["invoice_id"] = id_inv
                    data["product_id"] = id_prod
                    id_itm = self._create_model("invoiceitem", data, [ "quantity", "amount_paid" ])
                    if id_itm:
                        # then performing detail
                        self._detail_model("invoiceitem", self.invoice_item_data, id, [ "quantity", "amount_paid" ])
                    self.assertIsNotNone(id_itm)
                self.assertIsNotNone(id_prod)
            self.assertIsNotNone(id_inv)
        self.assertIsNotNone(id)


    def test_invoice_item_update(self):
        """
        This test case checks if invoice_item update endpoint is working as expected
        """
        # first we create a customer
        id = self._create_model("customer", self.customer_data, ["name", "email", "phone"])
        if id:
            # then we create a invoice
            data = self.invoice_data
            data["customer_id"] = id
            id_inv = self._create_model("invoice", data, [])
            if id_inv:
                # then we create a product
                id_prod = self._create_model("product", self.product_data, [ "name", "description", "image_link", "price" ])
                if id_prod:
                    # then we can create the invoice's item
                    data = self.invoice_item_data
                    data["invoice_id"] = id_inv
                    data["product_id"] = id_prod
                    id_itm = self._create_model("invoiceitem", data, [ "quantity", "amount_paid" ])
                    if id_itm:
                        # then performe update
                        data = self.invoice_item_data
                        data["price_paid"] = 88.77
                        self._update_model("invoiceitem", id, data, ["amount_paid"])
                    self.assertIsNotNone(id_itm)
                self.assertIsNotNone(id_prod)
            self.assertIsNotNone(id_inv)
        self.assertIsNotNone(id)


    def test_invoice_item_delete(self):
        """
        This test case checks if product delete endpoint is working as expected
        """
        # first we create a customer
        id = self._create_model("customer", self.customer_data, ["name", "email", "phone"])
        if id:
            # then we create a invoice
            data = self.invoice_data
            data["customer_id"] = id
            id_inv = self._create_model("invoice", data, [])
            if id_inv:
                # then we create a product
                id_prod = self._create_model("product", self.product_data, [ "name", "description", "image_link", "price" ])
                if id_prod:
                    # then we can create the invoice's item
                    data = self.invoice_item_data
                    data["invoice_id"] = id_inv
                    data["product_id"] = id_prod
                    id_itm = self._create_model("invoiceitem", data, [ "quantity", "amount_paid" ])
                    if id_itm:
                        # then performe delete
                        self._delete_model("invoiceitem", id_itm)
                    self.assertIsNotNone(id_itm)
                self.assertIsNotNone(id_prod)
            self.assertIsNotNone(id_inv)
        self.assertIsNotNone(id)
    # END invoice's item CRUD