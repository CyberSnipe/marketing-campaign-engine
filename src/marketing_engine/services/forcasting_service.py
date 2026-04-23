class ForecastingService:
    """
    Provides forecasting models and error metrics for demand prediction.
    """

    @staticmethod
    def moving_average(history, window):
        if len(history) < window:
            return sum(history) / len(history)
        return sum(history[-window:]) / window

    @staticmethod
    def weighted_moving_average(history, weights):
        w_len = len(weights)
        if len(history) < w_len:
            history = history[-w_len:]
        return sum(h * w for h, w in zip(history[-w_len:], weights)) / sum(weights)

    @staticmethod
    def exponential_smoothing(history, alpha):
        forecast = history[0]
        for value in history[1:]:
            forecast = alpha * value + (1 - alpha) * forecast
        return forecast

    # -----------------------------
    # Error Metrics
    # -----------------------------
    @staticmethod
    def mad(actual, forecast_list):
        return sum(abs(a - f) for a, f in zip(actual, forecast_list)) / len(actual)

    @staticmethod
    def mse(actual, forecast_list):
        return sum((a - f) ** 2 for a, f in zip(actual, forecast_list)) / len(actual)

    @staticmethod
    def mape(actual, forecast_list):
        return sum(abs((a - f) / a) for a, f in zip(actual, forecast_list)) / len(actual)

    # -----------------------------
    # Forecast Comparison Utility
    # -----------------------------
    @staticmethod
    def compare_models(history, ma_window, wma_weights, es_alpha):
        """
        Returns a dict comparing MA, WMA, and ES forecasts + error metrics.
        """
        ma = ForecastingService.moving_average(history, ma_window)
        wma = ForecastingService.weighted_moving_average(history, wma_weights)
        es = ForecastingService.exponential_smoothing(history, es_alpha)

        # Build forecast lists for error metrics
        # (simple approach: repeat forecast for each actual point)
        ma_list = [ma] * len(history)
        wma_list = [wma] * len(history)
        es_list = [es] * len(history)

        return {
            "MA": {
                "forecast": ma,
                "MAD": ForecastingService.mad(history, ma_list),
                "MSE": ForecastingService.mse(history, ma_list),
                "MAPE": ForecastingService.mape(history, ma_list),
            },
            "WMA": {
                "forecast": wma,
                "MAD": ForecastingService.mad(history, wma_list),
                "MSE": ForecastingService.mse(history, wma_list),
                "MAPE": ForecastingService.mape(history, wma_list),
            },
            "ES": {
                "forecast": es,
                "MAD": ForecastingService.mad(history, es_list),
                "MSE": ForecastingService.mse(history, es_list),
                "MAPE": ForecastingService.mape(history, es_list),
            },
        