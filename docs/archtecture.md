# System Architecture

```text
marketing-engine/
│
├── pyproject.toml
├── settings.cfg
├── README.md
│
├── src/
│   └── marketing_engine/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       │
│       ├── api/
│       │     └── marketing_api.py
│       │
│       ├── domain/
│       │     └── merch_item.py
│       │
│       ├── services/
│       │     ├── marketing_service.py
│       │     ├── forecasting_service.py
│       │     ├── analytics_service.py
│       │     ├── safety_stock_service.py
│       │     └── batch_service.py
│       │
│       ├── gui/
│       │     ├── app.py
│       │     ├── campaign_view.py
│       │     ├── analytics_view.py
│       │     ├── history_view.py
│       │     └── widgets.py
│       │
│       ├── persistence/
│       │     ├── merch_repository.py
│       │     └── restock_repository.py
│       │
│       ├── routing/
│       │     └── process_router.py
│       │
│       └── tests/
│             ├── test_forecasting.py
│             ├── test_analytics.py
│             ├── test_restock_logic.py
│             └── test_repositories.py
│
└── data/
      ├── merch_catalog.json
      └── restock_recommendations.json
```
