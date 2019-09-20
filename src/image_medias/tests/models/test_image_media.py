import pytest
from image_medias.models.image_media import ImageMedia
from users.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class TestImageMedia:

    def test_create_image_media(self):
        user = UserFactory()
        image_media = ImageMedia.objects.create(
            user=user,
            url='https://3dvortex-models.s3.us-east-2.amazonaws.com/1.obj',
        )
        assert image_media is not None
