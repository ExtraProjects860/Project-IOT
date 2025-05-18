import logging
import os
import sys
from datetime import datetime, UTC
from logging.handlers import RotatingFileHandler
from app import config


log_dir = "logs/files_logs"
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"app_{datetime.now(UTC).year}-{datetime.now(UTC).month}-{datetime.now(UTC).day}.log")

log_level = logging.DEBUG if config.settings.debug_logs else logging.INFO

log_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

file_handler = RotatingFileHandler(
    log_file, maxBytes=5*1024*1024, backupCount=5
)
file_handler.setLevel(log_level)
file_handler.setFormatter(log_formatter)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(log_level)
stream_handler.setFormatter(log_formatter)

logging.basicConfig(
    level=log_level,
    handlers=[file_handler, stream_handler],
)

logger = logging.getLogger(__name__)
