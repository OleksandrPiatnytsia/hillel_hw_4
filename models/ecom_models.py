from enum import Enum
from uuid import uuid4, UUID


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
    id: str
    title: str
    category: ProductCategory
    currency: Currency
    description: str | None
    __price: int  # price in coins
    __stock_quantity: list[int]

    def __init__(
        self,
        title: str,
        category: ProductCategory,
        currency: Currency,
        description: str | None = None,
    ) -> None:
        self.id = str(uuid4())
        self.title = title
        self.category = category
        self.currency = currency
        self.description = description
        self.__price = 0
        self.__stock_quantity = []

    def __str__(self):
        return f"({self.id}) {self.title} ({self.price})"

    def __repr__(self):
        return f"({self.id}) {self.title} ({self.price})"

    def __eq__(self, other):
        return isinstance(other, Product) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

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

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category.value,
            "currency": self.currency.value,
            "description": self.description,
            "price": self.__price,
            "stock_quantity": self.__stock_quantity,
        }

    @classmethod
    def from_dict(cls, data: dict):
        product = cls(
            title=data["title"],
            category=ProductCategory(data["category"]),
            currency=Currency(data["currency"]),
            description=data.get("description"),
        )

        product.id = data["id"]
        product._Product__price = data["price"]
        product._Product__stock_quantity = data["stock_quantity"]

        return product


class Order:
    id: str
    products: list[Product]
    total_price: int

    def __init__(self) -> None:
        self.id = str(uuid4())
        self.products = []
        self.total_price = 0

    def __eq__(self, other):
        return isinstance(other, Order) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def calculate_total_price(self) -> None:
        self.total_price = sum(product.price for product in self.products)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "products": [product.to_dict() for product in self.products],
            "total_price": self.total_price,
        }

    @classmethod
    def from_dict(cls, data: dict):
        order = cls()

        order.id = data["id"]
        order.products = [
            Product.from_dict(product_data) for product_data in data["products"]
        ]

        order.total_price = data["total_price"]

        return order


class Customer:
    id: str
    name: str
    email: str
    phone: str
    orders: list[Order]

    def __init__(self, name: str, email: str, phone: str) -> None:
        self.id = str(uuid4())
        self.name = name
        self.email = email
        self.phone = phone
        self.orders = []

    def __str__(self):
        return f"{self.name} ({self.email})"

    def __repr__(self):
        return f"{self.name} ({self.email})"

    def __eq__(self, other):
        return isinstance(other, Customer) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def add_order(self, order: Order) -> None:
        self.orders.append(order)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "orders": [order.to_dict() for order in self.orders],
        }

    @classmethod
    def from_dict(cls, data: dict):
        customer = cls(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
        )

        customer.id = data["id"]
        customer.orders = [Order.from_dict(order_data) for order_data in data["orders"]]

        return customer
