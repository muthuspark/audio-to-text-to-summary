import logging
import os
from logging.handlers import RotatingFileHandler

# Set up logging
log_file = os.path.join(os.getcwd(), 'app.log')
file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024 * 10,
                                   backupCount=10)  # 10 MB log file, with backup count of 10
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
file_handler.setFormatter(file_formatter)

log_level = logging.INFO

# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(log_level)
logger.addHandler(file_handler)

# Add console handler for logging to stdout
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)
