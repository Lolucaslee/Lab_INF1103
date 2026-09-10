inventory_count = 0

while True:
    input_value = input("Enter a stock quantity (or type 'quit' to quit): ")
    if input_value == 'quit':
        break
    elif not input_value.isdigit() or int(input_value) < 0:
        print("Error, invalid input")    
    else:
        inventory_count += int(input_value)
    if inventory_count >= 500:
        print("The total inventory has exceeded 500 units.")
        break