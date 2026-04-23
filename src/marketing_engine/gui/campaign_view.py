# gui/campaign_view.py

import tkinter as tk
from tkinter import ttk, messagebox

from marketing_engine.routing.process_router import ProcessRouter
from marketing_engine.persistence.merch_repository import MerchRepository


class CampaignView(ttk.Frame):
    """
    UI for running a single marketing campaign.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Run Marketing Campaign", font=("Arial", 18)).pack(pady=20)

        # Dropdown for merch selection
        ttk.Label(self, text="Select Item:").pack()
        self.item_var = tk.StringVar()
        self.item_dropdown = ttk.Combobox(self, textvariable=self.item_var)
        self.item_dropdown.pack(pady=5)

        # Load items
        items = MerchRepository.load_all_items()
        self.item_dropdown["values"] = [item.merch_id for item in items]

        # Demand increase
        ttk.Label(self, text="Demand Increase (0.20 = 20%)").pack()
        self.demand_var = tk.StringVar(value="0.20")
        ttk.Entry(self, textvariable=self.demand_var).pack(pady=5)

        # Run button
        ttk.Button(self, text="Run Campaign", command=self.run_campaign).pack(pady=15)

        # Output box
        self.output = tk.Text(self, height=12, width=80)
        self.output.pack(pady=10)

    # ---------------------------------------------------------
    def run_campaign(self):
        merch_id = self.item_var.get()
        if not merch_id:
            messagebox.showerror("Error", "Please select a merchandise item.")
            return

        try:
            demand_increase = float(self.demand_var.get())
        except ValueError:
            messagebox.showerror("Error", "Demand increase must be a number.")
            return

        try:
            result = ProcessRouter.run_single_campaign(merch_id, demand_increase)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"Best Model: {result['best_model']}\n")
        self.output.insert(tk.END, f"Projected Demand: {result['projected_demand']:.2f}\n\n")

        restock = result["restock"]
        for key, value in restock.items():
            self.output.insert(tk.END, f"{key}: {value}\n")