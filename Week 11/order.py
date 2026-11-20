from discount import DiscountStrategy, NoDiscount
from product import Product


class OrderLine:
    """
    One product and quantity inside an Order.

    Relationship: COMPOSITION with Order (Order owns the line, created only by
    Order.add_order_line). ASSOCIATION with Product (the line refers to a
    Product but does not own it).
    Validation: the line protects its own quantity (must be > 0).
    """

    def __init__(self, product: Product, quantity: int) -> None:
        self.product: Product = product
        self._quantity: int = 0
        self.quantity = quantity  # goes through the validating setter

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        if value <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self._quantity = value

    def calculate_subtotal(self) -> float:
        """Product price multiplied by quantity."""
        return self.product.price * self.quantity

    def display_information(self) -> None:
        print(
            f"  {self.product.name} x{self.quantity} "
            f"@ ${self.product.price:.2f} = ${self.calculate_subtotal():.2f}"
        )


class Order:
    """
    A customer order. It creates and manages its own OrderLine objects
    (composition).

    Strategy pattern: the order is GIVEN a DiscountStrategy and only calls
    apply(). It contains no if/elif about discount types. The strategy is
    something the order uses (association), not a part of it, so one strategy
    object can be shared by many orders.
    """

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        self.discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def set_discount(self, discount: DiscountStrategy) -> None:
        """Swaps the discount strategy on an existing order."""
        self.discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Creates an OrderLine internally and adds it to this order."""
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Removes (and so destroys) the line for a product. True if removed."""
        for line in self.order_lines:
            if line.product.product_id == product_id:
                self.order_lines.remove(line)
                return True
        return False

    def calculate_total(self) -> float:
        """Sums the line subtotals, then lets the strategy adjust the total."""
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)

    def display_information(self) -> None:
        print(f"Order {self.order_id}")
        for line in self.order_lines:
            line.display_information()
        print(f"  Total: ${self.calculate_total():.2f}")
