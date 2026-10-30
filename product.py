#Product class

class Product:

    def __init__(self, product_id, name, price, stock):         #Attributes
        self.__product_id == str(product_id).strip().upper()
        self.__name = str(name).strip()
        self.__price = Product.__validate_price(price)
        self.__stock = Product.__validate_stock(stock)
        if not self.__product_id:
            raise ValueError("Product ID cannot be empty.")
        if not self.__name:
            raise ValueError("Name cannot be empty.")

        #Self-Validation

        @staticmethod
        def __validate_price(price):        #Validate product price
            price = round(float(price), 2)
            if price <= 0:
                raise ValueError("Price must be more than $0")
            return price

        @staticmethod
        def __validate_stock(stock):        #Validate product stock
            if isinstance(stock, bool) or not isinstance(stock, int):
                raise ValueError("Stock must be a whole number.")
            if stock < 0:
                raise ValueError("Stock must be 0 or higher.")
            return stock

        #Properties

        @property
        def product_id(self):
            return self.__product_id

        @property
        def name(self):
            return self.__name

        @property
        def price(self):
            return self.__price

        @property
        def stock(self):
            return self.__stock

        #Behaviour

        def update_stock(self, quantity):       #Set new stock quantity
            self.__stock = Product.__validate_stock(quantity)

        def display_info(self):         #Display product information
            print(f"ID: {self.__product_id}|Name: {self.__name}|"
                  f"Price: ${self.__price:.2f}|Stock: {self.__stock}")

        #Dictionary Conversion

        def to_dict(self):
            return {
                "ID": self.__product_id,
                "Name": self.__name,
                "Price": self.__price,
                "Stock": self.__stock
            }

        @classmethod
        def from_dict(cls, data):
            return cls(data["ID"], data["Name"], data["Price"], data["Stock"])