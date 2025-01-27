import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from datetime import date, timedelta
from interview.order.models import Order


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def orders():
    Order.objects.create(start_date=date(2023, 1, 1), embargo_date=date(2023, 1, 31))
    Order.objects.create(start_date=date(2023, 2, 1), embargo_date=date(2023, 2, 28))
    Order.objects.create(start_date=date(2023, 3, 1), embargo_date=date(2023, 3, 31))
    Order.objects.create(start_date=date(2023, 1, 15), embargo_date=date(2023, 2, 15))  # Overlapping
    Order.objects.create(start_date=date(2023, 1, 1), embargo_date=date(2023, 1, 1))  # Exact match


def build_url(start_date, embargo_date):
    return reverse('order-list-between', kwargs={'start_date': start_date, 'embargo_date': embargo_date})


def test_order_list_between_valid_dates(client, orders):
    url = build_url('2023-01-01', '2023-01-31')
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2


def test_order_list_between_no_orders(client, orders):
    url = build_url('2024-01-01', '2024-01-31')
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 0  # No orders in 2024


def test_order_list_between_exact_match(client, orders):
    url = build_url('2023-01-01', '2023-01-01')
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1  # Only one order exactly matches


def test_order_list_between_partial_overlap(client, orders):
    url = build_url('2023-01-15', '2023-02-15')
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2  # Orders starting on 2023-01-15 and 2023-02-01


def test_order_list_between_invalid_date_format(client):
    url = build_url('invalid', '2023-01-31')
    response = client.get(url)

    assert response.status_code == 400
    assert 'Invalid date format' in response.data['detail']


def test_order_list_between_start_after_embargo(client):
    url = build_url('2023-02-01', '2023-01-01')
    response = client.get(url)

    assert response.status_code == 400
    assert 'start_date must be before or equal to embargo_date' in response.data['detail']


def test_order_list_between_missing_dates(client):
    url = reverse('order-list-between', kwargs={'start_date': '2023-01-01'})
    response = client.get(url)

    assert response.status_code == 404  # Django will raise a 404 for missing URL parameters
