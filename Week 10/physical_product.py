from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    """
    Represents a physical item requiring inventory storage and shipping.
    Inherits from Product and implements the CanBeShipped interface.
    """

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        weight: float,
    ):
        super().__init__(product_id, name, price, stock, supplier)
        self._weight: float = float(weight)

    @property
    def weight(self) -> float:
        """Getter for item weight in kg."""
        return self._weight

    @weight.setter
    def weight(self, value: float) -> None:
        """Setter for item weight with basic validation."""
        if value < 0:
            raise ValueError("Weight cannot be negative.")
        self._weight = float(value)

    def display_information(self) -> None:
        """
        Method Overriding: Reuses parent display_information() output, 
        then appends unique weight detail.
        """
        super().display_information()
        print(f" | Weight: {self._weight:.2f} kg")

    def get_fulfilment_info(self) -> str:
        """Concrete implementation of the abstract method from Product."""
        return f"Item requires physical packaging and postal shipping (Weight: {self._weight}kg)."

    def calculate_shipping_cost(self) -> float:
        """
        Concrete implementation of CanBeShipped interface method.
        Calculates shipping cost based on weight at $0.30 per kg.
        """
        cost_per_kg = 0.30
        return self._weight * cost_per_kg

    def to_dict(self) -> dict:
        """Extends parent dictionary serialization with type and weight info."""
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self._weight
        return data