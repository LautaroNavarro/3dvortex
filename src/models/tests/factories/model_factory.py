import factory
from models.models.model import Model
from users.tests.factories.user_factory import UserFactory
from helpers.date_helpers import get_current_utc_datetime


class ModelFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Model

    user = UserFactory()
    name = factory.Sequence(lambda n: 'model_name{}'.format(n))
    description = factory.Sequence(lambda n: 'model_description{}'.format(n))
    model_url = factory.Sequence(lambda n: 'https://3dvortex-models.s3.us-east-2.amazonaws.com/{}.obj'.format(n))
    volume = factory.Sequence(lambda n: '{}.{}'.format(n, n + 1))
    image_url = factory.Sequence(lambda n: 'https://3dvortex-models.s3.us-east-2.amazonaws.com/{}.obj'.format(n))
    privacy = Model.Privacy.PRIVATE.value
    category = None
    created = factory.LazyFunction(get_current_utc_datetime)
    changed = factory.LazyFunction(get_current_utc_datetime)
