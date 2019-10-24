import factory
from model_medias.models.model_media import ModelMedia
from users.tests.factories.user_factory import UserFactory
from helpers.date_helpers import get_current_utc_datetime


class ModelMediaFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ModelMedia

    user = factory.SubFactory(UserFactory)
    url = factory.Sequence(lambda n: 'https://3dvortex-models.s3.us-east-2.amazonaws.com/{}.stl'.format(n))
    created = factory.LazyFunction(get_current_utc_datetime)
    changed = factory.LazyFunction(get_current_utc_datetime)
