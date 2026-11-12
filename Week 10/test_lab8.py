"""Lab 8 tests: association, aggregation, composition, LSP and polymorphism."""
import sys

from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


def heading(text: str) -> None:
    print(f"\n=== {text} ===")


def show_product_details(product: Product) -> None:
    """Works for ANY Product - no subclass checks (LSP)."""
    product.display_information()
    print(product.get_fulfilment_info())


def test_association() -> None:
    heading("2. Association: Supplier and Product")
    supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")
    keyboard = PhysicalProduct("P001", "Keyboard", 120.0, 15, supplier, 1.5)
    licence = DigitalProduct("D001", "Antivirus", 29.99, 100, supplier, 450.0)

    keyboard.supplier.display_information()
    licence.supplier.display_information()
    print("Both products share the same Supplier object:", keyboard.supplier is licence.supplier)

    del supplier  # only removes the NAME 'supplier'; products still hold references
    print("After 'del supplier':")
    keyboard.supplier.display_information()
    licence.supplier.display_information()


def test_aggregation() -> None:
    heading("3. Aggregation: Inventory and Product")
    supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")
    mouse = PhysicalProduct("P002", "Mouse", 25.0, 40, supplier, 0.2)  # exists first

    inv_a, inv_b = Inventory(), Inventory()
    inv_a.add_product(mouse)
    print("In A:", inv_a.find_product("P002") is mouse)

    removed = inv_a.remove_product("P002")
    print("Removed from A; A.find_product ->", inv_a.find_product("P002"))
    print("Product still usable:")
    mouse.display_information()
    print("remove_product returned the same object:", removed is mouse)

    inv_b.add_product(mouse)
    print("Added to B; same object in B:", inv_b.find_product("P002") is mouse)
    inv_b.remove_product("P002")
    print("B emptied, product still alive:", mouse.name, "| stock", mouse.stock)


def test_composition() -> None:
    heading("4. Composition: Order and OrderLine")
    supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")
    keyboard = PhysicalProduct("P001", "Keyboard", 120.0, 15, supplier, 1.5)
    licence = DigitalProduct("D001", "Antivirus", 29.99, 100, supplier, 450.0)

    order1, order2 = Order("O1"), Order("O2")
    order1.add_order_line(keyboard, 2)
    order1.add_order_line(licence, 1)
    order1.display_information()

    order2.add_order_line(keyboard, 1)  # same Product, different Order
    order2.display_information()

    line1, line2 = order1.order_lines[0], order2.order_lines[0]
    print("Same Product object in both lines:", line1.product is line2.product)
    print("Same OrderLine object:", line1 is line2)
    print("Distinct OrderLine objects:", len({id(l) for l in order1.order_lines + order2.order_lines}))
    print("Distinct Product objects:", len({id(l.product) for l in order1.order_lines + order2.order_lines}))

    order1.remove_order_line("D001")
    print("After removing a line from O1, total =", f"${order1.calculate_total():.2f}")
    print("Product still alive:", licence.name)


def test_polymorphism_and_lsp() -> None:
    heading("6/7. LSP and polymorphism")
    supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")
    inventory = Inventory()
    inventory.add_product(PhysicalProduct("P001", "Keyboard", 120.0, 15, supplier, 1.5))
    inventory.add_product(DigitalProduct("D001", "Antivirus", 29.99, 100, supplier, 450.0))

    print("-- show_product_details on each product --")
    for product in inventory.products:
        show_product_details(product)

    print("-- single loop over Product collection --")
    for product in inventory.products:
        product.display_information()
        print(product.get_fulfilment_info())

    print("-- LSP: update_stock behaves the same for both subclasses --")
    for product in inventory.products:
        product.update_stock(7)
        print(product.name, "stock ->", product.stock)
        try:
            product.update_stock(-1)
        except ValueError as err:
            print("  rejects negative stock the same way:", err)


if __name__ == "__main__":
    test_association()
    test_aggregation()
    test_composition()
    test_polymorphism_and_lsp()
    sys.exit(0)
