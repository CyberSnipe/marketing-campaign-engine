import configparser
from pathlib import Path

# ====================== BASE_DIR ======================
BASE_DIR = Path(__file__).parent.resolve()
CONFIG_PATH = BASE_DIR / "settings.cfg"

# ====================== Load Configuration ======================
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

# ====================== Project Info ======================
PROJECT_NAME = config.get("project", "name")
VERSION = config.get("project", "version")
ENVIRONMENT = config.get("project", "environment")

# ====================== Paths ======================
DATA_DIR = BASE_DIR / config.get("paths", "data_dir")

MERCH_CATALOG = BASE_DIR / config.get("paths", "merch_catalog")
RESTOCK_OUTPUT = BASE_DIR / config.get("paths", "restock_output")

# ====================== Logging ======================
DEBUG = config.getboolean("logging", "debug")
LOG_LEVEL = config.get("logging", "log_level", fallback="INFO")

# ====================== Process Settings ======================
DEFAULT_DEMAND_INCREASE = config.getfloat("process", "default_demand_increase")
SAFETY_STOCK_MODE = config.get("process", "safety_stock_mode")
SAFETY_STOCK_VALUE = config.getint("process", "safety_stock_value")

# ====================== Forecasting Settings ======================
MA_WINDOW = config.getint("forecasting", "ma_window")
WMA_WEIGHTS = [float(w) for w in config.get("forecasting", "wma_weights").split(",")]
ES_ALPHA = config.getfloat("forecasting", "es_alpha")

# ====================== Ensure Directories Exist ======================
def ensure_dirs_exist():
    """Create necessary directories if they don't exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

ensure_dirs_exist()

# ====================== Debug Output ======================
if __name__ == "__main__" or DEBUG:
    print(f"✅ Configuration loaded for: {PROJECT_NAME} v{VERSION} ({ENVIRONMENT})")
    print(f"   DATA_DIR:         {DATA_DIR}")
    print(f"   MERCH_CATALOG:    {MERCH_CATALOG}")
    print(f"   RESTOCK_OUTPUT:   {RESTOCK_OUTPUT}")
    print(f"   DEBUG:            {DEBUG}")
    print(f"   DEFAULT_DEMAND_INCREASE: {DEFAULT_DEMAND_INCREASE}")
    print(f"   SAFETY_STOCK_MODE: {SAFETY_STOCK_MODE}")
    print(f"   SAFETY_STOCK_VALUE: {SAFETY_STOCK_VALUE}")
    print(f"   MA_WINDOW: {MA_WINDOW}")
    print(f"   WMA_WEIGHTS: {WMA_WEIGHTS}")
    print(f"   ES_ALPHA: {ES_ALPHA}")

