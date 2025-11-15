from collections import defaultdict
from typing import Dict


class InventoryStore:
    """Simple in-memory inventory store.
    In a real scenario this would be a persistent database.
    """

    def __init__(self) -> None:
        self._store: Dict[int, int] = defaultdict(int)

    def get_quantity(self, product_id: int) -> int:
        return self._store[product_id]

    def set_quantity(self, product_id: int, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self._store[product_id] = quantity

    def decrease_quantity(self, product_id: int, amount: int) -> int:
        current = self.get_quantity(product_id)
        if amount < 0:
            raise ValueError("Amount must be positive")
        if amount > current:
            raise ValueError("Insufficient inventory")
        new_qty = current - amount
        self._store[product_id] = new_qty
        return new_qty


inventory_store = InventoryStore()
