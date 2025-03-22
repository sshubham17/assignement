import logging
import os
from logging.handlers import RotatingFileHandler

# Ensure the logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log file paths
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")
INFO_LOG_FILE = os.path.join(LOG_DIR, "info.log")
API_LOG_FILE = os.path.join(LOG_DIR, "api.log")

# Log file max size (30 MB) and backup count (7 files)
MAX_LOG_SIZE = 30 * 1024 * 1024  # 30 MB
BACKUP_COUNT = 7  # Keep last 7 rotated logs

# Create formatters
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# ---- Main Logger (Handles Errors, Info, and Warning) ----
logger = logging.getLogger("fastapi_main")
logger.setLevel(logging.DEBUG)

# Error Log Handler
error_handler = RotatingFileHandler(ERROR_LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(log_formatter)

# Info & Warning Log Handler
info_handler = RotatingFileHandler(INFO_LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
info_handler.setLevel(logging.INFO)  # This will include both INFO and WARNING
info_handler.setFormatter(log_formatter)

# Attach Handlers to Main Logger
logger.addHandler(error_handler)
logger.addHandler(info_handler)

# ---- API Logger (Handles API Logs Separately) ----
api_logger = logging.getLogger("fastapi_api")
api_logger.setLevel(logging.INFO)  # Logs only API calls

# API Log Handler
api_handler = RotatingFileHandler(API_LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
api_handler.setLevel(logging.INFO)
api_handler.setFormatter(log_formatter)

# Attach API Handler
api_logger.addHandler(api_handler)

# Prevent log duplication
logger.propagate = False
api_logger.propagate = False