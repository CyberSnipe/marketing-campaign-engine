# services/safety_stock_service.py

from marketing_engine.config import SAFETY_STOCK_MODE, SAFETY_STOCK_VALUE

class SafetyStockService:
    """
    Applies safety stock rules to projected demand.
    """

    @staticmethod
    def apply(projected_demand):
        if SAFETY_STOCK_MODE == "fixed":
            return projected_demand + SAFETY_STOCK_VALUE

        if SAFETY_STOCK_MODE == "percent":
            return projected_demand * (1 + SAFETY_STOCK_VALUE)

        return projected_demand