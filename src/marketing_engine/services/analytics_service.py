# services/analytics_service.py

from marketing_engine.services.forcasting_service import ForecastingService
from marketing_engine.domain.merch_item import MerchItem
from marketing_engine.config import MA_WINDOW, WMA_WEIGHTS, ES_ALPHA


class AnalyticsService:
    """
    Produces analytics summaries including forecasting model comparison.
    """

    @staticmethod
    def summarize(merch_item):
        history = merch_item.demand_history

        comparison = ForecastingService.compare_models(
            history,
            ma_window=MA_WINDOW,
            wma_weights=WMA_WEIGHTS,
            es_alpha=ES_ALPHA,
        )

        # Determine best model by MAPE
        best_model = min(comparison, key=lambda m: comparison[m]["MAPE"])

        return {
            "item": merch_item.name,
            "history_points": len(history),
            "forecast_comparison": comparison,
            "best_model": best_model,
            "best_forecast": comparison[best_model]["forecast"],
        }