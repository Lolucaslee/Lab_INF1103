from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    """
    Abstract Base Class for all product types.
    Cannot be instantiated directly due to abstractmethod get_fulfilment_info.
    Association: each Product refers to one independently created Supplier.
    """

    def __init__(
        self, product_id: str, name: str, price: float, stock: int, supplier: Supplier
    ) -> None:
        self._product_id: str = str(product_id)
        self._name: str = str(name)
        # Validation lives here, in the class that owns the rules. Subclasses
        # inherit it and cannot skip it (LSP).
        self._price: float = 0.0
        self.price = price  # validating setter: must be > 0
        self._stock: int = self._checked_stock(stock)
        self.supplier: Supplier = supplier

    @staticmethod
    def _checked_stock(quantity: int) -> int:
        """Stock cannot be negative."""
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")
        return int(quantity)

    def display_supplier_information(self) -> None:
        """Shows this product's supplier details."""
        self.supplier.display_information()

    @property
    def product_id(self) -> str:
        """Read-only property for Product ID."""
        return self._product_id

    @property
    def name(self) -> str:
        """Getter for product name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Setter for product name."""
        self._name = str(value)

    @property
    def price(self) -> float:
        """Getter for product price."""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """Setter for price: must be greater than zero."""
        if value <= 0:
            raise ValueError("Price must be greater than zero.")
        self._price = float(value)

    @property
    def stock(self) -> int:
        """Getter for stock quantity."""
        return self._stock

    def update_stock(self, new_qty: int) -> None:
        """Updates internal stock quantity with validation."""
        self._stock = self._checked_stock(new_qty)

    def display_information(self) -> None:
        """Prints baseline product attributes shared across all product types."""
        print(
            f"ID: {self._product_id} | Name: {self._name} | Price: ${self._price:.2f} | Stock: {self._stock}",
            end="",
        )

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Abstract method returning fulfilment instructions. Must be overridden by subclasses."""
        pass

    def to_dict(self) -> dict:
        """Converts base attributes into a dictionary format for JSON export."""
        return {
            "id": self._product_id,
            "name": self._name,
            "price": self._price,
            "qty": self._stock,
            "supplier": self.supplier.to_dict(),
        }