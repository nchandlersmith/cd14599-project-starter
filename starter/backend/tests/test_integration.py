"""
Testing the integration of the order tracker with the storage layer outside of the API context.
This file contains tests that verify the interaction between the OrderTracker class and the storage.
The storage layer is the in-memory storage implementation, which is used in the actual application.
"""

import pytest

from starter.backend.in_memory_storage import InMemoryStorage
from starter.backend.order_tracker import OrderTracker


@pytest.fixture
def storage():
    return InMemoryStorage()


@pytest.mark.integration
def test_add_order_integration_success(storage):
    order_tracker = OrderTracker(storage)
    expected_order = {
        "id": "some_id",
        "item_name": "some_item",
        "quantity": 1,
        "customer_id": "some_customer",
        "status": "some_status"
    }

    order_tracker.add_order(expected_order["id"], expected_order["item_name"],
                            expected_order["quantity"], expected_order["customer_id"], expected_order["status"])

    assert storage.get_order("some_id") == expected_order
