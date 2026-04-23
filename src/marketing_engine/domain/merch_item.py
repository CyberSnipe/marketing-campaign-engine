class MerchItem:
    """
    Represents a merchandise item with forecasting history.
    """

    def __init__(self, merch_id, name, unit_cost, current_stock, base_demand, demand_history):
        self.merch_id = merch_id
        self.name = name
        self.unit_cost = float(unit_cost)
        self.current_stock = int(current_stock)
        self.base_demand = int(base_demand)
        self.demand_history = demand_history or []

    def __repr__(self):
        return (
            f"<MerchItem {self.merch_id}: {self.name}, "
            f"stock={self.current_stock}, base_demand={self.base_demand}, "
            f"history={len(self.demand_history)} pts>"
        )
        
        
        