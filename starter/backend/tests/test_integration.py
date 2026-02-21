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
        "order_id": "some_id",
        "item_name": "some_item",
        "quantity": 1,
        "customer_id": "some_customer",
        "status": "some_status"
    }

    order_tracker.add_order(**expected_order)

    assert storage.get_order("some_id") == expected_order


@pytest.mark.integration
def test_add_order_success_status_pending_by_default(storage):
    order_tracker = OrderTracker(storage)
    expected_order = {
        "order_id": "some_id",
        "item_name": "some_item",
        "quantity": 1,
        "customer_id": "some_customer",
    }

    order_tracker.add_order(**expected_order)

    assert storage.get_order("some_id") == {**expected_order, "status": "pending"}


@pytest.mark.integration
def test_get_order_by_id_integration_success(storage):
    order_tracker = OrderTracker(storage)
    expected_order = {
        "id": "some_id",
        "item_name": "some_item",
        "quantity": 1,
        "customer_id": "some_customer",
        "status": "some_status"
    }
    storage.save_order(expected_order["id"], expected_order)

    result = order_tracker.get_order_by_id("some_id")
    
    assert result == expected_order


@pytest.mark.integration
def test_get_order_by_id_integration_not_found(storage):
    order_tracker = OrderTracker(storage)
    result = order_tracker.get_order_by_id("nonexistent_id")
    assert result is None


@pytest.mark.integration
def test_get_order_by_id_integration_returns_correct_order(storage):
    order_tracker = OrderTracker(storage)
    order1 = {
        "id": "id1",
        "item_name": "item1",
        "quantity": 1,
        "customer_id": "customer1",
        "status": "status1"
    }
    order2 = {
        "id": "id2",
        "item_name": "item2",
        "quantity": 2,
        "customer_id": "customer2",
        "status": "status2"
    }
    storage.save_order(order1["id"], order1)
    storage.save_order(order2["id"], order2)

    result = order_tracker.get_order_by_id("id2")

    assert result == order2
    

def test_get_all_orders_success(storage):
    order_tracker = OrderTracker(storage)
    order1 = {
        "id": "id1",
        "item_name": "item1",
        "quantity": 1,
        "customer_id": "customer1",
        "status": "status1"
    }
    order2 = {
        "id": "id2",
        "item_name": "item2",
        "quantity": 2,
        "customer_id": "customer2",
        "status": "status2"
    }
    storage.save_order(order1["id"], order1)
    storage.save_order(order2["id"], order2)

    result = order_tracker.list_all_orders()

    assert len(result) == 2
    assert result["id1"] == order1
    assert result["id2"] == order2
