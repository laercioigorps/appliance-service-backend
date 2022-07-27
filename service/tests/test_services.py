from django.test import TestCase
from appliances.models import Appliance
from service.models import Status
from profiles.models import Organization

from service.services import SampleDataCreation


class SampleDataCreationServiceTest(TestCase):
    def setUp(self):
        self.sampleData = SampleDataCreation()
        self.organization = Organization.objects.create(name="own")
        self.setTestStatuses()

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

    def test_initial_customers(self):
        self.assertEqual(len(self.sampleData.customers), 0)

    def test_initial_available_status(self):
        self.assertEqual(len(self.sampleData.statuses), 0)

    def test_update_available_status(self):
        allStatuses = Status.objects.all()
        self.sampleData.updateStatuses()
        self.assertEqual(len(self.sampleData.statuses), allStatuses.count())
        self.assertEqual(list(allStatuses), list(self.sampleData.statuses))

    def test_initial_organization(self):
        self.assertEqual(self.sampleData.organization, None)

    def test_set_organization(self):
        self.sampleData.organization = self.organization
        self.assertEqual(self.sampleData.organization, self.organization)

    def test_initial_appliances(self):
        self.assertEqual(len(self.sampleData.appliances), 0)
