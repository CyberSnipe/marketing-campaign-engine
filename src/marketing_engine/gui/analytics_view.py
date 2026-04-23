# gui/analytics_view.py

import tkinter as tk
from tkinter import ttk, messagebox

from marketing_engine.routing.process_router import ProcessRouter
from marketing_engine.persistence.merch_repository import MerchRepository


class AnalyticsView(ttk.Frame):
    """
    UI for viewing forecasting analytics for a single item.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Analytics Summary", font=("Arial", 18)).pack(pady=20)

        # Dropdown
        ttk.Label(self, text="Select Item:").pack()
        self.item_var = tk.StringVar()
        self.item_dropdown = ttk.Combobox(self, textvariable=self.item_var)
        self.item_dropdown.pack(pady=5)

        items = MerchRepository.load_all_items()
        self.item_dropdown["values"] = [item.merch_id for item in items]

        ttk.Button(self, text="Show Analytics", command=self.show_analytics).pack(pady=10)

        self.output = tk.Text(self, height=20, width=90)
        self.output.pack(pady=10)

    # ---------------------------------------------------------
    def show_analytics(self):
        merch_id = self.item_var.get()
        if not merch_id:
            messagebox.showerror("Error", "Please select an item.")
            return

        try:
            summary = ProcessRouter.run_analytics(merch_id)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.output.delete("1.0", tk.END)

        self.output.insert(tk.END, f"Item: {summary['item']}\n")
        self.output.insert(tk.END, f"History Points: {summary['history_points']}\n")
        self.output.insert(tk.END, f"Best Model: {summary['best_model']}\n")
        self.output.insert(tk.END, f"Best Forecast: {summary['best_forecast']:.2f}\n\n")

        self.output.insert(tk.END, "Forecast Comparison:\n")
        for model, stats in summary["forecast_comparison"].items():
            self.output.insert(tk.END, f"\n{model}:\n")
            for k, v in stats.items():
                self.output.insert(tk.END, f"  {k}: {v:.4f}\n")