import factory


from core.utils.tests.base import faker

from appliances.models import Appliance, Brand, Category, Solution, Symptom


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


class SolutionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Solution

    name = factory.LazyAttribute(lambda _: faker.name())
    description = factory.LazyAttribute(lambda _: faker.paragraph(nb_sentences=5))
