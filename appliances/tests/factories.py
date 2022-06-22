import factory


from core.utils.tests.base import faker

from appliances.models import Brand

class BrandFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Brand

    name = factory.LazyAttribute(lambda _: faker.name())