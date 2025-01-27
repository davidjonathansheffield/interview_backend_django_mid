import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from interview.order.models import Order, OrderTag
from interview.inventory.models import Inventory


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def inventory():
    return Inventory.objects.create(name="Test Inventory")

@pytest.fixture
def order_tag():
    return OrderTag.objects.create(name="urgent")

@pytest.fixture
def order(inventory, order_tag):
    order = Order.objects.create(
        inventory=inventory,
        start_date="2023-10-01",
        embargo_date="2023-10-15"
    )
    order.tags.add(order_tag)
    return order


@pytest.mark.django_db
def test_order_list_by_tag_view_with_valid_tag(client, order, order_tag):
    url = reverse('orders-by-tag', kwargs={'tag': order_tag.name})
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['uuid'] == str(order.uuid)


@pytest.mark.django_db
def test_order_list_by_tag_view_with_invalid_tag(client):
    url = reverse('orders-by-tag', kwargs={'tag': 'nonexistent'})
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 0


@pytest.mark.django_db
def test_order_list_by_tag_view_with_multiple_orders(client, inventory, order_tag):
    # Create multiple orders with the same tag
    order1 = Order.objects.create(
        inventory=inventory,
        start_date="2023-10-01",
        embargo_date="2023-10-15"
    )
    order1.tags.add(order_tag)

    order2 = Order.objects.create(
        inventory=inventory,
        start_date="2023-10-05",
        embargo_date="2023-10-20"
    )
    order2.tags.add(order_tag)

    url = reverse('orders-by-tag', kwargs={'tag': order_tag.name})
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_order_list_by_tag_view_without_orders(client, order_tag):
    url = reverse('orders-by-tag', kwargs={'tag': order_tag.name})
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 0
