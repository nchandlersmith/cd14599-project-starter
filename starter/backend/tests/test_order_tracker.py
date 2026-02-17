import pytest
from unittest.mock import Mock
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
def test_add_order_stores_new_order(order_tracker):
    storage = order_tracker.storage
    order = {"id": "some_id", "item_name": "some_item", "quantity": 1, "customer_id": "some_customer", "status": "some_status"}
    
    order_tracker.add_order(order["id"], order["item_name"], order["quantity"], order["customer_id"], order["status"])
    
    storage.save_order.assert_called_once_with(order["id"], order)
    
def test_add_order_fails_with_missing_fields(order_tracker):
    with pytest.raises(ValueError, match="Missing the following required fields: id, item_name, quantity, customer_id"):
        order_tracker.add_order(None, None, None, None)