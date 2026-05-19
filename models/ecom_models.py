from enum import Enum


class ProductCategory(str, Enum):
    soft_toy = "soft toy"
    constructor = "constructor"
    wear = "wear"
    paw_patrol = "paw patrol"


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    UAH = "UAH"
    PLN = "PLN"


class Product:
    title: str
    category: ProductCategory
    currency: Currency
    description: str | None
    stock_quantity: int
    image: str
    __price: int  # price in coins
    __stock_quantity: list[int]

    def __init__(
        self,
        title: str,
        category: ProductCategory,
        currency: Currency,
        description: str | None = None,
    ) -> None:
        self.title = title
        self.category = category
        self.currency = currency
        self.description = description

    def __str__(self):
        return f"{self.title} ({self.price})"

    def __repr__(self):
        return f"{self.title} ({self.price})"

    @property
    def price(self) -> int:
        return self.__price

    @property
    def stock_quantity(self) -> int:
        return sum(self.__stock_quantity)

    def update_stock(self, quantity: int) -> None:
        self.__stock_quantity.append(quantity)

    def change_price(self, new_price: int) -> None:
        self.__price = new_price


class Order:
    products: list[Product]
    total_price: int

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def calculate_total_price(self) -> None:
        self.total_price = sum(product.price for product in self.products)


class Customer:
    name: str
    email: str
    phone: str
    orders: list[Order]

    def __init__(self, name: str, email: str, phone: str) -> None:
        self.name = name
        self.email = email
        self.phone = phone

    def __str__(self):
        return f"{self.name} ({self.email})"

    def __repr__(self):
        return f"{self.name} ({self.email})"
