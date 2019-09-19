import pytest
from medias.models.media import Media
from users.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class TestMedia:

    def test_create_media(self):
        user = UserFactory()
        media = Media.objects.create(
            user=user,
            media_type=Media.MediaType.IMAGE.value,
            url='https://3dvortex-models.s3.us-east-2.amazonaws.com/1.obj',
        )
        assert media is not None
