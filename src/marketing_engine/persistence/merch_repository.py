import json
from pathlib import Path
from marketing_engine.domain.merch_item import MerchItem
from ..config import MERCH_CATALOG


class MerchRepository:
    """
    Loads merchandise items from JSON.
    """

    @staticmethod
    def load_all_items():
        if not MERCH_CATALOG.exists():
            raise FileNotFoundError(f"Catalog not found: {MERCH_CATALOG}")

        with MERCH_CATALOG.open("r", encoding="utf-8") as f:
            data = json.load(f)

        items = []
        
        for item in data:
            items.append(
                MerchItem(
                    merch_id=item["merch_id"],
                    name=item["name"],
                    unit_cost=item["unit_cost"],
                    current_stock=item["current_stock"],
                    base_demand=item["base_demand"],
                    demand_history=item["demand_history"]
                )
            )
        return items

    @staticmethod
    def load_item(merch_id):
        for item in MerchRepository.load_all_items():
            if item.merch_id == merch_id:
                return item
        return None