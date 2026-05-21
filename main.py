from models.ecom_models import Order
from fake_data import create_random_product, create_random_customer
import random
from serialization.json_serialization import JsonDataSerialization


def main():

    customers, products = JsonDataSerialization.load_data()

    # Додаємо випадкових customers
    for _ in range(random.randint(0, 3)):
        customers.append(create_random_customer())

    # Додаємо випадкові products
    for _ in range(random.randint(0, 3)):
        products.append(create_random_product())

    # Якщо продуктів немає — створюємо хоча б один
    if not products:
        products.append(create_random_product())

    # Якщо customers немає — створюємо хоча б одного
    if not customers:
        customers.append(create_random_customer())

    for _ in range(10):

        new_order = Order()

        for __ in range(random.randint(1, 6)):

            random_product = random.choice(products)

            new_order.add_product(random_product)

        new_order.calculate_total_price()

        random_customer = random.choice(customers)

        random_customer.add_order(new_order)

    # print(f"\nCustomers count: {len(customers)}")
    # print(f"Products count: {len(products)}")

    JsonDataSerialization.save_data(customers)


if __name__ == "__main__":
    main()
