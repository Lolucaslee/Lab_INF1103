class Product:
    """
    Represents an individual Product object.
    
    Responsibility (SRP):
    Stores product details and manages its own internal state.
    """

    def __init__(self, product_id: str, name: str, price: float, stock: int):
        # Using leading underscores (_attribute) to signal encapsulated internal attributes
        self._product_id = str(product_id)
        self._name = str(name)
        self._price = float(price)
        self._stock = int(stock)

    # ------------------------------------------------------------------
    # Properties (Getters / Setters)
    # ------------------------------------------------------------------

    @property
    def product_id(self) -> str:
        """Getter for product_id (Read-only)."""
        return self._product_id

    @property
    def name(self) -> str:
        """Getter for product name."""
        return self._name

    @name.setter
    def name(self, value: str):
        """Setter for product name."""
        self._name = str(value)

    @property
    def price(self) -> float:
        """Getter for product price."""
        return self._price

    @price.setter
    def price(self, value: float):
        """Setter for product price with basic validation."""
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = float(value)

    @property
    def stock(self) -> int:
        """Getter for stock level."""
        return self._stock

    # ------------------------------------------------------------------
    # Product Methods
    # ------------------------------------------------------------------

    def update_stock(self, new_qty: int) -> None:
        """
        Updates the stock quantity directly (matching Week 5's new stock logic).
        Validates that stock cannot be negative.
        """
        if new_qty < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self._stock = int(new_qty)

    def display_information(self) -> None:
        """Prints product details matching your Week 5 format."""
        print(f"ID: {self._product_id} | Name: {self._name} | Price: ${self._price:.2f} | Stock: {self._stock}")

    # ------------------------------------------------------------------
    # Serialization Helpers
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Converts Product object back to dictionary matching Week 5 JSON structure."""
        return {
            "id": self._product_id,
            "name": self._name,
            "price": self._price,
            "qty": self._stock
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Product object from a dictionary (used when loading JSON)."""
        return cls(
            product_id=data["id"],
            name=data["name"],
            price=data["price"],
            stock=data["qty"]
        )