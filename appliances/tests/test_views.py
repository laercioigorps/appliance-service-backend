from django.test import TestCase
from django.urls import reverse
from appliances.models import Brand
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import io
from rest_framework.parsers import JSONParser


class BrandViewTest(TestCase):
    def setUp(self):
        self.brand1 = Brand.objects.create(name="Brand1")
        self.brand2 = Brand.objects.create(name="Brand2")

        self.user1 = User.objects.create_user("root1", "email1@exemple.com", "root")

        self.authenticatedClient = APIClient()
        self.authenticatedClient.force_authenticate(self.user1)

    def test_list_brand_with_authenticated_user(self):
        response = self.authenticatedClient.get(
            reverse("appliances:brand_list"), format="json"
        )
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 2)
