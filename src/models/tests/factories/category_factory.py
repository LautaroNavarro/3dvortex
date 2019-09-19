import factory
from models.models.category import Category


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category

    name = factory.Sequence(lambda n: 'name_{}'.format(n))
    father_category = None
