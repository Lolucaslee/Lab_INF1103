import os   

def greetings():
    print("===============================================================")
    print("Welcome to the Order/Delivery Service")
    print("===============================================================")

def load_inventory(filename="orders.txt"):
    # Attempting to read the inventory from txt file, if does not exist, will create a new one
    orders = []
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                            parts = [p.strip() for p in line.split(",")]
                            if len(parts) == 3 and parts[0].isdigit() and parts[2].isdigit():
                                orders.append({
                                    "id": int(parts[0]),
                                    "name": parts[1],
                                    "qty": int(parts[2])
                                })
        except Exception as e:
            print(f"Error loading inventory file: {e}")
            return orders
    else:
        # Initiate default inventory list
        orders = [{"id": 1001, "name": "Mouse", "qty": 0},
                  {"id": 1002, "name": "Keyboard", "qty": 0},]
    return orders

def save_inventory(orders, filename="orders.txt"):
    # Saves the complete order history list back to orders.txt.``
    try:
        with open(filename, "w") as file:
            for item in orders:
                file.write(f"{item['id']}, {item['name']}, {item['qty']}\n")
        print(f"\nOrder successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving inventory: {e}")

def add_inventory(orders, identifier, quantity):
    # Create a new product entry or update an existing one based on the identifier (ID or Name)
    existing_item = None

    # Search for match by ID or Name (case-insensitive)
    for item in orders:
        if identifier.isdigit() and int(identifier) == item["id"]:
            existing_item = item
            break
        elif item["name"].lower() == identifier.lower():
            existing_item = item
            break

    if existing_item:
        # Update quantity for matched product
        existing_item["qty"] += quantity
        print("\nOrder Updated:")
        print(f"Code: {existing_item['id']}, Item: {existing_item['name']}, Quantity: {existing_item['qty']}")
    else:
        # Create new product entry with auto-incremented ID
        next_id = max([item["id"] for item in orders], default=1000) + 1
        new_order = {
            "id": next_id,
            "name": identifier,
            "qty": quantity
        }
        orders.append(new_order)
        print("\nNew Order Added:")
        print(f"Code: {new_order['id']}, Item: {new_order['name']}, Quantity: {new_order['qty']}")

    return orders

def get_valid_input():
    input_value = input("Enter a stock name (or type 'quit' to quit): ")
    if input_value.lower() == 'quit':
        return 'quit'
    if input_value.isdigit() and int(input_value) >= 0:
        return int(input_value)
    else:
        print("Error, invalid input")
        return None

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(inventory_count, tax_rate=0.1):
    return inventory_count * tax_rate

def generate_report(inventory_count, error_count, delivery_count, tax_value):
    print("===============================================================")
    print("Order/Delivery Report")
    print("===============================================================")
    print("Total units processed:", inventory_count)
    print("Delivery Count       :", delivery_count)
    print("Number of failed entries:", error_count)
    print("Total tax value      :", f"${tax_value:.2f}")

def main():
    # 1. Display greeting header
    greetings()
    while True:
        # 2. Load existing orders from file
        orders = load_inventory()

        # 3. Display current orders
        print("\nCurrent Orders:\n")
        for item in orders:
            print(f"Code: {item['id']}, Item: {item['name']}, Quantity: {item['qty']}")
        print()

        error_count = 0

        # 4. User input prompt for Code or Name
        identifier = input("Enter Product Code or Name: ").strip()
        if identifier.lower() == 'quit':
            break

        qty_input = input("Enter Quantity: ").strip()

        # Validate input quantity
        if qty_input.isdigit() and int(qty_input) >= 0:
            quantity = int(qty_input)

            # 5. Call function to update or add item
            orders = add_inventory(orders, identifier, quantity)

            # 6. Save updated list to file
            save_inventory(orders)
        else:
            print("Error, invalid input")
            error_count += 1

        # 7. Calculate total metrics for report
        inventory_count = sum(item["qty"] for item in orders)
        delivery_count = len(orders)
        total_tax = calculate_tax(inventory_count)

    # 8. Print final summary report
    generate_report(inventory_count, error_count, delivery_count, total_tax)

    
main()