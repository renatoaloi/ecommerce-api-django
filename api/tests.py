from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
import json

class TestEcommerceApi(TestCase):
    """
    This class contains tests for ecommerce API
    """

    def setUp(self):
        """
        This method runs before execution of each test case
        """
        self.client = Client()
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


    def test_health_check(self):
        """
        This test case checks if health check endpoint is responsive
        """
        self.url = reverse("health-check")
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)


    def test_customer_list(self):
        """
        This test case checks if customer list endpoint is working as expected
        """
        self.url = reverse("customer-list")
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    
    def _create_model(self, model, data, fields):
        self.url = reverse("{}-list".format(model))
        response = self.client.post(self.url, data)
        if response.status_code == status.HTTP_201_CREATED:
            r_json = response.json()
            # check for the fields
            expected = {}
            for f in fields:
                expected[f] = r_json[f]
            # trying a more pythonic way
            #fs = [{[f]: r_json[f]} for f in fields] #failed
            self.assertJSONEqual(json.dumps(expected), json.dumps(data))
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
            for f in fields:
                expected[f] = r_json[f]
            self.assertJSONEqual(json.dumps(expected), json.dumps(data))
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
