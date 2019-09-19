import pytest
from models.models.category import Category


@pytest.mark.django_db
class TestCategory:

    def test_create_category(self):
        tech_category = Category.objects.create(name='Tech')
        laptop_category = Category.objects.create(name='Laptops', father_category=tech_category)
        assert tech_category is not None
        assert laptop_category is not None
