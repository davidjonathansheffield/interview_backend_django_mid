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
def test_tags_on_order_view_with_valid_order(client, order, order_tag):
    url = reverse('tags-on-order', kwargs={'pk': order.uuid})
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == order_tag.name


@pytest.mark.django_db
def test_tags_on_order_view_with_invalid_order(client):
    url = reverse('tags-on-order', kwargs={'pk': '123e4567-e89b-12d3-a456-426614174000'})
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0


@pytest.mark.django_db
def test_tags_on_order_view_with_multiple_tags(client, order):
    tag1 = OrderTag.objects.create(name="urgent")
    tag2 = OrderTag.objects.create(name="high-priority")
    order.tags.add(tag1, tag2)
    url = reverse('tags-on-order', kwargs={'pk': order.uuid})
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]['name'] in ["urgent", "high-priority"]
    assert response.data[1]['name'] in ["urgent", "high-priority"]


@pytest.mark.django_db
def test_tags_on_order_view_with_no_tags(client, inventory):
    order = Order.objects.create(
        inventory=inventory,
        start_date="2023-10-01",
        embargo_date="2023-10-15"
    )
    url = reverse('tags-on-order', kwargs={'pk': order.uuid})
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0
