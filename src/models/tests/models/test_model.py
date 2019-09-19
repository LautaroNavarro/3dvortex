import pytest
from models.models.model import Model
from users.tests.factories.user_factory import UserFactory
from models.tests.factories.category_factory import CategoryFactory


@pytest.mark.django_db
class TestModel:

    def test_create_model(self):
        user = UserFactory()
        category = CategoryFactory()
        model = Model.objects.create(
            user=user,
            name="Model name",
            description="This is a really cool model",
            model_url="https://3dvortex-models.s3.us-east-2.amazonaws.com/1.obj",
            volume="1.5",
            image_url="https://3dvortex-images.s3.us-east-2.amazonaws.com/1.obj",
            privacy=Model.Privacy.PRIVATE.value,
            category=category,
        )
        assert model is not None
