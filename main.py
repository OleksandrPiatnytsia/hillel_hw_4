from models.ecom_models import Order, ProductsCollection, Customer
from fake_data import (
    create_random_product,
    create_random_customer,
    create_random_order_item,
)
import random
from serialization.json_serialization import JsonDataSerialization

LOWER_STOCK_QUANTITY = 25


def main():

    products, customers = JsonDataSerialization.load_data()

    # Додаємо випадкових customers
    for _ in range(random.randint(0, 3)):
        customers.append(create_random_customer())

    for product in products.values():
        if product.stock_quantity < LOWER_STOCK_QUANTITY:
            product.update_stock(random.randint(25, 100))

    # Додаємо випадкові products
    for _ in range(random.randint(0, 5)):
        products.add_product(create_random_product())

    # Якщо продуктів немає — створюємо хоча б один
    if not products:
        products.add_product(create_random_product())

    # Якщо customers немає — створюємо хоча б одного
    if not customers:
        customers.append(create_random_customer())

    for _ in range(10):

        new_order = Order()

        for __ in range(random.randint(1, 6)):

            new_order.add_order_item(create_random_order_item())

        new_order.calculate_total_price()

        random_customer = random.choice(customers)

        if new_order.order_items:
            random_customer.add_order(new_order)

    # print(f"\nCustomers count: {len(customers)}")
    # print(f"Products count: {len(products)}")

    JsonDataSerialization.save_data(products, customers)


if __name__ == "__main__":
    main()
