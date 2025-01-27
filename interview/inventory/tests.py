import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from interview.inventory.models import Inventory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_inventory_items():
    for i in range(15):
        metadata = {"description": f"Metadata {i}"}
        Inventory.objects.create(name=f"Item {i}", quantity=i, metadata=metadata)


@pytest.mark.django_db
def test_pagination(api_client, create_inventory_items):
    url = reverse('inventory-list-create')
    response = api_client.get(url, {'page': 2, 'page_size': 5})

    assert response.status_code == 200
    assert 'count' in response.data
    assert 'next' in response.data
    assert 'previous' in response.data
    assert 'results' in response.data

    assert response.data['count'] == 15
    assert response.data['next'] is not None
    assert response.data['previous'] is not None

    assert len(response.data['results']) == 5

    results = response.data['results']
    assert results[0]['name'] == "Item 5"
    assert results[-1]['name'] == "Item 9"


@pytest.mark.django_db
def test_default_pagination(api_client, create_inventory_items):
    url = reverse('inventory-list-create')
    response = api_client.get(url)

    assert response.status_code == 200
    assert 'count' in response.data
    assert 'next' in response.data
    assert 'previous' in response.data
    assert 'results' in response.data

    assert len(response.data['results']) == 10
    assert response.data['count'] == 15
    assert response.data['next'] is not None
    assert response.data['previous'] is None


@pytest.mark.django_db
def test_custom_page_size(api_client, create_inventory_items):
    url = reverse('inventory-list-create')
    response = api_client.get(url, {'page_size': 20})

    assert response.status_code == 200
    assert 'count' in response.data
    assert 'next' in response.data
    assert 'previous' in response.data
    assert 'results' in response.data

    assert len(response.data['results']) == 15
    assert response.data['count'] == 15
    assert response.data['next'] is None
    assert response.data['previous'] is None
