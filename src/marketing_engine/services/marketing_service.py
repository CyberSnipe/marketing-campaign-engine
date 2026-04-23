# services/marketing_service.py

from marketing_engine.services.safety_stock_service import SafetyStockService
from marketing_engine.domain.merch_item import MerchItem

class MarketingService:
    """
    Calculates restock quantity and cost.
    """

    @staticmethod
    def calculate_restock(merch_item, projected_demand):
        adjusted_demand = SafetyStockService.apply(projected_demand)

        restock_qty = max(0, int(adjusted_demand - merch_item.current_stock))
        total_cost = restock_qty * merch_item.unit_cost

        return {
            "merch_id": merch_item.merch_id,
            "name": merch_item.name,
            "projected_demand": projected_demand,
            "adjusted_demand": adjusted_demand,
            "restock_qty": restock_qty,
            "total_cost": round(total_cost, 2),
        }