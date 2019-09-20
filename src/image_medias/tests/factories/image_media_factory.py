import factory
from image_medias.models.image_media import ImageMedia
from users.tests.factories.user_factory import UserFactory
from helpers.date_helpers import get_current_utc_datetime


class ImageMediaFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ImageMedia

    user = factory.SubFactory(UserFactory)
    url = factory.Sequence(lambda n: 'https://3dvortex-models.s3.us-east-2.amazonaws.com/{}.obj'.format(n))
    created = factory.LazyFunction(get_current_utc_datetime)
    changed = factory.LazyFunction(get_current_utc_datetime)
