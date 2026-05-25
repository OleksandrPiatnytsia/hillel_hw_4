import random
from enum import Enum
from typing import Any, Self
from uuid import uuid4
from abc import ABC, abstractmethod
from collections import UserDict

from models.metaclases import SingletonMeta


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


class SerializationDefine(ABC):
    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        pass


class UniqueIdentifier:
    __id: str

    def __init__(self) -> None:
        self.__id = str(uuid4())

    @property
    def id(self) -> str:
        return self.__id


class Product(UniqueIdentifier, SerializationDefine):
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

        super().__init__()
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
        if self.stock_quantity + quantity < 0:
            raise ValueError("Insufficient stock")

        self.__stock_quantity.append(quantity)

    def change_price(self, new_price: int) -> None:

        if new_price < 0:
            raise ValueError("Price cannot be negative")

        self.__price = new_price

    def to_dict(self) -> dict[str, Any]:
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
    def from_dict(cls, data: dict[str, Any]):
        product = cls(
            title=data["title"],
            category=ProductCategory(data["category"]),
            currency=Currency(data["currency"]),
            description=data.get("description"),
        )

        product._UniqueIdentifier__id = data["id"]
        product._Product__price = data["price"]
        product._Product__stock_quantity = data["stock_quantity"]

        return product


class ProductsCollection(
    UserDict[str, Product],
    metaclass=SingletonMeta,
):
    def add_product(self, product: Product) -> None:
        self.data[product.id] = product

    def find_product(self, product_id: str) -> Product | None:
        return self.data.get(product_id)

    def delete(self, product_id: str) -> None:
        self.data.pop(product_id, None)

    def get_random_product(self) -> Product:
        return random.choice(list(self.data.values()))


class OrderItem(SerializationDefine):
    product: Product
    quantity: int
    price: int
    discount: int
    item_total_price: int

    def __init__(
        self,
        product: Product,
        quantity: int,
        price: int | None = None,
        discount: int = 0,
    ) -> None:
        self.product = product
        self.quantity = quantity
        self.price = self.product.price if price is None else price
        self.discount = discount
        self.calculate_item_total_price()

    def calculate_item_total_price(self) -> None:
        self.item_total_price = (
            self.price * self.quantity * (100 - self.discount)
        ) // 100

    def to_dict(self) -> dict[str, Any]:
        return {
            "product_id": self.product.id,
            "quantity": self.quantity,
            "price": self.price,
            "discount": self.discount,
            "item_total_price": self.item_total_price,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]):

        product = ProductsCollection().find_product(data["product_id"])

        if not product:
            raise ValueError("Product not found")

        order_item = cls(
            product=product,
            quantity=data["quantity"],
            price=data["price"],
            discount=data["discount"],
        )
        order_item.item_total_price = data["item_total_price"]

        return order_item


class Order(UniqueIdentifier, SerializationDefine):

    total_price: int
    order_items: list[OrderItem]

    def __init__(self) -> None:
        super().__init__()
        self.order_items = []
        self.total_price = 0

    def __eq__(self, other):
        return isinstance(other, Order) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def add_order_item(self, new_order_item: OrderItem) -> bool:

        if new_order_item.quantity > new_order_item.product.stock_quantity:
            print(
                f"Order item quantity:{new_order_item.quantity} exceeds product stock quantity:"
                f" {new_order_item.product.stock_quantity}"
            )
            return False

        existing_order_item = next(
            (
                item
                for item in self.order_items
                if item.product == new_order_item.product
            ),
            None,
        )

        if existing_order_item:
            print(
                f"{existing_order_item.product}. "
                f"Adding quantity: {new_order_item.quantity} "
                f"to existing quantity: {existing_order_item.quantity}"
            )

            existing_order_item.quantity += new_order_item.quantity

            print(
                f"{existing_order_item.product}. Після Додавання: {existing_order_item.quantity}"
            )

            existing_order_item.discount = min(
                existing_order_item.discount, new_order_item.discount
            )
            existing_order_item.price = min(
                existing_order_item.price, new_order_item.price
            )

        else:

            self.order_items.append(new_order_item)

        new_order_item.product.update_stock(-new_order_item.quantity)

        self.calculate_total_price()

        return True

    def calculate_total_price(self) -> None:
        self.total_price = sum(
            order_item.item_total_price for order_item in self.order_items
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "order_items": [order_item.to_dict() for order_item in self.order_items],
            "total_price": self.total_price,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        order = cls()

        order._UniqueIdentifier__id = data["id"]
        order.order_items = [
            OrderItem.from_dict(order_item) for order_item in data["order_items"]
        ]

        order.total_price = data["total_price"]

        return order


class Customer(UniqueIdentifier, SerializationDefine):
    name: str
    email: str
    phone: str
    orders: list[Order]

    def __init__(self, name: str, email: str, phone: str) -> None:
        super().__init__()
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

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "orders": [order.to_dict() for order in self.orders],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        customer = cls(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
        )

        customer._UniqueIdentifier__id = data["id"]
        customer.orders = [Order.from_dict(order_data) for order_data in data["orders"]]

        return customer
