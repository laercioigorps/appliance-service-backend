import factory
from core.utils.tests.base import faker
from service.models import Service
from profiles.tests.factories import (
    OrganizationFactory,
    CustomerFactory,
    AddressFactory,
)
from appliances.tests.factories import HistoricFactory
from decimal import Decimal


class ServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Service

    owner = factory.SubFactory(OrganizationFactory)
    historic = factory.SubFactory(HistoricFactory)
    customer = factory.SubFactory(
        CustomerFactory, owner=factory.SelfAttribute("..owner")
    )
    address = factory.SubFactory(AddressFactory)
    price = factory.LazyAttribute(
        lambda _: faker.pydecimal(left_digits=4, right_digits=2)
    )
