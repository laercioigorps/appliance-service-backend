from django.test import TestCase
from appliances.models import Brand

# Create your tests here.
class BrandTest(TestCase):
    def test_create_brand(self):
        Brand.objects.create(name="Brastemp")
        myBrand = Brand.objects.get(name="Brastemp")
        self.assertEquals(myBrand.name, "Brastemp")