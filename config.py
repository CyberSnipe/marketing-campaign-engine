import configparser                             # import configparser used to parse together the system constants from settings.cfg file information      
from pathlib import Path                        # from built in library pathlib import to join config.py back to setting.cfg

# Load settings.cfg
config = configparser.ConfigParser()            # assign config to the Class ConfigParser() in configparser built in library
config.read("settings.cfg")                     # config read source settings information

# Project paths
DATA_DIR = Path(config["paths"]["data_dir"])                # create univeral constant for DATA_DIR with path via config.py back to settings.cfg
MERCH_CATALOG = Path(config["paths"]["merch_catalog"])      # create univeral constant for MERCH_CATALOG with path via config.py back to settings.cfg
RESTOCK_OUTPUT = Path(config["paths"]["restock_output"])    # create univeral constant for RESTOCK_OUTPUT with path via config.py back to settings.cfg

# Logging
DEBUG = config.getboolean("logging", "debug")              # create univeral constant for DEBUG with path via config.py back to settings.cfg with bool set to true

# Process defaults
DEFAULT_DEMAND_INCREASE = float(config["process"]["default_demand_increase"])   # create univeral constant for DEFAULT_DEMAND_INCREASE with path via config.py back to settings.cfg


