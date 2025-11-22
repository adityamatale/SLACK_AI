import logging
import sys
from logging.handlers import RotatingFileHandler

# Create a logger
logger = logging.getLogger("api_logger")
logger.propagate = False  # Prevent messages from going to the root logger
logger.setLevel(logging.INFO)  # Change to DEBUG for more details

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# File handler with rotation
file_handler = RotatingFileHandler(
    "SLLACK/api/logs/api.log", maxBytes=5*1024*1024, backupCount=5
)
file_handler.setLevel(logging.INFO)

# Log format
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
