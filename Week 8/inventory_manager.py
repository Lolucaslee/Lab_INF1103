import json
import os
from product import Product
from inventory import Inventory


def greetings():
    """Prints the system header banner."""
    print("===============================================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("===============================================================")


def load_inventory(filename="inventory.json") -> Inventory:
    """
    Loads product data from inventory.json into an Inventory instance.
    Uses Week 5 default starter list if the file is missing.
    """
    inventory = Inventory()

    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                for item in data:
                    product = Product.from_dict(item)
                    inventory.add_product(product)
                print("inventory.json found.")
                print("Inventory loaded successfully.\n")
                return inventory
        except Exception as e:
            print(f"Error loading inventory file: {e}")
            return inventory
    else:
        print("inventory.json not found. Initializing default inventory.")
        # Starter default list from Week 5
        defaults = [
            {"id": "P001", "name": "Laptop", "price": 1200.00, "qty": 15},
            {"id": "P002", "name": "Mouse", "price": 25.50, "qty": 40},
            {"id": "P003", "name": "Keyboard", "price": 45.00, "qty": 25},
        ]
        for item in defaults:
            inventory.add_product(Product.from_dict(item))
        return inventory


def save_inventory(inventory: Inventory, filename="inventory.json"):
    """Serializes Product objects in Inventory back to inventory.json."""
    data = [product.to_dict() for product in inventory.get_all_products()]
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Inventory saved successfully to {filename}.")
    except Exception as e:
        print(f"Error saving inventory: {e}")


def add_product_flow(inventory: Inventory):
    """Handles user input prompts for adding a new product."""
    print("\nAdd New Product")
    prod_id = input("Product ID: ").strip()

    if inventory.search_product(prod_id):
        print("Product ID already exists!")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: ").strip())
        qty = int(input("Stock Quantity: ").strip())
        new_product = Product(prod_id, name, price, qty)
        inventory.add_product(new_product)
        print("Product added successfully!")
    except ValueError:
        print("Invalid input for price or stock quantity.")


def update_stock_flow(inventory: Inventory):
    """Handles user input prompts for updating product stock."""
    print("\nUpdate Stock")
    prod_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(prod_id)

    if product:
        print("\nProduct Found:")
        print(f"Name: {product.name}")
        print(f"Current Stock: {product.stock}\n")

        try:
            new_qty = int(input("New Stock Quantity: ").strip())
            product.update_stock(new_qty)
            print("\nStock updated successfully!")
        except ValueError as e:
            print(f"Invalid input for stock quantity: {e}")
    else:
        print("\nProduct not found.")


def search_product_flow(inventory: Inventory):
    """Handles searching and displaying a single product's detailed view."""
    print("\nSearch Product")
    prod_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(prod_id)

    if product:
        print("\nProduct Found")
        print("-" * 30)
        print(f"ID: {product.product_id}")
        print(f"Name: {product.name}")
        print(f"Price: ${product.price:.2f}")
        print(f"Stock: {product.stock}")
        print("-" * 30)
    else:
        print("\nProduct not found.")


def display_menu():
    """Displays user menu options."""
    print("\nMENU")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")


def main():
    """Main execution loop."""
    greetings()
    inventory = load_inventory()

    while True:
        display_menu()
        choice = input("Enter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_flow(inventory)
        elif choice == "3":
            update_stock_flow(inventory)
        elif choice == "4":
            search_product_flow(inventory)
        elif choice == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
        elif choice == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()