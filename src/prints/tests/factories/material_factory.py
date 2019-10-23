import factory
from prints.models.material import Material
from helpers.date_helpers import get_current_utc_datetime


class MaterialFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Material

    name = factory.Sequence(lambda n: 'name_{}'.format(n))
    description = factory.Sequence(lambda n: 'description_{}'.format(n))
    price_per_kilogram = factory.Sequence(lambda n: '{}.{}'.format(n, str(n * 10)[:2]))
    created = factory.LazyFunction(get_current_utc_datetime)
    changed = factory.LazyFunction(get_current_utc_datetime)
