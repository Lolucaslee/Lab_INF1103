inventory_count = 0
input_value = 0
error_count = 0

while True:
    input_value = input("Enter a stock quantity (or type 'quit' to quit): ")
    if input_value == 'quit':
        break
    elif not input_value.isdigit() or int(input_value) < 0:
        print("Error, invalid input")    
        error_count += 1

    else:
        inventory_count += int(input_value)
    if inventory_count >= 500:
        print("The total inventory has exceeded 500 units.")
        break
    
print("Total units processed",inventory_count)
print("Number of failed entries: ",error_count)
