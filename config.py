import configparser
from pathlib import Path

# Load settings.cfg
config = configparser.ConfigParser()
config.read("settings.cfg")

# Project paths
DATA_DIR = Path(config["paths"]["data_dir"])
MERCH_CATALOG = Path(config["paths"]["merch_catalog"])
RESTOCK_OUTPUT = Path(config["paths"]["restock_output"])

# Logging
DEBUG = config.getboolean("logging", "debug")

# Process defaults
DEFAULT_DEMAND_INCREASE = float(config["process"]["default_demand_increase"])


