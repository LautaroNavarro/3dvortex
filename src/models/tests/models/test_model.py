import pytest
from models.models.model import Model
from users.tests.factories.user_factory import UserFactory
from models.tests.factories.category_factory import CategoryFactory
from image_medias.tests.factories.image_media_factory import ImageMediaFactory


class TestModel:

    @pytest.mark.django_db
    def test_create_model(self):
        user = UserFactory()
        category = CategoryFactory()
        model_media = 1
        image_media = ImageMediaFactory()
        model = Model.objects.create(
            user=user,
            name="Model name",
            description="This is a really cool model",
            model_media=model_media,
            volume="1.5",
            image_media=image_media,
            privacy=Model.Privacy.PRIVATE.value,
            category=category,
        )
        assert model is not None
