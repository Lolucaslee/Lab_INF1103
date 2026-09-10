inventory_count = 0
input_value = 0
error_count = 0

while inventory_count < 500:
    input_value = input("Enter the number of items in inventory (or type 'exit' to quit): ")
    if input_value == 'exit':
        error_count += 1
        break
    elif not input_value.isdigit() or int(input_value) < 0:
        print("Error, invalid input")    
    else:
        inventory_count += int(input_value)
    if inventory_count >= 500:
        print("The total inventory has exceeded 500 units.")
        break

print("Total units processed",inventory_count, "& Number of failed entries: ",error_count)