# gui/app.py

import tkinter as tk
from tkinter import ttk

from marketing_engine.gui.campaign_view import CampaignView
from marketing_engine.gui.analytics_view import AnalyticsView
from marketing_engine.gui.history_view import HistoryView


class MarketingEngineApp(tk.Tk):
    """
    Main Tkinter application window.
    Manages navigation between views.
    """

    def __init__(self):
        super().__init__()

        self.title("Marketing Engine – Campaign & Forecasting Suite")
        self.geometry("900x600")

        # Main container frame
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Dictionary of views
        self.frames = {}

        # Initialize views
        for ViewClass in (CampaignView, AnalyticsView, HistoryView):
            frame = ViewClass(parent=self.container, controller=self)
            self.frames[ViewClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Build menu bar
        self._build_menu()

        # Show default view
        self.show_frame("CampaignView")

    # ---------------------------------------------------------
    # MENU BAR
    # ---------------------------------------------------------
    def _build_menu(self):
        menubar = tk.Menu(self)

        # Campaign menu
        campaign_menu = tk.Menu(menubar, tearoff=0)
        campaign_menu.add_command(
            label="Run Campaign", command=lambda: self.show_frame("CampaignView")
        )
        campaign_menu.add_command(
            label="Batch Mode", command=lambda: self.show_frame("HistoryView")
        )
        menubar.add_cascade(label="Campaign", menu=campaign_menu)

        # Analytics menu
        analytics_menu = tk.Menu(menubar, tearoff=0)
        analytics_menu.add_command(
            label="Analytics Summary", command=lambda: self.show_frame("AnalyticsView")
        )
        menubar.add_cascade(label="Analytics", menu=analytics_menu)

        # History menu
        history_menu = tk.Menu(menubar, tearoff=0)
        history_menu.add_command(
            label="Past Recommendations", command=lambda: self.show_frame("HistoryView")
        )
        menubar.add_cascade(label="History", menu=history_menu)

        self.config(menu=menubar)

    # ---------------------------------------------------------
    # VIEW SWITCHING
    # ---------------------------------------------------------
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()