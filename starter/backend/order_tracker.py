# This module contains the OrderTracker class, which encapsulates the core
# business logic for managing orders.

class OrderTracker:
    """
    Manages customer orders, providing functionalities to add, update,
    and retrieve order information.
    """

    def __init__(self, storage):
        self._validate_storage(storage)
        self.storage = storage

    def add_order(self, order_id: str, item_name: str, quantity: int, customer_id: str, status: str = "pending"):
        self._validate_order(order_id, item_name, quantity, customer_id)
        self.storage.save_order(order_id, {
            "order_id": order_id,
            "item_name": item_name,
            "quantity": quantity,
            "customer_id": customer_id,
            "status": status
        })

    def get_order_by_id(self, order_id: str):
        return self.storage.get_order(order_id)

    def update_order_status(self, order_id: str, new_status: str):
        pass

    def list_all_orders(self):
        return self.storage.get_all_orders()

    def list_orders_by_status(self, status: str):
        pass

    def _validate_storage(self, storage):
        required_methods = ['save_order', 'get_order', 'get_all_orders']
        for method in required_methods:
            if not hasattr(storage, method) or not callable(getattr(storage, method)):
                raise TypeError(
                    f"Storage object must implement the following callable methods: {', '.join(required_methods)}.")

    def _validate_order(self, order_id, item_name, quantity, customer_id):
        missing_fields = []
        if order_id is None:
            missing_fields.append("order_id")
        if item_name is None:
            missing_fields.append("item_name")
        if quantity is None:
            missing_fields.append("quantity")
        if customer_id is None:
            missing_fields.append("customer_id")
        if missing_fields:
            raise ValueError(
                f"Missing the following required fields: {', '.join(missing_fields)}")
        if not isinstance(quantity, int) or quantity < 1:
            raise ValueError("Quantity must be a positive integer.")
