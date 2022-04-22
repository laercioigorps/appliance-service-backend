from django.test import TestCase
from appliances.models import Brand, Category, Appliance

# Create your tests here.
class BrandTest(TestCase):
    def test_create_brand(self):
        Brand.objects.create(name="Brastemp")
        myBrand = Brand.objects.get(name="Brastemp")
        self.assertEquals(myBrand.name, "Brastemp")


class CategoryTest(TestCase):
    def test_create_category(self):
        Category.objects.create(name="Geladeira")
        category = Category.objects.get(name="Geladeira")
        self.assertEquals(category.name, "Geladeira")


class ApplianceTest(TestCase):

    def setUp(self):
        self.brand1 = Brand.objects.create(name="Brastemp")
        self.category1 = Category.objects.create(name="Geladeira")

    def test_create_Apliance(self):
        Appliance.objects.create(
            model="BWC11ABANA", brand=self.brand1, category=self.category1)
        appliance = Appliance.objects.get(model="BWC11ABANA")
        self.assertEquals(appliance.model, "BWC11ABANA")
        self.assertEquals(appliance.brand.name, "Brastemp")
        self.assertEquals(appliance.category.name, "Geladeira")