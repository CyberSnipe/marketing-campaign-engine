import json
import configparser
from pathlib import Path


# ---------------------------------------------------------
# Load Settings
# ---------------------------------------------------------
config = configparser.ConfigParser()
config.read("settings.cfg")

DATA_DIR = Path(config["paths"]["data_dir"])
MERCH_CATALOG = Path(config["paths"]["merch_catalog"])
RESTOCK_OUTPUT = Path(config["paths"]["restock_output"])
DEFAULT_DEMAND_INCREASE = float(config["process"]["default_demand_increase"])
DEBUG = config.getboolean("logging", "debug")


# ---------------------------------------------------------
# Domain Model
# ---------------------------------------------------------
class MerchItem:
    def __init__(self, merch_id, name, unit_cost, current_stock):
        self.merch_id = merch_id
        self.name = name
        self.unit_cost = unit_cost
        self.current_stock = current_stock

    def __repr__(self):
        return f"<MerchItem {self.merch_id}: {self.name}, stock={self.current_stock}>"


# ---------------------------------------------------------
# Persistence Layer
# ---------------------------------------------------------
class MerchRepository:
    """Loads merch data from JSON."""

    @staticmethod
    def load_merch_item(merch_id):
        if not MERCH_CATALOG.exists():
            raise FileNotFoundError("Merch catalog file not found.")

        with open(MERCH_CATALOG, "r") as f:
            data = json.load(f)

        for item in data:
            if item["merch_id"] == merch_id:
                return MerchItem(
                    merch_id=item["merch_id"],
                    name=item["name"],
                    unit_cost=item["unit_cost"],
                    current_stock=item["current_stock"]
                )

        return None


class RestockRepository:
    """Saves restock recommendations to JSON."""

    @staticmethod
    def save_recommendation(result_dict):
        RESTOCK_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

        # Load existing or create new list
        if RESTOCK_OUTPUT.exists():
            with open(RESTOCK_OUTPUT, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(result_dict)

        with open(RESTOCK_OUTPUT, "w") as f:
            json.dump(data, f, indent=4)


# ---------------------------------------------------------
# Service Layer
# ---------------------------------------------------------
class MarketingService:
    """Business logic for calculating restock needs."""

    @staticmethod
    def calculate_restock(merch_item, demand_increase):
        projected_demand = merch_item.current_stock * (1 + demand_increase)
        restock_qty = max(0, int(projected_demand - merch_item.current_stock))
        total_cost = restock_qty * merch_item.unit_cost

        return {
            "merch_id": merch_item.merch_id,
            "name": merch_item.name,
            "restock_qty": restock_qty,
            "total_cost": round(total_cost, 2),
            "demand_increase": demand_increase
        }


# ---------------------------------------------------------
# Process Function
# ---------------------------------------------------------
def trigger_marketing_campaign():
    print("\n=== Trigger Marketing Campaign ===")

    merch_id = input("Enter merch ID: ").strip()
    demand_input = input(f"Expected demand increase (default {DEFAULT_DEMAND_INCREASE}): ").strip()

    if demand_input == "":
        demand_increase = DEFAULT_DEMAND_INCREASE
    else:
        try:
            demand_increase = float(demand_input)
        except ValueError:
            print("Invalid demand increase. Using default.")
            demand_increase = DEFAULT_DEMAND_INCREASE

    merch_item = MerchRepository.load_merch_item(merch_id)

    if merch_item is None:
        print("Merch item not found.")
        return

    result = MarketingService.calculate_restock(merch_item, demand_increase)
    RestockRepository.save_recommendation(result)

    print("\n--- Restock Recommendation ---")
    print(f"Item: {result['name']} ({result['merch_id']})")
    print(f"Recommended Quantity: {result['restock_qty']}")
    print(f"Total Cost: ${result['total_cost']}")
    print("------------------------------\n")


# ---------------------------------------------------------
# CLI Menu
# ---------------------------------------------------------
def main():
    while True:
        print("=== Marketing Campaign Engine ===")
        print("1. Trigger Marketing Campaign")
        print("2. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            trigger_marketing_campaign()
        elif choice == "2":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.\n")


# ---------------------------------------------------------
# Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":
    main()

