import json
from marketing_engine.config import RESTOCK_OUTPUT
class RestockRepository:
    """
    Saves restock recommendations to JSON.
    """

    @staticmethod
    def save(result_dict):
        if RESTOCK_OUTPUT.exists():
            try:
                with RESTOCK_OUTPUT.open("r", encoding="utf-8") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = []
        else:
            data = []

        data.append(result_dict)

        with RESTOCK_OUTPUT.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)