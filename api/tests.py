import datetime
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
import json
from django.contrib.auth.models import User

class TestEcommerceApi(TestCase):
    """
    This class contains tests for ecommerce API
    """

    #private
    def _create_model(self, model, data, fields):
        self.url = reverse("{}-list".format(model))
        response = self.client.post(self.url, data, **self.auth_headers)
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
        response = self.client.get(self.url, **self.auth_headers)
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
        response = self.client.put(self.url, data, content_type="application/json", **self.auth_headers)
        if response.status_code == status.HTTP_200_OK:
            r_json = response.json()
            # check if the name really changed
            for name in data_names:
                self.assertEqual(r_json[name], data[name])
        self.assertEqual(status.HTTP_200_OK, response.status_code)


    def _delete_model(self, model, id):
        self.url = reverse("{}-detail".format(model), kwargs={'pk': id})
        response = self.client.delete(self.url, **self.auth_headers)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            # call detail again to check if it was really deleted
            self.url = reverse("{}-detail".format(model), kwargs={'pk': id})
            response_confirm = self.client.get(self.url, **self.auth_headers)
            # response must be not found
            self.assertEqual(status.HTTP_404_NOT_FOUND, response_confirm.status_code)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)


    def setUp(self):
        """
        This method runs before execution of each test case
        """
        self.client = Client()
        self.token = ""
        self.auth_headers = ""
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
            "customer_id": 0,
            "total_value": 0.0,
            "total_quantity": 0.0,
            "total_discount": 0.0
        }
        self.invoice_item_data = {
            "invoice_id": 0,
            "product_id": 0,
            "quantity": 10,
            "quote_price": 9.99,
            "discount_value": 0.0
        }
        self.shoppingcart_data = {
            "customer_id": 0,
            "product_id": 0,
            "quantity": 0,
            "discount_value": 0.0,
            "is_closed": False
        }
        self.auth_user = {
            "first_name": "Renato",
            "last_name": "Aloi",
            "username": "renato.aloi",
            "password": "123456",
            "email": "renato.aloi@gmail.com"
        }

        # trying to get a token
        try:
            # create user
            user = User.objects.create_user(
                self.auth_user["username"],
                self.auth_user["email"],
                self.auth_user["password"]
            )
            user.first_name = self.auth_user["first_name"]
            user.last_name = self.auth_user["last_name"]
            user.save()
            response = self.client.post("/auth", self.auth_user)
            if response.status_code == 200:
                self.token = response.data["token"] if "token" in response.data else ""
                self.auth_headers = { "HTTP_AUTHORIZATION": "Token {}".format(self.token)}
        except Exception as e:
            print(str(e))


    # Testing health check
    def test_health_check(self):
        """
        This test case checks if health check endpoint is responsive
        """
        self.url = reverse("health-check")
        response = self.client.get(self.url, **self.auth_headers)
        self.assertEqual(200, response.status_code)


    # Testing customer CRUD
    def test_customer_list(self):
        """
        This test case checks if customer list endpoint is working as expected
        """
        self.url = reverse("customer-list")
        response = self.client.get(self.url, **self.auth_headers)
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
        response = self.client.get(self.url, **self.auth_headers)
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
        response = self.client.get(self.url, **self.auth_headers)
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


    def test_invoice_delete(self):
        """
        This test case checks if invoice delete endpoint is working as expected
        """
        # first we create a customer
        id = self._create_model("customer", self.customer_data, ["name", "email", "phone"])
        if id:
            # then we can create the invoice
            data = self.invoice_data
            data["customer_id"] = id
            id_inv = self._create_model("invoice", data, [])
            if id_inv:
                # then performe delete
                self._delete_model("invoice", id_inv)
            self.assertIsNotNone(id_inv)
        self.assertIsNotNone(id)
    # END invoice CRUD


    # Testing invoice's item CRUD
    def test_invoice_item_list(self):
        """
        This test case checks if invoice's item list endpoint is working as expected
        """
        self.url = reverse("invoiceitem-list")
        response = self.client.get(self.url, **self.auth_headers)
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
                    self._create_model("invoiceitem", data, ["quantity", "quote_price"])
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
                    id_itm = self._create_model("invoiceitem", data, [ "quantity", "quote_price" ])
                    if id_itm:
                        # then performing detail
                        self._detail_model("invoiceitem", self.invoice_item_data, id, [ "quantity", "quote_price" ])
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
                    id_itm = self._create_model("invoiceitem", data, [ "quantity", "quote_price" ])
                    if id_itm:
                        # then performe update
                        data = self.invoice_item_data
                        data["price_paid"] = 88.77
                        self._update_model("invoiceitem", id, data, ["quote_price"])
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
                    id_itm = self._create_model("invoiceitem", data, [ "quantity", "quote_price" ])
                    if id_itm:
                        # then performe delete
                        self._delete_model("invoiceitem", id_itm)
                    self.assertIsNotNone(id_itm)
                self.assertIsNotNone(id_prod)
            self.assertIsNotNone(id_inv)
        self.assertIsNotNone(id)
    # END invoice's item CRUD


    # Testing shoppingcart CRUD
    def test_shoppingcart_list(self):
        """
        This test case checks if shoppingcart list endpoint is working as expected
        """
        self.url = reverse("shoppingcart-list")
        response = self.client.get(self.url, **self.auth_headers)
        self.assertEqual(200, response.status_code)


    def test_shoppingcart_create(self):
        """
        This test case checks if shoppingcart create endpoint is working as expected
        """
        # first we create a customer
        id = self._create_model("customer", self.customer_data, ["name", "email", "phone"])
        if id:
            # then we create a product
            id_prod = self._create_model("product", self.product_data, ["name", "description", "image_link", "price"])
            if id_prod:
                # then we can create the shoppingcart
                data = self.shoppingcart_data
                data["customer_id"] = id
                data["product_id"] = id
                self._create_model("shoppingcart", data, [ "quantity", "discount_value", "is_closed" ])
            self.assertIsNotNone(id_prod)
        self.assertIsNotNone(id)


    def test_shoppingcart_detail(self):
        """
        This test case checks if shoppingcart detail endpoint is working as expected
        """
        # first we create a customer
        id = self._create_model("customer", self.customer_data, ["name", "email", "phone"])
        if id:
            # then we create a product
            id_prod = self._create_model("product", self.product_data, ["name", "description", "image_link", "price"])
            if id_prod:
                # then we can create the shoppingcart
                data = self.shoppingcart_data
                data["customer_id"] = id
                data["product_id"] = id
                id_cart = self._create_model("shoppingcart", data, ["quantity", "discount_value", "is_closed"])
                if id_cart:
                    # then performing detail
                    self._detail_model("shoppingcart", self.shoppingcart_data, id, ["quantity", "discount_value", "is_closed"])
                self.assertIsNotNone(id_cart)
            self.assertIsNotNone(id_prod)
        self.assertIsNotNone(id)


    def test_shoppingcart_update(self):
        """
        This test case checks if shoppingcart update endpoint is working as expected
        """
        # first we create a customer
        id = self._create_model("customer", self.customer_data, ["name", "email", "phone"])
        if id:
            # then we create a product
            id_prod = self._create_model("product", self.product_data, ["name", "description", "image_link", "price"])
            if id_prod:
                # then we can create the shoppingcart
                data = self.shoppingcart_data
                data["customer_id"] = id
                data["product_id"] = id
                id_cart = self._create_model("shoppingcart", data, ["quantity", "discount_value", "is_closed"])
                if id_cart:
                    # then performe update
                    data = self.shoppingcart_data
                    data["quantity"] = 20
                    data["discount_value"] = 9.99
                    data["is_closed"] = True
                    self._update_model("shoppingcart", id, data, ["quantity", "discount_value", "is_closed"])
                self.assertIsNotNone(id_cart)
            self.assertIsNotNone(id_prod)
        self.assertIsNotNone(id)


    def test_shoppingcart_delete(self):
        """
        This test case checks if shoppingcart delete endpoint is working as expected
        """
        # first we create a customer
        id = self._create_model("customer", self.customer_data, ["name", "email", "phone"])
        if id:
            # then we create a product
            id_prod = self._create_model("product", self.product_data, ["name", "description", "image_link", "price"])
            if id_prod:
                # then we can create the shoppingcart
                data = self.shoppingcart_data
                data["customer_id"] = id
                data["product_id"] = id
                id_cart = self._create_model("shoppingcart", data, ["quantity", "discount_value", "is_closed"])
                if id_cart:
                    # then performe delete
                    self._delete_model("shoppingcart", id_cart)
                self.assertIsNotNone(id_cart)
            self.assertIsNotNone(id_prod)
        self.assertIsNotNone(id)
    # END shoppingcart CRUD


    # Testing Update Soppingcart View
    def test_update_shoppingcart_view(self):
        """
        Test for update cart view
        """
        # first we create a customer
        id = self._create_model("customer", self.customer_data, ["name", "email", "phone"])
        if id:
            # then we create a product
            id_prod = self._create_model("product", self.product_data, ["name", "description", "image_link", "price"])
            if id_prod:
                # then we can create the shoppingcart
                data = self.shoppingcart_data
                data["customer_id"] = id
                data["product_id"] = id
                id_cart = self._create_model("shoppingcart", data, ["quantity", "discount_value", "is_closed"])
                if id_cart:
                    # then performe the update
                    self.url = reverse("update-shoppingcart")
                    data = { **self.shoppingcart_data }
                    data["is_closed"] = True
                    data["id"] = id_cart
                    response = self.client.post(self.url, data, **self.auth_headers)
                    if response.status_code == status.HTTP_200_OK:
                        r_json = response.json()
                        self.assertTrue(r_json["cart"]["is_closed"])
                self.assertIsNotNone(id_cart)
            self.assertIsNotNone(id_prod)
        self.assertIsNotNone(id)

    
    def test_shoppingcart_must_not_update_if_closed(self):
        """
        Test for update cart view if it is closed
        """
        # first we create a customer
        id = self._create_model("customer", self.customer_data, ["name", "email", "phone"])
        if id:
            # then we create a product
            id_prod = self._create_model("product", self.product_data, ["name", "description", "image_link", "price"])
            if id_prod:
                # then we can create the closed shoppingcart
                data = self.shoppingcart_data
                data["customer_id"] = id
                data["product_id"] = id
                data["is_closed"] = True
                id_cart = self._create_model("shoppingcart", data, ["quantity", "discount_value", "is_closed"])
                if id_cart:
                    # then check for fail in update shoppingcart
                    self.url = reverse("update-shoppingcart")
                    data["id"] = id_cart
                    response = self.client.post(self.url, data, **self.auth_headers)
                    self.assertNotEqual(response.status_code, status.HTTP_200_OK)
                self.assertIsNotNone(id_cart)
            self.assertIsNotNone(id_prod)
        self.assertIsNotNone(id)
    # END Testing Update Soppingcart View


    # Testing Auth Token
    def test_auth_token_valid_user(self):
        """
        This test case checks if auth token method works with a 
        designed pair of username and password keys
        """
        self.url = "/auth"
        ok_pass_user = { **self.auth_user }
        response = self.client.post(self.url, ok_pass_user)
        self.assertEqual(200, response.status_code)
    

    def test_auth_token_invalid_password(self):
        """
        This test case checks if auth token method fails when wrong password is informed
        """
        self.url = "/auth"
        wrong_pass_user = { **self.auth_user }
        wrong_pass_user["password"] = "1234567"
        response = self.client.post(self.url, wrong_pass_user)
        # for wrong password must not be status code 200!
        self.assertNotEqual(200, response.status_code)
    # END Testing Auth Token