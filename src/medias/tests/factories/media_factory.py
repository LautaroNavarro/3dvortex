import factory
from medias.models.media import Media
from users.tests.factories.user_factory import UserFactory
from helpers.date_helpers import get_current_utc_datetime


class MediaFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Media

    user = factory.SubFactory(UserFactory)
    media_type = Media.MediaType.IMAGE.value
    url = factory.Sequence(lambda n: 'https://3dvortex-models.s3.us-east-2.amazonaws.com/{}.obj'.format(n))
    created = factory.LazyFunction(get_current_utc_datetime)
    changed = factory.LazyFunction(get_current_utc_datetime)
