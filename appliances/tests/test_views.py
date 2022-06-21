from unicodedata import category
from django.test import TestCase
from django.urls import reverse
from appliances.models import Appliance, Brand, Category, Solution
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

        self.notAuthenticatedClient = APIClient()

    def test_list_brand_with_authenticated_user(self):
        response = self.authenticatedClient.get(
            reverse("appliances:brand_list"), format="json"
        )
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 2)

    def test_list_brand_with_not_authenticated_user(self):
        response = self.notAuthenticatedClient.get(
            reverse("appliances:brand_list"), format="json"
        )
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 2)


class CategoryViewTest(TestCase):
    def setUp(self):
        self.Category1 = Category.objects.create(name="cat1")
        self.Category2 = Category.objects.create(name="cat2")

        self.user1 = User.objects.create_user("root1", "email1@exemple.com", "root")

        self.authenticatedClient = APIClient()
        self.authenticatedClient.force_authenticate(self.user1)

        self.notAuthenticatedClient = APIClient()

    def test_list_category_with_authenticated_user(self):
        response = self.authenticatedClient.get(
            reverse("appliances:category_list"), format="json"
        )
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 2)

    def test_list_category_with_not_authenticated_user(self):
        response = self.notAuthenticatedClient.get(
            reverse("appliances:category_list"), format="json"
        )
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 2)


class ApplianceViewTest(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name="cat1")
        self.category2 = Category.objects.create(name="cat2")

        self.brand1 = Brand.objects.create(name="Brand1")
        self.brand2 = Brand.objects.create(name="Brand2")

        self.appliance1 = Appliance.objects.create(
            model="BRW15ABANA", category=self.category1, brand=self.brand1
        )
        self.appliance2 = Appliance.objects.create(
            model="BRW17ABANA", category=self.category2, brand=self.brand1
        )
        self.appliance3 = Appliance.objects.create(
            model="BRW18ABANA", category=self.category2, brand=self.brand2
        )

        self.user1 = User.objects.create_user("root1", "email1@exemple.com", "root")

        self.authenticatedClient = APIClient()
        self.authenticatedClient.force_authenticate(self.user1)

        self.notAuthenticatedClient = APIClient()

    def test_list_appliances_with_authenticated_user(self):
        response = self.authenticatedClient.get(
            reverse("appliances:appliance_list"), format="json"
        )
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 3)

    def test_list_appliances_with_not_authenticated_user(self):
        response = self.notAuthenticatedClient.get(
            reverse("appliances:appliance_list"), format="json"
        )
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 3)


class SolutionViewTest(TestCase):
    def setUp(self):
        self.solution1 = Solution.objects.create(
            name="solution1", description="solution1description"
        )
        self.solution2 = Solution.objects.create(
            name="solution2", description="solution2description"
        )
        self.solution3 = Solution.objects.create(
            name="solution3", description="solution3description"
        )

        self.user1 = User.objects.create_user("root1", "email1@exemple.com", "root")

        self.authenticatedClient = APIClient()
        self.authenticatedClient.force_authenticate(self.user1)

        self.notAuthenticatedClient = APIClient()

    def test_list_solutions_with_authenticated_user(self):
        response = self.authenticatedClient.get(
            reverse("appliances:solution_list"), format="json"
        )
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 3)
