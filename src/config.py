import configparser
from pathlib import Path

# ====================== Load Configuration ======================
config = configparser.ConfigParser()
config.read("settings.cfg")

# ====================== BASE_DIR ======================
BASE_DIR = Path(__file__).parent.resolve()

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

