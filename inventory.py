#Inventory class

class Inventory:

    def __init__(self):
        self.__products = []

    def add_product(self, product):         #Add new product
        if self.search_product(product.product_id) is not None:
            raise ValueError("Product ID already exists. Please enter a unique ID.")
        if self.find_by_name(product.name) is not None:
            raise ValueError("Product name already exists. Please enter a unique name.")
        self.__products.append(product)

    def search_product(self, product_id):       #Search for product by id
        product_id = product_id.strip().upper()
        return next((p for p in self.__products if p.product_id == product_id), None)

    def find_by_name(self, name):           #Search for product by name (case-insensitive)
        name = name.strip().lower()
        return next((p for p in self.__products if p.name.lower() == name), None)

    def display_all(self):          #Show full inventory
        print("\nCurrent Inventory")
        print("-------------------------------------------")
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()
        print("-------------------------------------------")

    def get_products(self):     
        return list(self.__products)

    def __len__(self):
        return len(self.__products)