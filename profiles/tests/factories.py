import factory
from django.contrib.auth.models import User
from profiles.models import Address, Customer, Organization


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


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    name = factory.LazyAttribute(lambda _: faker.name())
    owner = factory.SubFactory(OrganizationFactory)
    email = factory.LazyAttribute(lambda _: faker.name())
    profession = factory.LazyAttribute(lambda _: faker.job())
    nickname = factory.LazyAttribute(lambda _: faker.first_name())
    phone1 = factory.LazyAttribute(lambda _: faker.phone_number())
    phone2 = factory.LazyAttribute(lambda _: faker.phone_number())

    @factory.post_generation
    def addresses(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of solutions were passed in, use them
            for adress in extracted:
                self.addresses.add(adress)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: faker.first_name())
    password = "root"
