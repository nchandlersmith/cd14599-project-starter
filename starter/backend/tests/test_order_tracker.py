"""Unit tests for the OrderTracker class."""

from unittest.mock import Mock
import pytest

from starter.errors import FieldValidationError
from ..order_tracker import OrderTracker

# --- Fixtures for Unit Tests ---


@pytest.fixture
def mock_storage():
    """
    Provides a mock storage object for tests.
    This mock will be configured to simulate various storage behaviors.
    """
    mock = Mock()
    # By default, mock get_order to return None (no order found)
    mock.get_order.return_value = None
    # By default, mock get_all_orders to return an empty dict
    mock.get_all_orders.return_value = {}
    return mock


@pytest.fixture
def order_tracker(mock_storage):
    """
    Provides an OrderTracker instance initialized with the mock_storage.
    """
    return OrderTracker(mock_storage)

#
# --- TODO: add test functions below this line ---
#


def test_constructor_fails_with_non_callable_storage():
    with pytest.raises(TypeError, match="Storage object must implement the following callable methods: save_order, get_order, get_all_orders."):
        OrderTracker(None)


def test_add_order_stores_new_order(order_tracker):
    storage = order_tracker.storage
    order = {"order_id": "some_id", "item_name": "some_item", "quantity": 1,
             "customer_id": "some_customer", "status": "some_status"}

    order_tracker.add_order(**order)

    storage.save_order.assert_called_once_with(order["order_id"], order)


def test_add_order_status_defaults_to_pending(order_tracker):
    storage = order_tracker.storage
    order = {"order_id": "some_id", "item_name": "some_item", "quantity": 1,
             "customer_id": "some_customer"}

    order_tracker.add_order(**order)

    storage.save_order.assert_called_once_with(
        order["order_id"], {**order, "status": "pending"})


@pytest.mark.parametrize("order_id, item_name, quantity, customer_id, expected_error", [
    (None, "item", 1, "customer", "Missing the following required fields: order_id"),
    ("id", None, 1, "customer", "Missing the following required fields: item_name"),
    ("id", "item", None, "customer", "Missing the following required fields: quantity"),
    ("id", "item", 1, None, "Missing the following required fields: customer_id"),
    (None, None, None, None,
     "Missing the following required fields: order_id, item_name, quantity, customer_id")
])
def test_add_order_fails_with_missing_fields(order_tracker, order_id, item_name, quantity, customer_id, expected_error):
    with pytest.raises(FieldValidationError, match=expected_error):
        order_tracker.add_order(order_id, item_name, quantity, customer_id)


@pytest.mark.parametrize("order_id, item_name, quantity, customer_id, expected_error", [
    (20, "item", 1, "customer",
     "The following fields must be non-empty or blank strings: order_id"),
    ("id", 30, 1, "customer",
     "The following fields must be non-empty or blank strings: item_name"),
    ("id", "item", 1, 789,
     "The following fields must be non-empty or blank strings: customer_id"),
    (9001, 7878, 1, 314, "The following fields must be non-empty or blank strings: order_id, item_name, customer_id")
])
def test_add_order_fails_with_wrong_field_type(order_tracker, order_id, item_name, quantity, customer_id, expected_error):
    with pytest.raises(FieldValidationError, match=expected_error):
        order_tracker.add_order(order_id, item_name, quantity, customer_id)


@pytest.mark.parametrize("order_id, item_name, quantity, customer_id, expected_error", [
    ("", "item", 1, "customer",
     "The following fields must be non-empty or blank strings: order_id"),
    ("id", "", 1, "customer",
     "The following fields must be non-empty or blank strings: item_name"),
    ("id", "item", 1, "",
     "The following fields must be non-empty or blank strings: customer_id"),
    (" ", " ", 1, " ", "The following fields must be non-empty or blank strings: order_id, item_name, customer_id")
])
def test_add_order_fails_with_empty_strings(order_tracker, order_id, item_name, quantity, customer_id, expected_error):
    with pytest.raises(FieldValidationError, match=expected_error):
        order_tracker.add_order(order_id, item_name, quantity, customer_id)


@pytest.mark.parametrize("quantity", [0, -1, "foo"])
def test_add_order_fails_with_invalid_quantity(order_tracker, quantity):
    with pytest.raises(FieldValidationError, match="Quantity must be a positive integer."):
        order_tracker.add_order("id", "item", quantity, "customer")


def test_get_order_by_id_returns_order(order_tracker, mock_storage):
    order = {"order_id": "some_id", "item_name": "some_item", "quantity": 1,
             "customer_id": "some_customer", "status": "some_status"}
    mock_storage.get_order.return_value = order

    result = order_tracker.get_order_by_id("some_id")

    assert result == order
    mock_storage.get_order.assert_called_once_with("some_id")


def test_list_all_orders(order_tracker, mock_storage):
    orders = {
        "id1": {"id": "id1", "item_name": "item1", "quantity": 1, "customer_id": "customer1", "status": "pending"},
        "id2": {"id": "id2", "item_name": "item2", "quantity": 2, "customer_id": "customer2", "status": "shipped"}
    }
    mock_storage.get_all_orders.return_value = orders

    result = order_tracker.list_all_orders()

    assert result == orders
    mock_storage.get_all_orders.assert_called_once()


def test_update_order_status_success_returns_updated_order(order_tracker, mock_storage):
    order = {"order_id": "some_id", "item_name": "some_item", "quantity": 1,
             "customer_id": "some_customer", "status": "pending"}
    updated_order = {**order, "status": "shipped"}
    mock_storage.get_order.return_value = order
    mock_storage.get_order.return_value = updated_order

    result = order_tracker.update_order_status("some_id", "shipped")
    assert result == updated_order
    mock_storage.save_order.assert_called_once_with(order["order_id"], updated_order)
