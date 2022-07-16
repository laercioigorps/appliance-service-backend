from datetime import date, timedelta
from django import views
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import io
from rest_framework.parsers import JSONParser

from profiles.models import Address, Customer
from profiles.tests.factories import CustomerFactory


class TestCustomerView(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create_user("root1", "email1@exemple.com", "root")
        self.user2 = User.objects.create_user("root2", "email2@exemple.com", "root")

        self.customer1 = Customer.objects.create(
            name="josé", owner=self.user2.profile.org
        )
        self.customer2 = Customer.objects.create(
            name="Maria", owner=self.user2.profile.org
        )
        self.customer3 = Customer.objects.create(
            name="Pedro", owner=self.user2.profile.org
        )
        self.customer4 = Customer.objects.create(
            name="Pedro", owner=self.user1.profile.org
        )

    def test_create_customer(self):
        customer_count = Customer.objects.all().count()
        self.assertEqual(customer_count, 4)

        client = APIClient()
        client.force_authenticate(user=self.user1)
        response = client.post(
            reverse("profiles:customer_list"), {"name": "customer1"}, format="json"
        )
        self.assertEqual(response.status_code, 201)

        customer_count = Customer.objects.all().count()
        self.assertEqual(customer_count, 5)

    def test_list_customer_by_user_organization(self):
        customer_owned_by_user2_organization = Customer.objects.filter(
            owner=self.user2.profile.org
        ).count()
        self.assertEqual(customer_owned_by_user2_organization, 3)

        client = APIClient()
        client.force_authenticate(user=self.user2)
        response = client.get(reverse("profiles:customer_list"))
        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(len(data), 3)


class TestCustomerDetailView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("root1", "email1@exemple.com", "root")
        self.user2 = User.objects.create_user("root2", "email2@exemple.com", "root")

        self.customer1 = Customer.objects.create(
            name="josé", owner=self.user2.profile.org
        )
        self.customer2 = Customer.objects.create(
            name="Maria", owner=self.user2.profile.org
        )
        self.customer3 = Customer.objects.create(
            name="Pedro", owner=self.user2.profile.org
        )
        self.customer4 = Customer.objects.create(
            name="Pedro", owner=self.user1.profile.org
        )

    def test_get_customer_with_valid_user(self):
        client = APIClient()
        client.force_authenticate(self.user1)

        response = client.get(
            reverse("profiles:customer_detail", kwargs={"pk": self.customer4.id}),
            format="json",
        )

        self.assertEquals(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data["name"], self.customer4.name)
        self.assertEqual(data["id"], self.customer4.id)

    def test_get_customer_fields(self):
        client = APIClient()
        client.force_authenticate(self.user1)

        customer = CustomerFactory(owner=self.user1.profile.org)

        response = client.get(
            reverse("profiles:customer_detail", kwargs={"pk": customer.id}),
            format="json",
        )

        self.assertEquals(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data["name"], customer.name)
        self.assertEqual(data["nickname"], customer.nickname)
        self.assertEqual(data["email"], customer.email)
        self.assertEqual(data["profession"], customer.profession)
        self.assertEqual(data["phone1"], customer.phone1)
        self.assertEqual(data["phone2"], customer.phone2)
        self.assertEqual(data["owner"], customer.owner.id)
        self.assertEqual(data["created_at"], customer.created_at.strftime("%Y-%m-%d"))

    def test_get_customer_with_not_authenticated_user(self):
        client = APIClient()

        response = client.get(
            reverse("profiles:customer_detail", kwargs={"pk": self.customer4.id}),
            format="json",
        )

        self.assertEquals(response.status_code, 403)

    def test_get_invalid_customer_with_authenticated_user(self):
        client = APIClient()
        client.force_authenticate(self.user1)
        response = client.get(
            reverse("profiles:customer_detail", kwargs={"pk": 100}),
            format="json",
        )

        self.assertEquals(response.status_code, 404)

    def test_get_customer_wich_authenticated_user_dont_own(self):
        client = APIClient()
        client.force_authenticate(self.user1)
        response = client.get(
            reverse("profiles:customer_detail", kwargs={"pk": self.customer1.id}),
            format="json",
        )

        self.assertEquals(response.status_code, 403)

    def test_update_customer_with_authenticated_user(self):
        client = APIClient()
        client.force_authenticate(self.user2)
        response = client.put(
            reverse("profiles:customer_detail", kwargs={"pk": self.customer1.id}),
            {"name": "new name", "owner": self.customer1.owner.id},
            format="json",
        )

        self.assertEquals(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data["name"], "new name")

    def test_update_invalid_customer_with_authenticated_user(self):
        client = APIClient()
        client.force_authenticate(self.user2)
        response = client.put(
            reverse("profiles:customer_detail", kwargs={"pk": 100}),
            {"name": "new name", "owner": self.customer1.owner.id},
            format="json",
        )

        self.assertEquals(response.status_code, 404)

    def test_update_customer_with_invalid_data(self):
        client = APIClient()
        client.force_authenticate(self.user2)
        response = client.put(
            reverse("profiles:customer_detail", kwargs={"pk": self.customer1.id}),
            {"owner": self.customer1.owner.id},
            format="json",
        )

        self.assertEquals(response.status_code, 400)

    def test_delete_customer_with_valid_authenticated_user(self):
        customer_count = Customer.objects.filter(owner=self.user2.profile.org).count()
        self.assertEquals(customer_count, 3)

        client = APIClient()
        client.force_authenticate(self.user2)
        response = client.delete(
            reverse("profiles:customer_detail", kwargs={"pk": self.customer1.id}),
            format="json",
        )

        self.assertEquals(response.status_code, 200)

        customer_count = Customer.objects.filter(owner=self.user2.profile.org).count()
        self.assertEquals(customer_count, 2)

    def test_delete_customer_with_not_authenticated_user(self):
        customer_count = Customer.objects.filter(owner=self.user2.profile.org).count()
        self.assertEquals(customer_count, 3)

        client = APIClient()

        response = client.delete(
            reverse("profiles:customer_detail", kwargs={"pk": self.customer1.id}),
            format="json",
        )

        self.assertEquals(response.status_code, 403)

        customer_count = Customer.objects.filter(owner=self.user2.profile.org).count()
        self.assertEquals(customer_count, 3)

    def test_delete_customer_wich_authenticated_user_does_not_own(self):
        customer_count = Customer.objects.filter(owner=self.user2.profile.org).count()
        self.assertEquals(customer_count, 3)

        client = APIClient()
        client.force_authenticate(self.user1)
        response = client.delete(
            reverse("profiles:customer_detail", kwargs={"pk": self.customer1.id}),
            format="json",
        )

        self.assertEquals(response.status_code, 403)

        customer_count = Customer.objects.filter(owner=self.user2.profile.org).count()
        self.assertEquals(customer_count, 3)


class TestCustomerHistoricView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("root1", "email1@exemple.com", "root")

        self.client1Authenticated = APIClient()
        self.client1Authenticated.force_authenticate(self.user1)

        for i in range(4):
            customer = CustomerFactory(
                owner=self.user1.profile.org,
                created_at=date(year=2022, month=1, day=15),
            )
        customer = CustomerFactory(
            owner=self.user1.profile.org,
            created_at=date(year=2022, month=1, day=5),
        )
        for i in range(4):
            customer = CustomerFactory(
                owner=self.user1.profile.org,
                created_at=date(year=2022, month=2, day=15),
            )
        for i in range(3):
            customer = CustomerFactory(
                owner=self.user1.profile.org,
                created_at=date(year=2022, month=3, day=15),
            )
        for i in range(2):
            customer = CustomerFactory(
                owner=self.user1.profile.org,
                created_at=date(year=2022, month=4, day=15),
            )
        for i in range(1):
            customer = CustomerFactory(
                owner=self.user1.profile.org,
                created_at=date(year=2022, month=5, day=15),
            )

    def test_new_customers_history(self):
        customerCount = Customer.objects.all().count()
        self.assertEqual(customerCount, 15)

        response = self.client1Authenticated.get(
            reverse("profiles:customer_history"),
            format="json",
        )
        self.assertEquals(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data["data"], [5, 4, 3, 2, 1])

    def test_get_new_customers_history_with_not_authenticated_user(self):
        client = APIClient()

        response = client.get(
            reverse("profiles:customer_history"),
            format="json",
        )
        self.assertEquals(response.status_code, 403)

    def test_get_new_customers_history_with_different_years(self):

        newCustomer = CustomerFactory(
            owner=self.user1.profile.org, created_at=date(year=2021, month=1, day=17)
        )
        response = self.client1Authenticated.get(
            reverse("profiles:customer_history"),
            format="json",
        )
        self.assertEquals(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data["data"], [1, 5, 4, 3, 2, 1])

    def test_get_new_customers_history_labels(self):

        newCustomer = CustomerFactory(
            owner=self.user1.profile.org, created_at=date(year=2021, month=1, day=17)
        )
        response = self.client1Authenticated.get(
            reverse("profiles:customer_history"),
            format="json",
        )
        self.assertEquals(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(
            data["labels"], ["1-2021", "1-2022", "2-2022", "3-2022", "4-2022", "5-2022"]
        )

    def test_get_new_customers_history_total_customers(self):

        response = self.client1Authenticated.get(
            reverse("profiles:customer_history"),
            format="json",
        )
        self.assertEquals(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data["total"], 15)


class TestAddressView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("root1", "email1@exemple.com", "root")
        self.user2 = User.objects.create_user("root2", "email2@exemple.com", "root")

        self.customer1 = Customer.objects.create(
            name="josé", owner=self.user2.profile.org
        )
        self.customer2 = Customer.objects.create(
            name="Maria", owner=self.user2.profile.org
        )
        self.customer3 = Customer.objects.create(
            name="Pedro", owner=self.user2.profile.org
        )

    def test_create_address_to_custumer_with_authenticated_user(self):
        addressCount = self.customer1.addresses.count()
        self.assertEqual(addressCount, 0)

        client = APIClient()
        client.force_authenticate(user=self.user2)

        response = client.post(
            reverse("profiles:customer_address_list", kwargs={"pk": self.customer1.id}),
            {
                "number": "5",
                "street": "street1",
                "neighborhood": "neighb",
                "city": "San Andreas",
            },
            format="json",
        )
        self.assertEquals(response.status_code, 201)

        addressCount = self.customer1.addresses.count()
        self.assertEqual(addressCount, 1)

    def test_create_address_to_custumer_with_not_authenticated_user(self):
        addressCount = self.customer2.addresses.count()
        self.assertEqual(addressCount, 0)

        client = APIClient()

        response = client.post(
            reverse("profiles:customer_address_list", kwargs={"pk": self.customer2.id}),
            {
                "number": "5",
                "street": "street1",
                "neighborhood": "neighb",
                "city": "San Andreas",
            },
            format="json",
        )
        self.assertEquals(response.status_code, 403)

        addressCount = self.customer2.addresses.count()
        self.assertEqual(addressCount, 0)

    def test_create_address_to_custumer_wich_the_user_organization_not_own(self):
        addressCount = self.customer2.addresses.count()
        self.assertEqual(addressCount, 0)

        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.post(
            reverse("profiles:customer_address_list", kwargs={"pk": self.customer2.id}),
            {
                "number": "5",
                "street": "street1",
                "neighborhood": "neighb",
                "city": "San Andreas",
            },
            format="json",
        )
        self.assertEquals(response.status_code, 403)

        addressCount = self.customer2.addresses.count()
        self.assertEqual(addressCount, 0)

    def test_create_address_to_invalid_customer_with_authenticated_user(self):
        addressCount = Address.objects.all().count()
        self.assertEquals(addressCount, 0)

        client = APIClient()
        client.force_authenticate(user=self.user1)

        response = client.post(
            reverse("profiles:customer_address_list", kwargs={"pk": 100}),
            {
                "number": "5",
                "street": "street1",
                "neighborhood": "neighb",
                "city": "San Andreas",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 404)

        addressCount = Address.objects.all().count()
        self.assertEquals(addressCount, 0)

    def test_create_address_to_custumer_with_not_valid_data(self):
        addressCount = self.customer1.addresses.count()
        self.assertEqual(addressCount, 0)

        client = APIClient()
        client.force_authenticate(user=self.user2)

        response = client.post(
            reverse("profiles:customer_address_list", kwargs={"pk": self.customer1.id}),
            {
                "street": "street1",
                "neighborhood": "neighb",
                "city": "San Andreas",
            },
            format="json",
        )
        self.assertEquals(response.status_code, 400)

        addressCount = self.customer1.addresses.count()
        self.assertEqual(addressCount, 0)


class TestAddressListGetView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("root1", "email1@exemple.com", "root")
        self.user2 = User.objects.create_user("root2", "email2@exemple.com", "root")

        self.customer1 = Customer.objects.create(
            name="josé", owner=self.user2.profile.org
        )
        self.customer2 = Customer.objects.create(
            name="Maria", owner=self.user2.profile.org
        )
        self.customer3 = Customer.objects.create(
            name="Pedro", owner=self.user2.profile.org
        )

        self.address1 = Address.objects.create(
            number="1", street="street1", neighborhood="neigh1"
        )
        self.address2 = Address.objects.create(
            number="2", street="street2", neighborhood="neigh2"
        )
        self.address3 = Address.objects.create(
            number="3", street="street3", neighborhood="neigh3"
        )

        self.customer1.addresses.add(self.address1)
        self.customer1.addresses.add(self.address2)

        self.customer2.addresses.add(self.address3)

    def test_list_address_from_customer_with_authenticated_user(self):

        client = APIClient()
        client.force_authenticate(self.user2)

        response = client.get(
            reverse("profiles:customer_address_list", kwargs={"pk": self.customer1.id})
        )

        self.assertEquals(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(len(data), 2)

        firstAddress = self.customer1.addresses.first()

        self.assertEqual(data[0]["id"], firstAddress.id)
        self.assertEqual(data[0]["number"], firstAddress.number)
        self.assertEqual(data[0]["street"], firstAddress.street)

    def test_list_address_from_customer_with_not_authenticated_user(self):

        client = APIClient()

        response = client.get(
            reverse("profiles:customer_address_list", kwargs={"pk": self.customer1.id})
        )

        self.assertEquals(response.status_code, 403)

    def test_list_address_from_customer_with_invalid_customer_id(self):

        client = APIClient()
        client.force_authenticate(self.user1)

        response = client.get(
            reverse("profiles:customer_address_list", kwargs={"pk": 100})
        )

        self.assertEquals(response.status_code, 404)

    def test_list_address_from_customer_wich_the_user_does_not_own(self):

        client = APIClient()
        client.force_authenticate(self.user1)

        response = client.get(
            reverse("profiles:customer_address_list", kwargs={"pk": self.customer1.id})
        )

        self.assertEquals(response.status_code, 403)


class TestCustomerAddressDetailView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("root1", "email1@exemple.com", "root")
        self.user2 = User.objects.create_user("root2", "email2@exemple.com", "root")

        self.customer1 = Customer.objects.create(
            name="josé", owner=self.user2.profile.org
        )
        self.customer2 = Customer.objects.create(
            name="Maria", owner=self.user2.profile.org
        )
        self.customer3 = Customer.objects.create(
            name="Pedro", owner=self.user2.profile.org
        )

        self.address1 = Address.objects.create(
            number="1", street="street1", neighborhood="neigh1"
        )
        self.address2 = Address.objects.create(
            number="2", street="street2", neighborhood="neigh2"
        )
        self.address3 = Address.objects.create(
            number="3", street="street3", neighborhood="neigh3"
        )

        self.customer1.addresses.add(self.address1)
        self.customer1.addresses.add(self.address2)

        self.customer2.addresses.add(self.address3)

    def test_retrieve_customer_address_with_valid_authenticated_user(self):
        client = APIClient()
        client.force_authenticate(self.user2)

        response = client.get(
            reverse(
                "profiles:customer_address_detail",
                kwargs={"pk": self.customer1.id, "address_pk": self.address1.id},
            )
        )

        self.assertEquals(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data["number"], self.address1.number)
        self.assertEqual(data["street"], self.address1.street)
        self.assertEqual(data["neighborhood"], self.address1.neighborhood)

    def test_retrieve_customer_address_with_not_authenticated_user(self):
        client = APIClient()

        response = client.get(
            reverse(
                "profiles:customer_address_detail",
                kwargs={"pk": self.customer1.id, "address_pk": self.address1.id},
            )
        )

        self.assertEquals(response.status_code, 403)

    def test_retrieve_customer_address_wich_authenticated_user_does_not_own(self):
        client = APIClient()
        client.force_authenticate(self.user1)
        response = client.get(
            reverse(
                "profiles:customer_address_detail",
                kwargs={"pk": self.customer1.id, "address_pk": self.address1.id},
            )
        )

        self.assertEquals(response.status_code, 403)

    def test_retrieve_invalid_customer_address(self):
        client = APIClient()
        client.force_authenticate(self.user2)
        response = client.get(
            reverse(
                "profiles:customer_address_detail",
                kwargs={"pk": self.customer1.id, "address_pk": 100},
            )
        )

        self.assertEquals(response.status_code, 404)

    def test_update_customer_address_with_valid_authenticated_user(self):
        client = APIClient()
        client.force_authenticate(self.user2)

        response = client.put(
            reverse(
                "profiles:customer_address_detail",
                kwargs={"pk": self.customer1.id, "address_pk": self.address1.id},
            ),
            {
                "number": "9999",
                "street": "newStreet",
                "neighborhood": "newNeighborhood",
            },
        )

        self.assertEqual(response.status_code, 200)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data["number"], "9999")
        self.assertEqual(data["street"], "newStreet")
        self.assertEqual(data["neighborhood"], "newNeighborhood")

    def test_update_not_valid_customer_address(self):
        client = APIClient()
        client.force_authenticate(self.user2)

        response = client.put(
            reverse(
                "profiles:customer_address_detail",
                kwargs={"pk": self.customer1.id, "address_pk": 100},
            ),
            {
                "number": "9999",
                "street": "newStreet",
                "neighborhood": "newNeighborhood",
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_update_customer_address_wich_the_authenticated_user_does_not_own(self):
        client = APIClient()
        client.force_authenticate(self.user1)

        response = client.put(
            reverse(
                "profiles:customer_address_detail",
                kwargs={"pk": self.customer1.id, "address_pk": self.address1.id},
            ),
            {
                "number": "9999",
                "street": "newStreet",
                "neighborhood": "newNeighborhood",
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_update_customer_address_with_invalid_data(self):
        client = APIClient()
        client.force_authenticate(self.user2)

        response = client.put(
            reverse(
                "profiles:customer_address_detail",
                kwargs={"pk": self.customer1.id, "address_pk": self.address1.id},
            ),
            {
                "street": "newStreet",
                "neighborhood": "newNeighborhood",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_customer_address_with_valid_authenticated_user(self):
        address_count = Address.objects.all().count()

        client = APIClient()
        client.force_authenticate(self.user2)

        response = client.delete(
            reverse(
                "profiles:customer_address_detail",
                kwargs={"pk": self.customer1.id, "address_pk": self.address1.id},
            )
        )

        self.assertEqual(response.status_code, 204)

        new_address_count = Address.objects.all().count()
        self.assertEqual(new_address_count, address_count - 1)

    def test_delete_customer_address_with_not_authenticated_user(self):
        client = APIClient()

        response = client.delete(
            reverse(
                "profiles:customer_address_detail",
                kwargs={"pk": self.customer1.id, "address_pk": self.address1.id},
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_customer_address_wich_authenticated_user_does_not_own(self):
        client = APIClient()
        client.force_authenticate(self.user1)

        response = client.delete(
            reverse(
                "profiles:customer_address_detail",
                kwargs={"pk": self.customer1.id, "address_pk": self.address1.id},
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_not_valid_customer_address(self):
        client = APIClient()
        client.force_authenticate(self.user2)

        response = client.delete(
            reverse(
                "profiles:customer_address_detail",
                kwargs={"pk": self.customer1.id, "address_pk": 100},
            )
        )
        self.assertEqual(response.status_code, 404)


class CustomerHistoryTest(TestCase):
    def setUp(self):
        pass
