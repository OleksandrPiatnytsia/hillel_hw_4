from models.ecom_models import Customer, Product, Order, ProductCategory, Currency


def main():

    teddy_bear = Product(
        "Teddy bear",
        ProductCategory.soft_toy,
        Currency.EUR,
    )
    teddy_bear.change_price(10)

    new_order = Order()
    new_order.add_product(teddy_bear)
    new_order.add_product(teddy_bear)
    new_order.calculate_total_price()

    print(new_order.total_price)

if __name__ == "__main__":
    main()
