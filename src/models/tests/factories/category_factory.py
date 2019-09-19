import factory
from models.models.category import Category
from helpers.date_helpers import get_current_utc_datetime


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category

    name = factory.Sequence(lambda n: 'name_{}'.format(n))
    father_category = None
    created = factory.LazyFunction(get_current_utc_datetime)
    changed = factory.LazyFunction(get_current_utc_datetime)
