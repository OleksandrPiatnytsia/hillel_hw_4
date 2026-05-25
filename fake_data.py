import random

from faker import Faker

from models.ecom_models import (
    Customer,
    Product,
    ProductCategory,
    Currency,
    OrderItem,
    ProductsCollection,
)

fake = Faker()


def create_random_product() -> Product:
    product = Product(
        title=fake.word().title(),
        category=random.choice(list(ProductCategory)),
        currency=random.choice(list(Currency)),
        description=fake.sentence(),
    )

    product.change_price(random.randint(10, 50))
    product.update_stock(random.randint(50, 200))

    return product


def create_random_customer() -> Customer:
    customer = Customer(
        name=fake.name(),
        email=fake.email(),
        phone=fake.phone_number(),
    )

    return customer


def create_random_order_item() -> OrderItem:
    product = ProductsCollection().get_random_product()

    order_item = OrderItem(
        product=product,
        quantity=random.randint(1, 100),
        price=product.price,
        discount=random.choice(
            [5, 10, 15, 20],
        ),
    )

    return order_item
