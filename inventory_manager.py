#Main Program

import json
import math
import re

from product import Product
from inventory import Inventory

#Convert text to a non-negative int
def parse_qty(raw):
    try:
        qty = int(raw)
    except ValueError:
        raise ValueError("Please enter a valid number.")
    if qty < 0:
        raise ValueError("Please enter a non-negative number.")
    return qty

#Convert text to a price above $0, rounded to 2 decimals
def parse_price(raw):
    try:
        price = round(float(raw), 2)
    except ValueError:
        raise ValueError("Please enter a valid number.")
    if not math.isfinite(raw):
        raise ValueError("Please enter a real number.")
    if price <= 0:
        raise ValueError("Please enter a price above $0.")
    return price

#Check product ID format
def parse_id(raw,format=re.compile(r"P[0-9]{3,}")):
    pid = raw.upper()
    if not format.fullmatch(pid):
        raise ValueError("Please enter a valid product ID (e.g. P001).")
    return pid

#Prompt until input is validated using required parse function
def prompt_until_valid(prompt, parse):
    while True:
        raw = input(prompt).strip()
        try:
            return parse(raw)
        except ValueError as err:
            print(err)

#Load inventory from json file
def load_inventory(filename):
    inventory = Inventory()
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        print(f"{filename} found.")
    #Empty inventory if file not found
    except (FileNotFoundError, json.JSONDecodeError, OSError) as err:
        print(f"Could not read {filename} ({err}). Starting with an empty inventory.\n")
        return inventory
    for item in data:
        try:
            inventory.add_product(Product.from_dict(item))
        except (KeyError, ValueError, TypeError) as err:
            print(f"Skipped invalid record {item}: {err}")
    print("Inventory loaded successfully.\n")
    return inventory

#Save inventory to json file
def save_inventory(filename, inventory):
    print("\nSaving inventory...")
    try:
        with open(filename, 'w') as file:
            json.dump([product.to_dict() for product in inventory.get_products()], file, indent=4)
        print(f"Inventory saved successfully to {filename}.")
    except OSError as err:
        print(f"Could not save inventory: {err}")
    
#Add new product to inventory
def add_product(inventory):
    print("\nAdd New Product")
    #Prompt for Product ID
    while True:
        pid = prompt_until_valid("Product ID: ", parse_id)
        #Check if ID already exists
        if inventory.search_product(pid):
            print("Product ID already exists. Please enter a unique ID.")
        else:
            break
    #Prompt for Product Name
    while True:
        name = input("Product Name: ").strip()
        #Check that name is not empty
        if not name:
            print("Name cannot be empty.")
        #Check if product name already exists
        elif inventory.find_by_name(name):
            print("Product name already exists. Please enter a unique name.")
        else:
            break
    #Prompt for Price & Stock
    price = prompt_until_valid("Price($): ", parse_price)
    stock = prompt_until_valid("Stock Quantity: ", parse_qty)
    #Create and add product to inventory
    try:
        inventory.add_product(Product(pid,name,price,stock))
        print("\nProduct added successfully!")
    except ValueError as err:
        print(f"\n{err}")

#Update stock of product
def update_stock(inventory):
    pid = prompt_until_valid("Enter Product ID: ", parse_id)
    product = inventory.search_product(pid)
    #Check if product exists
    if product is None:
        print("\nProduct Not Found")
        return
    print(f"Product Found:\nName: {product.name}\nCurrent Stock: {product.stock}\n")
    #Update Stock
    while True:
        qty = prompt_until_valid("New Stock Quantity: ", parse_qty)
        try:
            product.update_stock(qty)
            break
        except ValueError as err:
            print(f"\n{err}")
    print("\nStock updated successfully!")

#Search and display product in inventory
def search_product(inventory):
    print("Search Product")
    pid = prompt_until_valid("Enter Product ID: ", parse_id)
    product = inventory.search_product(pid)
    if product is None:
        print("\nProduct Not Found")
    else:
        print("\nProduct Found")
        print("-------------------------------------------")
        product.display_info()
        print("-------------------------------------------")

#print menu options
def menu_page(menu):
    print("---------MENU---------")
    for i, option in enumerate(menu.keys(), start=1):
        print(f"{i}. {option}")
    print("----------------------\n")
    while True:
        option = input(f"Enter option (1-{len(menu)}): ").strip()
        if option.isdigit() and 1 <= int(option) <= len(menu):
            return list(menu.keys())[int(option) - 1]
        else:
            print("Invalid option. Please select a valid option.")

#Manager main program function
def manager():
    file = "inventory.json"
    #Title
    print("============================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("============================\n")
    # Load inventory from file
    inventory = load_inventory(file)
    #User menu options
    menu = {
        "Display All Products": inventory.display_all,
        "Add New Product": lambda: add_product(inventory),
        "Update Stock": lambda: update_stock(inventory),
        "Search Product": lambda: search_product(inventory),
        "Save Inventory": lambda: save_inventory(file, inventory),
        "Exit": None
    }
    #Menu
    try:
        while True:
            option = menu_page(menu)
            if option == "Exit":
                break
            menu[option]()
            input("\nPress Enter to return to the menu...")
    #Ctrl+C / Ctrl+D (or no interactive input) - exit cleanly instead of crashing
    except (KeyboardInterrupt, EOFError):
        print("\n\nInput interrupted.")
    save_inventory(file, inventory)
    print("\nThank you for using the Inventory Management System.")
    print("Program terminated.")
    
#Run main program
if __name__ == "__main__":
    manager()