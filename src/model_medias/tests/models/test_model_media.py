import pytest
from model_medias.models.model_media import ModelMedia
from users.tests.factories.user_factory import UserFactory


@pytest.mark.django_db
class TestModelMedia:

    def test_create_image_media(self):
        user = UserFactory()
        model_media = ModelMedia.objects.create(
            user=user,
            url='https://3dvortex-models.s3.us-east-2.amazonaws.com/1.stl',
        )
        assert model_media is not None
