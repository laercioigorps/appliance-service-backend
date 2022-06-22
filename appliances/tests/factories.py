import factory


from core.utils.tests.base import faker

from appliances.models import Brand, Category

class BrandFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Brand

    name = factory.LazyAttribute(lambda _: faker.name())


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category

    name = factory.LazyAttribute(lambda _: faker.name())