import json
import os
from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


def greetings() -> None:
    """Prints application header banner."""
    print("===============================================================")
    print("INVENTORY MANAGEMENT SYSTEM (Lab 8 Relationships Architecture)")
    print("===============================================================")


def test_abstract_instantiation() -> None:
    """
    Lab 7 Section 3.3 Test: Verifies that abstract class Product 
    cannot be instantiated directly.
    """
    print("\n--- Running Section 3.3 Test (Abstract Class Direct Instantiation) ---")
    try:
        invalid_product = Product("P999", "Generic Item", 10.0, 5, Supplier("S999", "X", "x@x.com"))  # type: ignore
        print("FAIL: Product was instantiated.")
    except TypeError as e:
        print("SUCCESS: Cannot instantiate abstract class Product directly.")
        print(f"Caught expected TypeError: {e}")
    print("-------------------------------------------------------------------\n")


DEFAULT_SUPPLIER = {
    "id": "S000",
    "name": "Unknown Supplier",
    "email": "unknown@example.com",
}


def get_or_create_supplier(data: dict, suppliers: dict[str, Supplier]) -> Supplier:
    """
    Returns the Supplier for this data, reusing one already created so products
    from the same supplier share a single Supplier object (association).
    """
    supplier_id = data["id"]
    if supplier_id not in suppliers:
        suppliers[supplier_id] = Supplier(supplier_id, data["name"], data["email"])
    return suppliers[supplier_id]


def create_product_from_dict(data: dict, suppliers: dict[str, Supplier]) -> Product:
    """Factory helper function to instantiate subclasses from dictionary data."""
    product_type = data.get("type", "physical")
    supplier = get_or_create_supplier(data.get("supplier", DEFAULT_SUPPLIER), suppliers)
    if product_type == "physical":
        return PhysicalProduct(
            product_id=data["id"],
            name=data["name"],
            price=data["price"],
            stock=data["qty"],
            supplier=supplier,
            weight=data.get("weight", 0.0),
        )
    elif product_type == "digital":
        return DigitalProduct(
            product_id=data["id"],
            name=data["name"],
            price=data["price"],
            stock=data["qty"],
            supplier=supplier,
            download_size=data.get("download_size", 0.0),
        )
    else:
        raise ValueError(f"Unknown product type: {product_type}")


def load_inventory(filename: str = "inventory.json") -> Inventory:
    """Loads product data from JSON into the Inventory instance."""
    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}

    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                for item in data:
                    product = create_product_from_dict(item, suppliers)
                    inventory.add_product(product)
                print(f"Loaded '{filename}' successfully.\n")
                return inventory
        except Exception as e:
            print(f"Error loading inventory file: {e}")
            return inventory
    else:
        print(f"'{filename}' not found. Initializing default inventory.")
        defaults = [
            {
                "id": "P001",
                "name": "Mechanical Keyboard",
                "price": 120.00,
                "qty": 15,
                "type": "physical",
                "weight": 1.5,
                "supplier": {"id": "S001", "name": "TechSupply Co", "email": "sales@techsupply.com"},
            },
            {
                "id": "D001",
                "name": "Antivirus License Key",
                "price": 29.99,
                "qty": 100,
                "type": "digital",
                "download_size": 450.0,
                "supplier": {"id": "S002", "name": "SoftWare Hub", "email": "info@softwarehub.com"},
            },
        ]
        for item in defaults:
            inventory.add_product(create_product_from_dict(item, suppliers))
        return inventory


def save_inventory(inventory: Inventory, filename: str = "inventory.json") -> None:
    """Serializes stored products into JSON format."""
    data = [product.to_dict() for product in inventory.get_all_products()]
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Inventory saved successfully to {filename}.")
    except Exception as e:
        print(f"Error saving inventory: {e}")


def prompt_supplier(inventory: Inventory) -> Supplier:
    """Asks for a supplier; reuses an existing Supplier object if the ID is known."""
    supplier_id = input("Supplier ID: ").strip()
    for product in inventory.get_all_products():
        if product.supplier.supplier_id == supplier_id:
            return product.supplier
    name = input("Supplier Name: ").strip()
    email = input("Supplier Email: ").strip()
    return Supplier(supplier_id, name, email)


def add_product_flow(inventory: Inventory) -> None:
    """User input prompt for adding a physical or digital product."""
    print("\nAdd New Product")
    prod_id = input("Product ID: ").strip()

    if inventory.find_product(prod_id):
        print("Product ID already exists!")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: ").strip())
        qty = int(input("Stock Quantity: ").strip())
        supplier = prompt_supplier(inventory)

        print("Select Product Type:")
        print("1. Physical Product")
        print("2. Digital Product")
        type_choice = input("Option (1/2): ").strip()

        if type_choice == "1":
            weight = float(input("Weight (kg): ").strip())
            new_product = PhysicalProduct(prod_id, name, price, qty, supplier, weight)
        elif type_choice == "2":
            size = float(input("Download Size (MB): ").strip())
            new_product = DigitalProduct(prod_id, name, price, qty, supplier, size)
        else:
            print("Invalid product type selected.")
            return

        inventory.add_product(new_product)
        print("Product added successfully!")
    except ValueError:
        print("Invalid input format entered.")


def search_product_flow(inventory: Inventory) -> None:
    """Searches product and displays fulfillment details and shipping calculations."""
    print("\nSearch Product")
    prod_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(prod_id)

    if product:
        print("\nProduct Details")
        print("-" * 45)
        product.display_information()
        print(f"Fulfilment: {product.get_fulfilment_info()}")
        product.display_supplier_information()

        if isinstance(product, CanBeShipped):
            shipping_fee = product.calculate_shipping_cost()
            print(f"Calculated Shipping Cost ($0.30/kg): ${shipping_fee:.2f}")
        else:
            print("Shipping: N/A (Digital Product)")
        print("-" * 45)
    else:
        print("\nProduct not found.")


def main() -> None:
    """Main execution loop."""
    greetings()
    test_abstract_instantiation()

    json_path = "inventory.json"
    inventory = load_inventory(json_path)

    while True:
        print("\nMENU")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        choice = input("Enter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_flow(inventory)
        elif choice == "3":
            prod_id = input("Enter Product ID: ").strip()
            prod = inventory.search_product(prod_id)
            if prod:
                try:
                    new_q = int(input("New Stock: ").strip())
                    prod.update_stock(new_q)
                    print("Stock updated.")
                except ValueError as err:
                    print(f"Error: {err}")
            else:
                print("Product not found.")
        elif choice == "4":
            search_product_flow(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            save_inventory(inventory)
            print("Program terminated.")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()