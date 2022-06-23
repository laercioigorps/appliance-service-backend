import factory

from profiles.models import Organization


from core.utils.tests.base import faker


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.LazyAttribute(lambda _: faker.company())


