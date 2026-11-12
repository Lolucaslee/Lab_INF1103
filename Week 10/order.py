from product import Product


class OrderLine:
    """
    One product and quantity inside an Order.

    Relationship: COMPOSITION with Order (Order owns the line, created only by
    Order.add_order_line). ASSOCIATION with Product (the line refers to a
    Product but does not own it).
    """

    def __init__(self, product: Product, quantity: int) -> None:
        self.product: Product = product
        self.quantity: int = quantity

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
    (composition): lines are never passed in from outside or moved between
    orders, and they disappear with the order.
    """

    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

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
        """Total of every line's subtotal."""
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_information(self) -> None:
        print(f"Order {self.order_id}")
        for line in self.order_lines:
            line.display_information()
        print(f"  Total: ${self.calculate_total():.2f}")
