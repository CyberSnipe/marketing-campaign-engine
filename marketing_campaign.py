import configparser

config = configparser.ConfigParser()
config.read("settings.cfg")

DATA_DIR = config["paths"]["data_dir"]
MERCH_CATALOG = config["paths"]["merch_catalog"]
RESTOCK_OUTPUT = config["paths"]["restock_output"]
DEBUG = config.getboolean("logging", "debug")
DEFAULT_DEMAND_INCREASE = float(config["process"]["default_demand_increase"])

