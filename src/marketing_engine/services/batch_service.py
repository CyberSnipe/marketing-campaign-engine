# services/batch_service.py

from marketing_engine.persistence.merch_repository import MerchRepository
from marketing_engine.services.forcasting_service import ForecastingService
from marketing_engine.services.marketing_service import MarketingService
from marketing_engine.config import MA_WINDOW, WMA_WEIGHTS, ES_ALPHA


class BatchService:
    """
    Runs campaigns for all merch items.
    """

    @staticmethod
    def run_batch(demand_increase):
        items = MerchRepository.load_all_items()
        results = []

        for item in items:
            # Forecast demand
            comparison = ForecastingService.compare_models(
                item.demand_history,
                MA_WINDOW,
                WMA_WEIGHTS,
                ES_ALPHA,
            )
            best_model = min(comparison, key=lambda m: comparison[m]["MAPE"])
            projected = comparison[best_model]["forecast"] * (1 + demand_increase)

            # Calculate restock
            restock = MarketingService.calculate_restock(item, projected)
            results.append(restock)

        return results