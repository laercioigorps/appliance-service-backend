from django.test import TestCase

from service.services import SampleDataCreation


class SampleDataCreationServiceTest(TestCase):
    def setUp(self):
        self.sampleData = SampleDataCreation()

    def test_initial_customers(self):
        self.assertEqual(len(self.sampleData.customers), 0)
