import factory
from models.models.model import Model
from users.tests.factories.user_factory import UserFactory
from image_medias.tests.factories.image_media_factory import ImageMediaFactory
from helpers.date_helpers import get_current_utc_datetime
from model_medias.tests.factories.model_media_factory import ModelMediaFactory


class ModelFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Model

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: 'model_name{}'.format(n))
    description = factory.Sequence(lambda n: 'model_description{}'.format(n))
    model_media = factory.SubFactory(ModelMediaFactory)
    volume = factory.Sequence(lambda n: '{}.{}'.format(n, n + 1))
    image_media = factory.SubFactory(ImageMediaFactory)
    privacy = Model.Privacy.PRIVATE.value
    category = None
    printed_quantity = 0
    created = factory.LazyFunction(get_current_utc_datetime)
    changed = factory.LazyFunction(get_current_utc_datetime)
