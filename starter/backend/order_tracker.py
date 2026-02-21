"""This module contains the OrderTracker class, which encapsulates the core
    business logic for managing orders. """

from starter.backend.errors import FieldValidationError, NotFoundError


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
        existing_order = self.storage.get_order(order_id)
        if existing_order is None:
            raise NotFoundError(
                f"Order not found for order_id: {order_id}")
        self.storage.save_order(
            order_id, {**existing_order, "status": new_status})
        return self.storage.get_order(order_id)

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
        self._validate_fields_not_missing(
            order_id, item_name, quantity, customer_id)
        self._validate_fields_nonempty(order_id, item_name, customer_id)
        self._validate_quantity(quantity)

    def _validate_fields_not_missing(self, order_id, item_name, quantity, customer_id):
        fields_to_check = {"order_id": order_id, "item_name": item_name,
                           "quantity": quantity, "customer_id": customer_id}
        missing_fields = [field_name for field_name,
                          value in fields_to_check.items() if value is None]
        if missing_fields:
            raise FieldValidationError(
                f"Missing the following required fields: {', '.join(missing_fields)}")

    def _validate_fields_nonempty(self, order_id, item_name, customer_id):
        fields_to_check = {"order_id": order_id,
                           "item_name": item_name, "customer_id": customer_id}
        not_string_fields = [field_name for field_name, value in fields_to_check.items(
        ) if self._is_not_empty_or_blank_string(value)]
        if not_string_fields:
            raise FieldValidationError(
                f"The following fields must be non-empty or blank strings: {', '.join(not_string_fields)}")

    def _is_not_empty_or_blank_string(self, value):
        return not isinstance(value, str) or not value.strip()

    def _validate_quantity(self, quantity):
        if not isinstance(quantity, int) or quantity < 1:
            raise FieldValidationError("Quantity must be a positive integer.")
