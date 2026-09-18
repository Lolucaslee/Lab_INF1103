
def greetings():
    print("===============================================================")
    print("Welcome to the Order/Delivery Service")
    print("===============================================================")

def get_valid_input():
    input_value = input("Enter a stock quantity (or type 'quit' to quit): ")
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
    print("Total tax value      :", tax_value)

def main():
    # Say HI :)
    greetings()
    inventory_count = 0
    error_count = 0
    delivery_count = 0
    total_tax = 0
    while True:
        result = get_valid_input()
        if result == "quit":
            break
        elif result is None:
            error_count += 1
        else:
            delivery_count += 1
            inventory_count = process_delivery(inventory_count, result)
            total_tax = calculate_tax(inventory_count)
            
            if inventory_count >= 500:
                print("The total inventory has exceeded 500 units.")
                break

    generate_report(inventory_count, error_count, delivery_count, total_tax)
    
main()