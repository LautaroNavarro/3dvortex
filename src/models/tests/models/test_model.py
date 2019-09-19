import pytest
from models.models.model import Model
from users.tests.factories.user_factory import UserFactory
from models.tests.factories.category_factory import CategoryFactory
from medias.tests.factories.media_factory import MediaFactory
from medias.models.media import Media


class TestModel:

    @pytest.mark.django_db
    def test_create_model(self):
        user = UserFactory()
        category = CategoryFactory()
        media_model = MediaFactory(media_type=Media.MediaType.MODEL.value)
        media_image = MediaFactory(media_type=Media.MediaType.MODEL.value)
        model = Model.objects.create(
            user=user,
            name="Model name",
            description="This is a really cool model",
            media_model=media_model,
            volume="1.5",
            media_image=media_image,
            privacy=Model.Privacy.PRIVATE.value,
            category=category,
        )
        assert model is not None
