import factory
from addresses.models.address import Address
from helpers.date_helpers import get_current_utc_datetime


class AddressFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Address

    name = factory.Sequence(lambda n: 'name_{}'.format(n))
    latitude = factory.Sequence(lambda n: '{}'.format(n))
    longitude = factory.Sequence(lambda n: '{}'.format(n))
    created = factory.LazyFunction(get_current_utc_datetime)
    changed = factory.LazyFunction(get_current_utc_datetime)
