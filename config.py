import os
import socket
import importlib
from pathlib import Path

try:
    # from pycfhelpers.cellframenet import CellframeNetwork
    from pycfhelpers.cfnet_struct import CFNet
except ImportError:
    pass

from logger import logIt

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
hostname = socket.gethostname()

if load_dotenv(dotenv_path=str(BASE_DIR / ".env.local")):
    logIt.message(f"ENVIRONMENT VARIABLES loaded successfully from .env.local")
elif load_dotenv(dotenv_path=str(BASE_DIR / ".env.dev")):
    logIt.message(f"ENVIRONMENT VARIABLES loaded successfully from .env.dev")
else:
    logIt.error(f"ENVIRONMENT VARIABLES  not loaded")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT") or 5432
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")  # DB name

logIt.message(f"{DB_HOST=}")
logIt.message(f"{POSTGRES_DB=}")

module_name = f"hostsettings.{hostname}"
try:
    module = importlib.import_module(module_name)
    NETS: list[CFNet] = getattr(module, "NETS")
except ImportError:
    pass
