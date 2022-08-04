from datetime import date, timedelta
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from appliances.tests.factories import ApplianceFactory
from profiles.models import Customer
from profiles.tests.factories import AddressFactory, CustomerFactory, UserFactory
from service.models import Service, Status
from rest_framework.test import APIClient
import io
from rest_framework.parsers import JSONParser
from service.services import InitialSampleDataCreation

from service.tests.factories import ServiceFactory


class ServiceViewTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()

        self.user1Client = APIClient()
        self.user1Client.force_authenticate(user=self.user1)

        self.user2Client = APIClient()
        self.user2Client.force_authenticate(user=self.user2)

        self.customer1 = CustomerFactory(
            owner=self.user1.profile.org, addresses=(AddressFactory(), AddressFactory())
        )
        self.service1 = ServiceFactory(
            owner=self.user1.profile.org,
            customer=self.customer1,
            address=self.customer1.addresses.first(),
        )
        self.service1.historic.appliance = ApplianceFactory()
        self.service1.historic.save()

        self.customer2 = CustomerFactory(
            owner=self.user2.profile.org, addresses=(AddressFactory(), AddressFactory())
        )
        self.service2 = ServiceFactory(
            owner=self.user2.profile.org,
            customer=self.customer2,
            address=self.customer2.addresses.first(),
        )

        self.service3 = ServiceFactory(owner=self.user1.profile.org)

        self.notAuthenticatedClient = APIClient()

    def test_list_services_by_user_org(self):
        serviceCount = Service.objects.filter(owner=self.user1.profile.org).count()
        self.assertEqual(serviceCount, 2)

        response = self.user1Client.get(reverse("service:service_list"), format="json")

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 2)

        self.assertEqual(data[0]["customer"]["name"], self.service1.customer.name)
        self.assertEqual(data[0]["address"]["number"], self.service1.address.number)
        self.assertEqual(
            data[0]["historic"]["appliance"]["model"],
            self.service1.historic.appliance.model,
        )
        self.assertEqual(data[0]["price"], str(self.service1.price))

    def test_list_services_with_not_authenticated_user(self):
        response = self.notAuthenticatedClient.get(
            reverse("service:service_list"), format="json"
        )
        self.assertEqual(response.status_code, 401)

    def test_create_service_only_with_required_data(self):
        serviceCount = Service.objects.filter(owner=self.user1.profile.org).count()
        self.assertEqual(serviceCount, 2)

        response = self.user1Client.post(reverse("service:service_list"), format="json")

        self.assertEqual(response.status_code, 201)

        serviceCount = Service.objects.filter(owner=self.user1.profile.org).count()
        self.assertEqual(serviceCount, 3)

    def test_create_service_with_not_authenticated_user(self):
        response = self.notAuthenticatedClient.post(
            reverse("service:service_list"), format="json"
        )
        self.assertEqual(response.status_code, 401)

    def test_get_service_detail_with_valid_user(self):
        response = self.user1Client.get(
            reverse("service:service_detail", kwargs={"service_pk": self.service1.id}),
            format="json",
        )
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data["customer"]["name"], self.service1.customer.name)
        self.assertEqual(data["address"]["number"], self.service1.address.number)
        self.assertEqual(data["price"], str(self.service1.price))

    def test_get_service_detail_with_not_authenticated_user(self):
        response = self.notAuthenticatedClient.get(
            reverse("service:service_detail", kwargs={"service_pk": self.service1.id}),
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_get_not_valid_service_detail_with_authenticated_user(self):
        response = self.user1Client.get(
            reverse("service:service_detail", kwargs={"service_pk": 100}),
            format="json",
        )
        self.assertEqual(response.status_code, 404)

    def test_get_service_detail_wich_the_user_does_not_own(self):
        response = self.user2Client.get(
            reverse("service:service_detail", kwargs={"service_pk": self.service1.id}),
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_create_service_for_valid_user(self):
        serviceCount = Service.objects.filter(customer=self.customer1).count()

        response = self.user1Client.post(
            reverse(
                "service:customer_service_list",
                kwargs={"customer_pk": self.customer1.id},
            ),
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        newServiceCount = Service.objects.filter(customer=self.customer1).count()
        self.assertEqual(newServiceCount, serviceCount + 1)

    def test_create_service_for_customer_with_not_authenticated_user(self):
        serviceCount = Service.objects.filter(customer=self.customer1).count()

        response = self.notAuthenticatedClient.post(
            reverse(
                "service:customer_service_list",
                kwargs={"customer_pk": self.customer1.id},
            ),
            format="json",
        )

        self.assertEqual(response.status_code, 401)

        newServiceCount = Service.objects.filter(customer=self.customer1).count()
        self.assertEqual(newServiceCount, serviceCount)

    def test_create_service_for_customer_wich_the_user_does_not_own(self):
        response = self.user1Client.post(
            reverse(
                "service:customer_service_list",
                kwargs={"customer_pk": self.customer2.id},
            ),
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_create_service_for_invalid_customer(self):
        response = self.user1Client.post(
            reverse(
                "service:customer_service_list",
                kwargs={"customer_pk": 100},
            ),
            format="json",
        )
        self.assertEqual(response.status_code, 404)

    def test_partially_update_service_with_price_using_valid_user(self):
        response = self.user1Client.put(
            reverse("service:service_detail", kwargs={"service_pk": self.service1.id}),
            {"price": 125.99},
            format="json",
        )
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(data["price"], str(125.99))

    def test_partially_update_service_with_price_using_not_valid_user(self):
        response = self.user2Client.put(
            reverse("service:service_detail", kwargs={"service_pk": self.service1.id}),
            {"price": 125.99},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_partially_update_service_with_price_using_not_authenticated_user(self):
        client = APIClient()
        response = client.put(
            reverse("service:service_detail", kwargs={"service_pk": self.service1.id}),
            {"price": 125.99},
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_partially_update_service_with_price_using_not_valid_data(self):
        client = APIClient()
        response = self.user1Client.put(
            reverse("service:service_detail", kwargs={"service_pk": self.service1.id}),
            {"price": "testing"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_partially_update_service_with_address_using_valid_user(self):
        address = AddressFactory()
        response = self.user1Client.put(
            reverse("service:service_detail", kwargs={"service_pk": self.service1.id}),
            {"address": address.id},
            format="json",
        )
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data["address"], address.id)

    def test_update_service_with_conclusive_status_using_valid_user(self):

        self.assertEqual(self.service1.status, None)
        self.assertEqual(self.service1.end_date, None)

        conclusive = Status.objects.create(
            name="completed", description="completed", is_conclusive=True
        )

        response = self.user1Client.put(
            reverse("service:service_detail", kwargs={"service_pk": self.service1.id}),
            {"status": conclusive.id},
            format="json",
        )
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data["status"], conclusive.id)
        self.assertEqual(data["end_date"], date.today().strftime("%Y-%m-%d"))


class ServiceHistoryTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user1Client = APIClient()
        self.user1Client.force_authenticate(user=self.user1)

        instructions = [
            {"month": 1, "year": 2021, "count": 2},
            {"month": 2, "year": 2021, "count": 1},
            {"month": 1, "year": 2022, "count": 5},
            {"month": 2, "year": 2022, "count": 4},
            {"month": 3, "year": 2022, "count": 3},
            {"month": 4, "year": 2022, "count": 2},
            {"month": 5, "year": 2022, "count": 1},
        ]
        for instruction in instructions:
            for i in range(instruction["count"]):
                ServiceFactory(
                    owner=self.user1.profile.org,
                    end_date=date(
                        year=instruction["year"], month=instruction["month"], day=15
                    ),
                    price=Decimal("100"),
                )

    def test_setUP(self):
        serviceCount = Service.objects.count()
        self.assertEqual(serviceCount, 18)

    def test_service_income_history_data_using_valid_user(self):
        response = self.user1Client.get(
            reverse("service:service_history"), format="json"
        )

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data["incomeHistoryData"], [200, 100, 500, 400, 300, 200, 100])

    def test_service_income_history_data_using_now_authenticated_user(self):
        client = APIClient()
        response = client.get(reverse("service:service_history"), format="json")

        self.assertEqual(response.status_code, 401)

    def test_service_income_history_labels_using_valid_user(self):
        response = self.user1Client.get(
            reverse("service:service_history"), format="json"
        )

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(
            data["incomeHistoryLabels"],
            ["1-2021", "2-2021", "1-2022", "2-2022", "3-2022", "4-2022", "5-2022"],
        )

    def test_service_count_history_data_using_valid_user(self):
        response = self.user1Client.get(
            reverse("service:service_history"), format="json"
        )

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(
            data["serviceCountHistoryData"],
            [2, 1, 5, 4, 3, 2, 1],
        )

    def test_add_services_with_no_end_date(self):
        for i in range(5):
            service = ServiceFactory(owner=self.user1.profile.org, price=50)

        response = self.user1Client.get(
            reverse("service:service_history"), format="json"
        )

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(
            data["serviceCountHistoryData"],
            [2, 1, 5, 4, 3, 2, 1],
        )
        self.assertEqual(
            data["incomeHistoryLabels"],
            ["1-2021", "2-2021", "1-2022", "2-2022", "3-2022", "4-2022", "5-2022"],
        )
        self.assertEqual(data["incomeHistoryData"], [200, 100, 500, 400, 300, 200, 100])


class StatusViewTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user1Client = APIClient()
        self.user1Client.force_authenticate(user=self.user1)

        self.status1 = Status.objects.create(name="Visit Scheduled")
        self.status2 = Status.objects.create(name="waiting approval")
        self.status3 = Status.objects.create(name="Analysis")
        self.status4 = Status.objects.create(name="Waiting Payment")
        self.status5 = Status.objects.create(name="Completed")
        self.status6 = Status.objects.create(name="Cancelled")

        instructions = {
            str(self.status1.id): 5,
            str(self.status2.id): 4,
            str(self.status3.id): 3,
            str(self.status4.id): 2,
            str(self.status5.id): 1,
            str(self.status6.id): 3,
        }
        self.values = list(instructions.values())

        self.serviceCount = sum(self.values)

        self.keys = [int(x) for x in instructions.keys()]

        for key in self.keys:
            count = instructions[str(key)]
            for i in range(count):
                service = ServiceFactory(
                    owner=self.user1.profile.org, status=Status.objects.get(pk=key)
                )

        oldService = ServiceFactory(
            owner=self.user1.profile.org,
            status=self.status5,
            start_date=date.today() - timedelta(days=90),
        )

    def test_initial_service_count(self):
        count = Service.objects.filter(owner=self.user1.profile.org).count()
        self.assertEqual(self.serviceCount + 1, count)

    def test_list_status_using_authenticated_user(self):
        response = self.user1Client.get(reverse("service:status_list"), format="json")

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 6)

        self.assertEqual(data[0]["name"], self.status1.name)
        self.assertEqual(data[1]["name"], self.status2.name)
        self.assertEqual(data[2]["name"], self.status3.name)

    def test_service_count_order_by_status_using_valid_user(self):
        response = self.user1Client.get(
            reverse("service:services_status_count", kwargs={"days": 30}), format="json"
        )

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(
            data["labels"],
            [
                self.status1.name,
                self.status2.name,
                self.status3.name,
                self.status4.name,
                self.status5.name,
                self.status6.name,
            ],
        )
        self.assertEqual(data["data"], self.values)

    def test_service_count_order_by_status_in_last_90_days_using_valid_user(self):
        response = self.user1Client.get(
            reverse("service:services_status_count", kwargs={"days": 90}), format="json"
        )

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(
            data["labels"],
            [
                self.status1.name,
                self.status2.name,
                self.status3.name,
                self.status4.name,
                self.status5.name,
                self.status6.name,
            ],
        )
        val = self.values
        val[4] += 1
        self.assertEqual(data["data"], val)

    def test_service_count_order_by_status_with_null_services_using_valid_user(self):
        service = ServiceFactory(
            owner=self.user1.profile.org,
        )
        response = self.user1Client.get(
            reverse("service:services_status_count", kwargs={"days": 90}), format="json"
        )

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(
            data["labels"],
            [
                self.status1.name,
                self.status2.name,
                self.status3.name,
                self.status4.name,
                self.status5.name,
                self.status6.name,
                "null",
            ],
        )
        self.assertEqual(data["data"], [5, 4, 3, 2, 2, 3, 1])


class TopCustomerTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user1Client = APIClient()
        self.user1Client.force_authenticate(user=self.user1)

        self.completed = Status.objects.create(
            name="completed", description="completed", is_conclusive=True
        )

        self.customer1 = CustomerFactory(owner=self.user1.profile.org)
        self.customer2 = CustomerFactory(owner=self.user1.profile.org)
        self.customer3 = CustomerFactory(owner=self.user1.profile.org)
        self.customer4 = CustomerFactory(owner=self.user1.profile.org)
        self.customer5 = CustomerFactory(owner=self.user1.profile.org)
        self.customer6 = CustomerFactory(owner=self.user1.profile.org)

        instructions = [
            {"customer": self.customer1, "quantity": 2, "total_price": 1500},
            {"customer": self.customer2, "quantity": 10, "total_price": 500},
            {"customer": self.customer3, "quantity": 5, "total_price": 400},
            {"customer": self.customer4, "quantity": 3, "total_price": 600},
            {"customer": self.customer5, "quantity": 2, "total_price": 200},
            {"customer": self.customer6, "quantity": 2, "total_price": 100},
        ]

        self.serviceCount = 0

        for instruction in instructions:
            for i in range(instruction["quantity"]):
                service = ServiceFactory(
                    owner=self.user1.profile.org,
                    customer=instruction["customer"],
                    price=instruction["total_price"] / instruction["quantity"],
                    status=self.completed,
                    end_date=date.today(),
                )
                self.serviceCount += 1

    def test_setUp(self):
        customerCount = Customer.objects.count()
        self.assertEqual(customerCount, 6)

        serviceCount = Service.objects.count()
        self.assertEqual(24, serviceCount)

    def test_top_5_customer_income_with_valid_user(self):
        quantity = 5
        response = self.user1Client.get(
            reverse("service:top_customers_income", kwargs={"quantity": quantity}),
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), quantity)

        self.assertEqual(data[0]["customer__id"], self.customer1.id)
        self.assertEqual(data[1]["customer__id"], self.customer4.id)
        self.assertEqual(data[2]["customer__id"], self.customer2.id)
        self.assertEqual(data[3]["customer__id"], self.customer3.id)
        self.assertEqual(data[4]["customer__id"], self.customer5.id)

        self.assertEqual(data[0]["income"], 1500)
        self.assertEqual(data[1]["income"], 600)
        self.assertEqual(data[2]["income"], 500)
        self.assertEqual(data[3]["income"], 400)
        self.assertEqual(data[4]["income"], 200)

        self.assertEqual(data[0]["services"], 2)
        self.assertEqual(data[1]["services"], 3)
        self.assertEqual(data[2]["services"], 10)
        self.assertEqual(data[3]["services"], 5)
        self.assertEqual(data[4]["services"], 2)

    def test_top_5_customer_service_count_with_valid_user(self):
        quantity = 5
        response = self.user1Client.get(
            reverse("service:top_customers_services", kwargs={"quantity": quantity}),
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), quantity)

        self.assertEqual(data[0]["customer__id"], self.customer2.id)
        self.assertEqual(data[1]["customer__id"], self.customer3.id)
        self.assertEqual(data[2]["customer__id"], self.customer4.id)
        self.assertEqual(data[3]["customer__id"], self.customer1.id)
        self.assertEqual(data[4]["customer__id"], self.customer5.id)

        self.assertEqual(data[0]["income"], 500)
        self.assertEqual(data[1]["income"], 400)
        self.assertEqual(data[2]["income"], 600)
        self.assertEqual(data[3]["income"], 1500)
        self.assertEqual(data[4]["income"], 200)

        self.assertEqual(data[0]["services"], 10)
        self.assertEqual(data[1]["services"], 5)
        self.assertEqual(data[2]["services"], 3)
        self.assertEqual(data[3]["services"], 2)
        self.assertEqual(data[4]["services"], 2)


class SampleDataCreateViewTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user1Client = APIClient()
        self.user1Client.force_authenticate(user=self.user1)

        self.initialData = InitialSampleDataCreation()
        self.setTestStatuses()
        self.generateInitialData()

    def generateInitialData(self):
        self.initialData.generateRandomBrands(3)
        self.initialData.generateRandomCategories(3)
        self.initialData.generateRandomAppliances(5)
        self.initialData.generateRandomSymptoms(10)
        self.initialData.generateRandomProblems(10)
        self.initialData.generateRandomSolutions(10)
        self.initialData.statuses = list(Status.objects.all())

    def setTestStatuses(self):
        self.awaiting = Status.objects.create(
            name="Scheduled visit", description="Scheduled visit"
        )
        self.completed = Status.objects.create(
            name="Waiting for approval", description="Waiting for approval"
        )
        self.completed = Status.objects.create(
            name="Scheduled service", description="Scheduled service"
        )
        self.completed = Status.objects.create(
            name="Awaiting payment", description="Awaiting payment"
        )
        self.completed = Status.objects.create(
            name="Concluded", description="Concluded", is_conclusive=True
        )
        self.completed = Status.objects.create(name="Canceled", description="Canceled")

    def test_create_sample_data_for_new_user_with_valid_client(self):
        response = self.user1Client.post(
            reverse("service:sample_creation"), format="json"
        )
        self.assertEqual(response.status_code, 201)

        self.assertEqual(
            Service.objects.filter(owner=self.user1.profile.org).count(), 100
        )
        self.assertEqual(
            Customer.objects.filter(owner=self.user1.profile.org).count(), 100
        )

    def test_create_sample_data_with_not_authenticated_user(self):
        client = APIClient()
        response = self.client.post(reverse("service:sample_creation"), format="json")
        self.assertEqual(response.status_code, 401)

    def test_created_sample_data_has_different_dates_in_6_month_range(self):
        startDate = date.today() - timedelta(days=30 * 6)
        endDate = date.today()

        response = self.user1Client.post(
            reverse("service:sample_creation"), format="json"
        )
        self.assertEqual(response.status_code, 201)

        services = Service.objects.all()[:10]
        inDateRange = True
        dates = []
        for service in services:
            if service.start_date < startDate or service.start_date > endDate:
                inDateRange = False
                break
            if service.start_date not in dates:
                dates.append(service.start_date)
        self.assertTrue(inDateRange)
        self.assertGreater(len(dates), 5)

    def test_set_customer_and_services_quantity_to_create(self):
        response = self.user1Client.post(
            reverse("service:sample_creation"),
            {"customers": 3, "services": 5},
            format="json",
        )
        self.assertEqual(response.status_code, 201)

        self.assertEqual(
            Service.objects.filter(owner=self.user1.profile.org).count(), 5
        )
        self.assertEqual(
            Customer.objects.filter(owner=self.user1.profile.org).count(), 3
        )
