# Main Entry Point for the Marketing Engine
# main.py

"""
Entry point for the Marketing Engine application.
Launches the Tkinter GUI.
"""
from marketing_engine.gui.app import MarketingEngineApp

def main():
    app = MarketingEngineApp()
    app.mainloop()


if __name__ == "__main__":
    main()
    
    