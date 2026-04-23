# gui/history_view.py

import tkinter as tk
from tkinter import ttk
import json

from marketing_engine.config import RESTOCK_OUTPUT


class HistoryView(ttk.Frame):
    """
    Displays past restock recommendations.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Past Recommendations", font=("Arial", 18)).pack(pady=20)

        columns = ("merch_id", "restock_qty", "total_cost", "projected_demand")

        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(pady=10)

        ttk.Button(self, text="Refresh", command=self.load_history).pack(pady=10)

        self.load_history()

    # ---------------------------------------------------------
    def load_history(self):
        self.tree.delete(*self.tree.get_children())

        if not RESTOCK_OUTPUT.exists():
            return

        try:
            with RESTOCK_OUTPUT.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            return

        for entry in data:
            self.tree.insert(
                "", tk.END,
                values=(
                    entry.get("merch_id"),
                    entry.get("restock_qty"),
                    entry.get("total_cost"),
                    entry.get("projected_demand"),
                )
            )