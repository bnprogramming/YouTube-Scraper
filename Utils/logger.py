import logging
import os

from Utils.get_time import get_time

# Create a custom logger
logger = logging.getLogger('custom_logger')

# Set the logging level
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

log_path = 'logs/'

if not os.path.exists(log_path):
    os.makedirs(log_path)
    logger.info(f"Directory '{log_path}' created.")
else:
    logger.info(f"Directory '{log_path}' already exists.")

now_time = get_time()
file_handler = logging.FileHandler(log_path +f'{now_time}.log','a')
file_handler.setLevel(logging.WARNING)

# Create formatters and add them to the handlers
console_formatter = logging.Formatter('%(asctime)s: %(message)s')
console_handler.setFormatter(console_formatter)

file_formatter = logging.Formatter('%(asctime)s: %(message)s')
file_handler.setFormatter(file_formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
