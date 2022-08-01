import factory
from django.contrib.auth.models import User
from profiles.models import Address, Customer, Organization


from core.utils.tests.base import faker


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.LazyAttribute(lambda _: faker.company()[:30])


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    number = factory.LazyAttribute(lambda _: faker.building_number()[:10])
    street = factory.LazyAttribute(lambda _: faker.street_name()[:30])
    neighborhood = factory.LazyAttribute(lambda _: faker.city_suffix()[:30])
    city = factory.LazyAttribute(lambda _: faker.city()[:30])
    state = factory.LazyAttribute(lambda _: faker.state()[:30])
    country = factory.LazyAttribute(lambda _: faker.country()[:30])


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    name = factory.LazyAttribute(lambda _: faker.name()[:40])
    owner = factory.SubFactory(OrganizationFactory)
    email = factory.LazyAttribute(lambda _: faker.company_email()[:40])
    profession = factory.LazyAttribute(lambda _: faker.job()[:40])
    nickname = factory.LazyAttribute(lambda _: faker.first_name()[:40])
    phone1 = factory.LazyAttribute(lambda _: faker.phone_number()[:29])
    phone2 = factory.LazyAttribute(lambda _: faker.phone_number()[:29])

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
