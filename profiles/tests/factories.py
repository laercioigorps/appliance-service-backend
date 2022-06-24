import factory

from profiles.models import Address, Organization


from core.utils.tests.base import faker


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.LazyAttribute(lambda _: faker.company())


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    number = factory.LazyAttribute(lambda _: faker.building_number())
    street = factory.LazyAttribute(lambda _: faker.street_name())
    neighborhood = factory.LazyAttribute(lambda _: faker.city_suffix())
    city = factory.LazyAttribute(lambda _: faker.city())
    state = factory.LazyAttribute(lambda _: faker.state())
    country = factory.LazyAttribute(lambda _: faker.country())
