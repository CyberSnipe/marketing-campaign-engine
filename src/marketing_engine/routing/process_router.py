# routing/process_router.py

from persistence.merch_repository import MerchRepository
from persistence.restock_repository import RestockRepository

from services.forcasting_service import ForecastingService
from services.marketing_service import MarketingService
from services.analytics_service import AnalyticsService
from services.batch_service import BatchService

from src.marketing_engine.config import (
    MA_WINDOW,
    WMA_WEIGHTS,
    ES_ALPHA,
    DEFAULT_DEMAND_INCREASE,
)


class ProcessRouter:
    """
    Orchestrates flows between repositories, services, and the GUI/CLI.
    This is the 'traffic controller' of the Marketing Engine.
    """

    # ---------------------------------------------------------
    # SINGLE ITEM CAMPAIGN
    # ---------------------------------------------------------
    @staticmethod
    def run_single_campaign(merch_id, demand_increase=None):
        """
        Runs a campaign for a single merchandise item.
        Returns a dict with restock results + forecast summary.
        """

        if demand_increase is None:
            demand_increase = DEFAULT_DEMAND_INCREASE

        # Load item
        item = MerchRepository.load_item(merch_id)
        if not item:
            raise ValueError(f"Item '{merch_id}' not found in catalog.")

        # Forecast demand using all models
        comparison = ForecastingService.compare_models(
            item.demand_history,
            MA_WINDOW,
            WMA_WEIGHTS,
            ES_ALPHA,
        )

        # Pick best model by MAPE
        best_model = min(comparison, key=lambda m: comparison[m]["MAPE"])
        base_forecast = comparison[best_model]["forecast"]

        # Apply demand increase
        projected_demand = base_forecast * (1 + demand_increase)

        # Calculate restock
        restock_result = MarketingService.calculate_restock(item, projected_demand)

        # Save result
        RestockRepository.save(restock_result)

        # Return combined result
        return {
            "restock": restock_result,
            "forecast_comparison": comparison,
            "best_model": best_model,
            "projected_demand": projected_demand,
        }

    # ---------------------------------------------------------
    # ANALYTICS SUMMARY
    # ---------------------------------------------------------
    @staticmethod
    def run_analytics(merch_id):
        """
        Returns analytics summary for a single item.
        """
        item = MerchRepository.load_item(merch_id)
        if not item:
            raise ValueError(f"Item '{merch_id}' not found in catalog.")

        return AnalyticsService.summarize(item)

    # ---------------------------------------------------------
    # BATCH CAMPAIGN
    # ---------------------------------------------------------
    @staticmethod
    def run_batch_campaign(demand_increase=None):
        """
        Runs a campaign for ALL items in the catalog.
        Returns a list of restock results.
        """

        if demand_increase is None:
            demand_increase = DEFAULT_DEMAND_INCREASE

        results = BatchService.run_batch(demand_increase)

        # Save each result
        for r in results:
            RestockRepository.save(r)

        return results