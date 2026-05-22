import json
from pathlib import Path
from models.ecom_models import Customer, Product, ProductsCollection


class JsonDataSerialization:

    ecom_data_path = Path(__file__).parent.parent / "data" / "ecom_data.json"

    @classmethod
    def load_data(cls) -> tuple[ProductsCollection, list[Customer]]:

        products = ProductsCollection()

        response = products, []

        if not cls.ecom_data_path.exists():
            return response

        try:
            with open(cls.ecom_data_path, "r", encoding="utf-8") as fd:
                content = fd.read().strip()

                if not content:
                    return response

                data = json.loads(content)

        except json.JSONDecodeError:
            return response

        for product_item in data.get("products", []):
            products.add_product(Product.from_dict(product_item))

        customers = [
            Customer.from_dict(customer_item)
            for customer_item in data.get("customers", [])
        ]

        return products, customers

    @classmethod
    def save_data(cls, products: ProductsCollection, customers: list[Customer]) -> None:

        cls.ecom_data_path.parent.mkdir(parents=True, exist_ok=True)

        print(cls.ecom_data_path)

        with open(cls.ecom_data_path, "w", encoding="utf-8") as fd:

            json.dump(
                {
                    "products": [
                        product.to_dict() for product in products.data.values()
                    ],
                    "customers": [customer_.to_dict() for customer_ in customers],
                },
                fd,
                ensure_ascii=False,
                indent=4,
            )
