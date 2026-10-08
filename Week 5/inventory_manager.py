import json
import os


def greetings():
    print("===============================================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("===============================================================")


def load_inventory(filename="inventory.json"):
    """Loads inventory from inventory.json.

    Initializes defaults if missing.
    """
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                inventory = json.load(file)
                print("inventory.json found.")
                print("Inventory loaded successfully.\n")
                return inventory
        except Exception as e:
            print(f"Error loading inventory file: {e}")
            return []
    else:
        print("inventory.json not found. Initializing default inventory.")
        # Default starter inventory (at least three products)
        default_inventory = [
            {"id": "P001", "name": "Laptop", "price": 1200.00, "qty": 15},
            {"id": "P002", "name": "Mouse", "price": 25.50, "qty": 40},
            {"id": "P003", "name": "Keyboard", "price": 45.00, "qty": 25},
        ]
        return default_inventory


def save_inventory(inventory, filename="inventory.json"):
    """Saves the inventory list to inventory.json."""
    try:
        with open(filename, "w") as file:
            json.dump(inventory, file, indent=4)
        print(f"Inventory saved successfully to {filename}.")
    except Exception as e:
        print(f"Error saving inventory: {e}")


def display_all(inventory):
    """Displays all products in the inventory."""
    print("\nCurrent Inventory")
    if not inventory:
        print("No products in inventory.")
        return

    for item in inventory:
        print(
            f"ID: {item['id']} | Name: {item['name']} | Price: ${item['price']:.2f} | Stock: {item['qty']}"
        )


def add_product(inventory):
    """Adds a new product entry to the inventory."""
    print("\nAdd New Product")
    prod_id = input("Product ID: ").strip()

    # Check if product ID already exists
    for item in inventory:
        if item["id"].lower() == prod_id.lower():
            print("Product ID already exists!")
            return inventory

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: ").strip())
        qty = int(input("Stock Quantity: ").strip())
    except ValueError:
        print("Invalid input for price or stock quantity.")
        return inventory

    new_item = {"id": prod_id, "name": name, "price": price, "qty": qty}

    inventory.append(new_item)
    print("Product added successfully!")
    return inventory


def update_stock(inventory):
    """Updates the stock quantity of an existing product by ID."""
    print("\nUpdate Stock")
    prod_id = input("Enter Product ID: ").strip()

    for item in inventory:
        if item["id"].lower() == prod_id.lower():
            print("\nProduct Found:")
            print(f"Name: {item['name']}")
            print(f"Current Stock: {item['qty']}\n")

            try:
                new_qty = int(input("New Stock Quantity: ").strip())
                item["qty"] = new_qty
                print("\nStock updated successfully!")
            except ValueError:
                print("Invalid input for stock quantity.")
            return inventory

    print("\nProduct not found.")
    return inventory


def search_product(inventory):
    """Searches for a product by its ID."""
    print("\nSearch Product")
    prod_id = input("Enter Product ID: ").strip()

    for item in inventory:
        if item["id"].lower() == prod_id.lower():
            print("\nProduct Found")
            print("-" * 30)
            print(f"ID: {item['id']}")
            print(f"Name: {item['name']}")
            print(f"Price: ${item['price']:.2f}")
            print(f"Stock: {item['qty']}")
            print("-" * 30)
            return

    print("\nProduct not found.")


def display_menu():
    print("\nMENU")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")


def main():
    greetings()
    inventory = load_inventory()

    while True:
        display_menu()
        choice = input("Enter option: ").strip()

        if choice == "1":
            display_all(inventory)
        elif choice == "2":
            inventory = add_product(inventory)
        elif choice == "3":
            inventory = update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
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