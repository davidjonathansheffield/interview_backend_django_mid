import pytest
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from rest_framework.test import APIRequestFactory
from interview.inventory.views import InventoryListAfterView
from interview.inventory.models import Inventory


@pytest.fixture
def api_request_factory():
    return APIRequestFactory()


@pytest.fixture
def inventory_items():
    """ Create some test Inventory items with different created_at dates. """
    now = make_aware(datetime.now())
    past = now - timedelta(days=5)
    future = now + timedelta(days=5)

    Inventory.objects.create(name="Item 1", created_at=past)
    Inventory.objects.create(name="Item 2", created_at=now)
    Inventory.objects.create(name="Item 3", created_at=future)


@pytest.mark.django_db
def test_inventory_list_after_valid_date(api_request_factory, inventory_items):
    view = InventoryListAfterView.as_view()
    now = datetime.now().strftime('%Y-%m-%d')

    request = api_request_factory.get(f'/after/{now}/')
    response = view(request, date=now)

    # Assert
    assert response.status_code == 200
    assert len(response.data) == 2  # Items created at or after the current date
    assert response.data[0]['name'] == "Item 2"
    assert response.data[1]['name'] == "Item 3"


@pytest.mark.django_db
def test_inventory_list_after_invalid_date(api_request_factory):
    view = InventoryListAfterView.as_view()
    invalid_date = "2023-13-01"  # Invalid month
    request = api_request_factory.get(f'/after/{invalid_date}/')

    response = view(request, date=invalid_date)

    assert response.status_code == 400
    assert response.data == {'error': 'Invalid date format. Expected YYYY-MM-DD.'}


@pytest.mark.django_db
def test_inventory_list_after_no_matching_items(api_request_factory, inventory_items):
    view = InventoryListAfterView.as_view()
    future_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
    request = api_request_factory.get(f'/after/{future_date}/')

    response = view(request, date=future_date)

    assert response.status_code == 200
    assert len(response.data) == 0  # No items created after the future date
