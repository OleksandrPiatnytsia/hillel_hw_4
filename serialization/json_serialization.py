import json
from pathlib import Path
from models.ecom_models import Customer, Product


class JsonDataSerialization:

    ecom_data_path = Path(__file__).parent.parent / "data" / "ecom_data.json"

    @classmethod
    def load_data(cls) -> tuple[list[Customer], list[Product]]:

        if not cls.ecom_data_path.exists():
            return [], []

        try:
            with open(cls.ecom_data_path, "r", encoding="utf-8") as fd:
                content = fd.read().strip()

                if not content:
                    return [], []

                data = json.loads(content)

        except json.JSONDecodeError:
            return [], []

        customers = [Customer.from_dict(data_item) for data_item in data]
        products: set[Product] = set()

        for current_customer in customers:
            for current_order in current_customer.orders:
                products.update(current_order.products)

        return customers, list(products)

    @classmethod
    def save_data(cls, customers: list[Customer]) -> None:

        cls.ecom_data_path.parent.mkdir(parents=True, exist_ok=True)

        print(cls.ecom_data_path)

        with open(cls.ecom_data_path, "w", encoding="utf-8") as fd:

            json.dump(
                [customer_.to_dict() for customer_ in customers],
                fd,
                ensure_ascii=False,
                indent=4,
            )
