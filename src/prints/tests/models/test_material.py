import pytest
from prints.models.material import Material


@pytest.mark.django_db
class TestMaterialModel:

    def test_create_model(self):
        material = Material(
            name='ABS',
            description='Good mechanical properties.',
            price_per_kilogram='120.23',
        )
        material.save()
        assert Material.objects.filter(id=material.id).exists() is True
