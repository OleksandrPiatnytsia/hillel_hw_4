import random

from faker import Faker

from models.ecom_models import (
    Customer,
    Product,
    ProductCategory,
    Currency,
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
    product.update_stock(random.randint(1, 100))

    return product


def create_random_customer() -> Customer:
    customer = Customer(
        name=fake.name(),
        email=fake.email(),
        phone=fake.phone_number(),
    )

    return customer
