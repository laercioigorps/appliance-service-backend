import factory


from core.utils.tests.base import faker

from appliances.models import Appliance, Brand, Category


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.LazyAttribute(lambda _: faker.company())


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.LazyAttribute(lambda _: faker.color_name())


class ApplianceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Appliance

    model = factory.LazyAttribute(lambda _: faker.lexify(text="??????????"))
    category = factory.SubFactory(CategoryFactory)
    brand = factory.SubFactory(BrandFactory)
