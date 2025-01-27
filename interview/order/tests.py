import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import logging
from io import StringIO
from interview.order.models import Order


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def order():
    return Order.objects.create(is_active=True)


# Fixture for capturing logs
@pytest.fixture
def log_capture():
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    logger = logging.getLogger('interview.order.views')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    yield log_stream
    logger.removeHandler(handler)
    handler.close()


# Test for successful deactivation
def test_deactivate_order_success(client, order, log_capture):
    url = reverse('order-deactivate', kwargs={'pk': order.pk})

    response = client.patch(url)
    assert response.status_code == status.HTTP_200_OK

    order.refresh_from_db()

    assert order.is_active is False
    assert response.data['is_active'] is False

    log_output = log_capture.getvalue()
    assert f"Order {order.id} deactivated successfully" in log_output


def test_deactivate_order_concurrency(client, order):
    url = reverse('order-deactivate', kwargs={'pk': order.pk})

    # Simulate concurrent updates using threads
    import threading

    def deactivate_order():
        client.patch(url)

    # Start two threads to deactivate the same order concurrently
    thread1 = threading.Thread(target=deactivate_order)
    thread2 = threading.Thread(target=deactivate_order)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    # Assert the order is deactivated
    order.refresh_from_db()
    assert order.is_active is False


# Test for invalid order ID
def test_deactivate_order_not_found(client, log_capture):
    invalid_url = reverse('order-deactivate', kwargs={'pk': 999})

    response = client.patch(invalid_url)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    log_output = log_capture.getvalue()
    assert "Failed to deactivate order 999" in log_output
