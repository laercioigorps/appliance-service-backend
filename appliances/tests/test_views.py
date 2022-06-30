from pydoc import describe
from unicodedata import category
from django.test import TestCase
from django.urls import reverse
from appliances.models import (
    Appliance,
    Brand,
    Category,
    Historic,
    Problem,
    Solution,
    Symptom,
)
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import io
from rest_framework.parsers import JSONParser
from appliances.tests.factories import (
    HistoricFactory,
    ProblemFactory,
    SolutionFactory,
    SymptomFactory,
)


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

        self.assertEqual(data[0]["name"], self.brand1.name)
        self.assertEqual(data[0]["id"], self.brand1.id)

        self.assertEqual(data[1]["name"], "Brand2")

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
        self.category1 = Category.objects.create(name="cat1")
        self.category2 = Category.objects.create(name="cat2")

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

        self.assertEqual(data[0]["name"], self.category1.name)
        self.assertEqual(data[0]["id"], self.category1.id)

        self.assertEqual(data[1]["name"], self.category2.name)

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

        self.assertEqual(data[0]["model"], self.appliance1.model)
        self.assertEqual(data[0]["id"], self.appliance1.id)
        self.assertEqual(data[0]["brand"], self.appliance1.brand.id)
        self.assertEqual(data[0]["category"], self.appliance1.category.id)

        self.assertEqual(data[1]["model"], self.appliance2.model)
        self.assertEqual(data[2]["model"], self.appliance3.model)

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

        self.assertEqual(data[0]["id"], self.solution1.id)
        self.assertEqual(data[0]["name"], self.solution1.name)
        self.assertEqual(data[0]["description"], self.solution1.description)

        self.assertEqual(data[1]["name"], "solution2")

    def test_list_solutions_with_not_authenticated_user(self):
        response = self.notAuthenticatedClient.get(
            reverse("appliances:solution_list"), format="json"
        )
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 3)


class ProblemViewTest(TestCase):
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

        self.problem1 = Problem.objects.create(
            name="Problem1", description="problem1Description"
        )
        self.problem2 = Problem.objects.create(
            name="Problem2", description="problem2Description"
        )
        self.problem3 = Problem.objects.create(
            name="Problem3", description="problem3Description"
        )
        self.problem4 = Problem.objects.create(
            name="Problem4", description="problem4Description"
        )

        self.problem1.solutions.add(self.solution1)
        self.problem2.solutions.add(self.solution2)
        self.problem3.solutions.add(self.solution3)
        self.problem4.solutions.add(self.solution3)

        self.user1 = User.objects.create_user("root1", "email1@exemple.com", "root")

        self.authenticatedClient = APIClient()
        self.authenticatedClient.force_authenticate(self.user1)

        self.notAuthenticatedClient = APIClient()

    def test_list_problems_with_authenticated_user(self):
        response = self.authenticatedClient.get(
            reverse("appliances:problem_list"), format="json"
        )
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 4)

        self.assertEqual(data[0]["id"], self.problem1.id)
        self.assertEqual(data[0]["name"], self.problem1.name)
        self.assertEqual(data[0]["description"], self.problem1.description)
        self.assertEqual(data[0]["solutions"][0], self.problem1.solutions.first().id)

        self.assertEqual(data[1]["name"], "Problem2")
        self.assertEqual(data[2]["name"], "Problem3")
        self.assertEqual(data[3]["name"], "Problem4")


