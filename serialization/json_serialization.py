import json
from pathlib import Path
from models.ecom_models import Customer


class JsonDataSerialization:

    ecom_data_path = Path(__file__).parent / "data" / "ecom_data.json"

    @classmethod
    def load_data(cls) -> list[Customer]:
        with open(cls.ecom_data_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            return [Customer.from_dict(data_item) for data_item in data]

    @classmethod
    def save_data(cls) -> list[Customer]:
        with open(cls.ecom_data_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            return [Customer.from_dict(data_item) for data_item in data]
