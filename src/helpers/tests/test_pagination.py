import pytest
import mock
import json
from models.tests.factories.category_factory import CategoryFactory
from models.models.category import Category
from helpers.pagination import PaginatedResponse
from django.http import JsonResponse


@pytest.mark.django_db
@mock.patch('helpers.pagination.DEFAULT_PAGE_SIZE', 3)
class TestPagination:

    def test_it_returns_paginated_response(self):
        for i in range(0, 2):
            CategoryFactory.create()
        query = Category.objects.all()
        paginated_response = PaginatedResponse('categories', query, 1)
        response = json.loads(paginated_response.content)
        assert type(paginated_response) == JsonResponse
        assert response['page'] == 1
        assert response['has_next'] is False
        assert response['page_size'] == 3
        assert len(response['categories']) == 2

    def test_it_returns_page_2_response(self):
        for i in range(0, 4):
            CategoryFactory.create()
        query = Category.objects.all()
        paginated_response = PaginatedResponse('categories', query, 2)
        response = json.loads(paginated_response.content)
        assert type(paginated_response) == JsonResponse
        assert response['page'] == 2
        assert response['has_next'] is False
        assert response['page_size'] == 3
        assert len(response['categories']) == 1

    def test_it_returns_has_next_when_it_has_next(self):
        for i in range(0, 4):
            CategoryFactory.create()
        query = Category.objects.all()
        paginated_response = PaginatedResponse('categories', query, 1)
        response = json.loads(paginated_response.content)
        assert type(paginated_response) == JsonResponse
        assert response['page'] == 1
        assert response['has_next'] is True
        assert response['page_size'] == 3
        assert len(response['categories']) == 3