class SymptomViewTest(TestCase):
    def setUp(self):
        self.problem1 = Problem.objects.create(
            name="Problem1", description="problem1Description"
        )
        self.problem2 = Problem.objects.create(
            name="Problem2", description="problem2Description"
        )
        self.problem3 = Problem.objects.create(
            name="Problem3", description="problem3Description"
        )
        self.problem4 = Problem.objects.create(
            name="Problem4", description="problem4Description"
        )

        self.symptom1 = Symptom.objects.create(
            name="symptom1", description="symptom1description"
        )
        self.symptom2 = Symptom.objects.create(
            name="symptom2", description="symptom2description"
        )

        self.symptom1.causes.add(self.problem1)
        self.symptom1.causes.add(self.problem2)
        self.symptom2.causes.add(self.problem1)

        self.user1 = User.objects.create_user("root1", "email1@exemple.com", "root")

        self.authenticatedClient = APIClient()
        self.authenticatedClient.force_authenticate(self.user1)

        self.notAuthenticatedClient = APIClient()

    def test_list_symptoms_with_authenticated_user(self):
        response = self.authenticatedClient.get(
            reverse("appliances:symptom_list"), format="json"
        )
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 2)

        self.assertEqual(data[0]["id"], self.symptom1.id)
        self.assertEqual(data[0]["name"], self.symptom1.name)
        self.assertEqual(data[0]["description"], self.symptom1.description)
        self.assertEqual(data[0]["causes"][0], self.symptom1.causes.first().id)

        self.assertEqual(data[1]["name"], self.symptom2.name)

    def test_list_symptoms_with_not_authenticated_user(self):
        response = self.notAuthenticatedClient.get(
            reverse("appliances:symptom_list"), format="json"
        )
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 2)

        self.assertEqual(data[0]["name"], "symptom1")
        self.assertEqual(data[1]["name"], "symptom2")


class HistoricViewTest(TestCase):
    def setUp(self):

        self.user1 = User.objects.create_user("root1", "email1@exemple.com", "root")
        self.user2 = User.objects.create_user("root2", "email1@exemple.com", "root")

        self.authenticatedClient = APIClient()
        self.authenticatedClient.force_authenticate(self.user1)

        self.notAuthenticatedClient = APIClient()

        self.historic1 = Historic.objects.create(org=self.user1.profile.org)
        self.h2 = Historic.objects.create(org=self.user1.profile.org)

        self.h3 = Historic.objects.create(org=self.user2.profile.org)

    def test_list_historic_with_authenticated_user(self):
        response = self.authenticatedClient.get(
            reverse("appliances:historic_list"), format="json"
        )
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 2)

        self.assertEqual(data[0]["id"], self.historic1.id)
        self.assertEqual(data[0]["org"], self.user1.profile.org.id)
        self.assertEqual(data[0]["completed"], self.historic1.completed)

        self.assertEqual(data[1]["org"], self.user1.profile.org.id)

    def test_list_historic_with_not_authenticated_user(self):
        response = self.notAuthenticatedClient.get(
            reverse("appliances:historic_list"), format="json"
        )
        self.assertEqual(response.status_code, 403)

    def test_get_historic_detail_using_valid_authenticated_user(self):
        historic = HistoricFactory(
            symptoms=(SymptomFactory(), SymptomFactory()),
            problems=(ProblemFactory(), ProblemFactory()),
            solutions=(SolutionFactory(), SolutionFactory()),
            org=self.user1.profile.org,
        )

        response = self.authenticatedClient.get(
            reverse("appliances:historic_detail", kwargs={"historic_pk": historic.id}),
            format="json",
        )
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        # assert fields are equal
        self.assertEqual(data["completed"], False)
        self.assertEqual(
            data["symptoms"],
            [historic.symptoms.all()[0].id, historic.symptoms.all()[1].id],
        )
        self.assertEqual(
            data["problems"],
            [historic.problems.all()[0].id, historic.problems.all()[1].id],
        )
        self.assertEqual(
            data["solutions"],
            [historic.solutions.all()[0].id, historic.solutions.all()[1].id],
        )
        self.assertEqual(data["appliance"], historic.appliance.id)

    def test_get_historic_detail_using_not_authenticated_user(self):

        response = self.notAuthenticatedClient.get(
            reverse(
                "appliances:historic_detail", kwargs={"historic_pk": self.historic1.id}
            ),
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_get_historic_detail_wich_authenticated_user_does_not_own(self):

        response = self.authenticatedClient.get(
            reverse("appliances:historic_detail", kwargs={"historic_pk": self.h3.id}),
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_get_invalid_historic_detail_with_authenticated_user(self):

        response = self.authenticatedClient.get(
            reverse("appliances:historic_detail", kwargs={"historic_pk": 100}),
            format="json",
        )
        self.assertEqual(response.status_code, 404)
