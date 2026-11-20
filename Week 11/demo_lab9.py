"""Lab 9 demo: prints the evidence for each 'Predict first' question."""
from unittest.mock import patch

from discount import BulkDiscount, PercentageDiscount, StudentDiscount
from input_helpers import get_positive_float
from inventory import Inventory
from order import Order, OrderLine
from product_factory import ProductFactory
from product_loader import load_products
from supplier import Supplier


def heading(text: str) -> None:
    print(f"\n=== {text} ===")


supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")


def demo_strategy() -> None:
    heading("2.3 Strategy: total 250 with BulkDiscount(200, 20), then PercentageDiscount(10)")
    order = Order("O1", BulkDiscount(200, 20))
    order.add_order_line(ProductFactory.create("physical", "P1", "Desk", 100.0, 5, supplier), 2)
    order.add_order_line(ProductFactory.create("digital", "D1", "Editor", 50.0, 5, supplier), 1)
    print("Lines add up to 250.0")
    print("BulkDiscount(200, 20)      ->", order.calculate_total())
    order.set_discount(PercentageDiscount(10))
    print("set_discount(Percentage 10) ->", order.calculate_total())
    order.set_discount(StudentDiscount())
    print("set_discount(StudentDiscount) ->", order.calculate_total())

    heading("2.4 Same PercentageDiscount object shared by two orders")
    shared = PercentageDiscount(10)
    a, b = Order("A", shared), Order("B", shared)
    print("a.discount is b.discount:", a.discount is b.discount)


def demo_factory() -> None:
    heading("3.2 Factory: unknown type 'service' (caught here so the demo continues)")
    try:
        ProductFactory.create("service", "S1", "Installation", 30.0, 5, supplier)
    except ValueError as err:
        print("ValueError:", err)


def demo_validation() -> None:
    heading("4 Validation")
    for label, action in [
        ("price 0", lambda: ProductFactory.create("physical", "P1", "X", 0, 1, supplier)),
        ("stock -1", lambda: ProductFactory.create("digital", "D1", "X", 10.0, -1, supplier)),
        ("order line quantity 0", lambda: OrderLine(ProductFactory.create("digital", "D2", "X", 10.0, 1, supplier), 0)),
        ("DigitalProduct.update_stock(-5)", lambda: ProductFactory.create("digital", "D3", "X", 10.0, 1, supplier).update_stock(-5)),
    ]:
        try:
            action()
            print(f"{label}: accepted (unexpected)")
        except ValueError as err:
            print(f"{label}: rejected -> {err}")


def demo_input() -> None:
    heading("5.1 get_positive_float with inputs: abc, -5, 12.50")
    with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
        value = get_positive_float("Price: ")
    print("Returned:", value)


def demo_loader() -> None:
    heading("5.2 load_products('products.csv')")
    inventory = Inventory()
    load_products("products.csv", inventory, supplier)
    print("IDs loaded:", [p.product_id for p in inventory.products])

    heading("5.2 load_products on a missing file (products.csv renamed)")
    load_products("products_renamed.csv", Inventory(), supplier)


if __name__ == "__main__":
    demo_strategy()
    demo_factory()
    demo_validation()
    demo_input()
    demo_loader()
