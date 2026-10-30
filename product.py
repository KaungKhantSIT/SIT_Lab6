#Product class

class Product:

    def __init__(self, product_id, name, price, stock):
        self.__product_id = str(product_id).strip().upper()
        self.__name = str(name).strip()
        self.__price = self.__validate_price(price)
        self.__stock = self.__validate_stock(stock)
        if not self.__product_id:
            raise ValueError("Product ID cannot be empty.")
        if not self.__name:
            raise ValueError("Name cannot be empty.")

    @staticmethod
    def __validate_price(price):
        price = round(float(price), 2)
        if price <= 0:
            raise ValueError("Price must be more than $0")
        return price

    @staticmethod
    def __validate_stock(stock):
        if isinstance(stock, bool) or not isinstance(stock, int):
            raise ValueError("Stock must be a whole number.")
        if stock < 0:
            raise ValueError("Stock must be 0 or higher.")
        return stock

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

    def update_stock(self, quantity):
        self.__stock = self.__validate_stock(quantity)

    def display_info(self):
        print(f"ID: {self.__product_id}|Name: {self.__name}|"
              f"Price: ${self.__price:.2f}|Stock: {self.__stock}")

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
