inventory_count = 0

while True:
    input_value = input("Enter a stock quantity (or type 'quit' to quit): ")
    if input_value == 'quit':
        break
    elif not input_value.isdigit():
        print("Error, invalid input")    