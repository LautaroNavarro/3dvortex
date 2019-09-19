import factory
from models.models.model import Model
from users.tests.factories.user_factory import UserFactory
from medias.tests.factories.media_factory import MediaFactory
from medias.models.media import Media
from helpers.date_helpers import get_current_utc_datetime


class ModelFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Model

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: 'model_name{}'.format(n))
    description = factory.Sequence(lambda n: 'model_description{}'.format(n))
    media_model = MediaFactory(media_type=Media.MediaType.MODEL.value)
    volume = factory.Sequence(lambda n: '{}.{}'.format(n, n + 1))
    media_image = factory.SubFactory(MediaFactory)
    privacy = Model.Privacy.PRIVATE.value
    category = None
    created = factory.LazyFunction(get_current_utc_datetime)
    changed = factory.LazyFunction(get_current_utc_datetime)
