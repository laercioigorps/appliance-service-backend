from django.test import TestCase
from appliances.models import Brand, Category

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