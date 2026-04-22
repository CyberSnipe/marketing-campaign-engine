import json
from src.config import MERCH_CATALOG, RESTOCK_OUTPUT, DEFAULT_DEMAND_INCREASE


# ---------------------------------------------------------
# Domain Model
# ---------------------------------------------------------
class MerchItem:
    """Represents a single merchandise item in the catalog."""

    def __init__(self, merch_id: str, name: str, unit_cost: float, current_stock: int, base_demand: int):
        self.merch_id = merch_id
        self.name = name
        self.unit_cost = unit_cost
        self.current_stock = current_stock
        self.base_demand = base_demand

    def __repr__(self) -> str:
        return (
            f"<MerchItem {self.merch_id}: {self.name}, "
            f"stock={self.current_stock}, base_demand={self.base_demand}>"
        )


# ---------------------------------------------------------
# Persistence Layer
# ---------------------------------------------------------
class MerchRepository:
    """Loads merch data from JSON."""

    @staticmethod
    def load_merch_item(merch_id: str) -> MerchItem | None:
        """Return a MerchItem for the given ID, or None if not found."""
        if not MERCH_CATALOG.exists():
            raise FileNotFoundError(f"Merch catalog file not found: {MERCH_CATALOG}")

        try:
            with MERCH_CATALOG.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid JSON in merch catalog: {exc}") from exc

        for item in data:
            if item["merch_id"] == merch_id:
                return MerchItem(
                    merch_id=item["merch_id"],
                    name=item["name"],
                    unit_cost=float(item["unit_cost"]),
                    current_stock=int(item["current_stock"]),
                    base_demand=int(item["base_demand"]),
                )

        return None


class RestockRepository:
    """Saves restock recommendations to JSON."""

    @staticmethod
    def save_recommendation(result_dict: dict) -> None:
        """Append a single recommendation dict to the JSON output file."""
        RESTOCK_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

        if RESTOCK_OUTPUT.exists():
            try:
                with RESTOCK_OUTPUT.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if not isinstance(data, list):
                    data = []
            except json.JSONDecodeError:
                data = []
        else:
            data = []

        data.append(result_dict)

        with RESTOCK_OUTPUT.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)


# ---------------------------------------------------------
# Service Layer
# ---------------------------------------------------------
class MarketingService:
    """Business logic for calculating restock needs."""

    @staticmethod
    def calculate_restock(merch_item: MerchItem, demand_increase: float) -> dict:
        """
        Calculate restock quantity and total cost for a merch item.

        projected_demand = base_demand * (1 + demand_increase)
        restock_qty = max(0, projected_demand - current_stock)
        """
        projected_demand = merch_item.base_demand * (1 + demand_increase)
        restock_qty = max(0, int(projected_demand - merch_item.current_stock))
        total_cost = restock_qty * merch_item.unit_cost

        return {
            "merch_id": merch_item.merch_id,
            "name": merch_item.name,
            "restock_qty": restock_qty,
            "total_cost": round(total_cost, 2),
            "demand_increase": demand_increase,
        }


# ---------------------------------------------------------
# Process Function
# ---------------------------------------------------------
def trigger_marketing_campaign() -> None:
    """CLI flow: prompt user, run marketing logic, save and display results."""
    print("\n=== Trigger Marketing Campaign ===")

    merch_id = input("Enter merch ID: ").strip()
    if not merch_id:
        print("Merch ID is required.\n")
        return

    demand_input = input(f"Expected demand increase (default {DEFAULT_DEMAND_INCREASE}): ").strip()

    if demand_input == "":
        demand_increase = DEFAULT_DEMAND_INCREASE
    else:
        try:
            demand_increase = float(demand_input)
        except ValueError:
            print("Invalid demand increase. Using default.")
            demand_increase = DEFAULT_DEMAND_INCREASE

    try:
        merch_item = MerchRepository.load_merch_item(merch_id)
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"Error loading merch catalog: {exc}")
        return

    if merch_item is None:
        print("Merch item not found.\n")
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
def main() -> None:
    """Main CLI loop for the Marketing Campaign Engine."""
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