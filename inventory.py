# Importing tabuate to create tables. 
from tabulate import tabulate

# Defining the starting show class
class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = float(cost)
        self.quantity = int(quantity)
# defning three methods 
    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f"{self.country},{self.code},{self.product},${self.cost},{self.quantity}"


# Creating empty shoe list. 
shoe_list = []


# Functions for menu
def read_shoes_data():
    # Try to read the file
    try:
        with open("inventory.txt", "r") as file:
            # Skipping the first header in the text file
            next(file)  
            # Reading data in text file
            for line in file:
                data = line.strip().split(",")
                shoe = Shoe(*data)
                shoe_list.append(shoe)
                # Printing fail or false messages
        print("Inventory data has been collected.")
    except FileNotFoundError:
        print("No file found.")


def capture_shoes():
    # Creating inputs for new shoes. 
    country = input("Enter the country: ")
    code = input("Enter the shoe code: ")
    product = input("Enter the product name: ")
    cost = input("Enter the cost of the shoe: ")
    quantity = input("Enter the quantity of the shoe: ")
    shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(shoe)
    # Printing output message
    print("New shoe has been addedd.")


def view_all():
    headers = ["Country", "Code", "Product", "Cost", "Quantity"]
    data = []
    for shoe in shoe_list:
        data.append([shoe.country, shoe.code, shoe.product, f"${shoe.cost}", shoe.quantity])
        # tabulate to print out in a table.
    print(tabulate(data, headers=headers))


def re_stock():
    # Searching for lowest stock of shoe
    lowest_quantity_shoe = min(shoe_list, key=lambda shoe: shoe.quantity)
    print(f"The shoe with the lowest quantity is: {lowest_quantity_shoe}")
    # Creating input message for user to input new data
    add_qty = input("Do you want to restock this show? (y/n): ")
    if add_qty.lower() == "y":
        qty_to_add = input("Enter the quantity to add: ")
        lowest_quantity_shoe.quantity += int(qty_to_add)
        # Writing new shoe into the text file. 
        with open("inventory.txt", "r") as file:
            lines = file.readlines()
        with open("inventory.txt", "w") as file:
            for line in lines:
                data = line.strip().split(",")
                if data[1] == lowest_quantity_shoe.code:
                    data[-1] = str(lowest_quantity_shoe.quantity)
                    line = ",".join(data) + "\n"
                file.write(line)
                # Printing messages for fail or false input. 
        print("Stock has been added.")
    else:
        print("Failed to add stock.")


def search_shoe():
    code = input("Enter the shoe code: ")
    # Searching for shoe code from shoe list
    for shoe in shoe_list:
        if shoe.code == code:
            # Prinitng fail or false input messages. 
            print(f"The shoe with code {code} is: {shoe}")
            break
    else:
        print(f"Shoe with code {code} not found.")


def value_per_item():
    # Searching for values in table
    headers = ["Product", "Total Value"]
    data = []
    for shoe in shoe_list:
        total_value = shoe.cost * shoe.quantity
        data.append([shoe.product, f"${total_value}"])
        # Printing values in a table. 
    print(tabulate(data, headers=headers))


def highest_qty():
    # Seaching for higest stock
    highest_qty_shoe = max(shoe_list, key=lambda shoe: shoe.quantity)
    # Printing error message 
    print(f"The shoe for sale with the most stock is: {highest_qty_shoe}")

# Creating a menu for user. 
while True:
    print("SHOE INVENTORY")
    print("1. Read shoes data from inventory")
    print("2. Input new shoe")
    print("3. View all stock")
    print("4. Re-stock shoes")
    print("5. Search for a shoe")
    print("6. View value per item")
    print("7. View shoe with highest stock")
    print("8. Exit")
    choice = input("Please pick a number: ")

    if choice == "1":
        read_shoes_data()
    elif choice == "2":
        capture_shoes()
    elif choice == "3":
        view_all()
    elif choice == "4":
        re_stock()
    elif choice == "5":
        search_shoe()
    elif choice == "6":
        value_per_item()
    elif choice == "7":
        highest_qty()
    elif choice == "8":
        print("Exiting inventory managment")
        break
    else:
        print("You have to pick a number.")
