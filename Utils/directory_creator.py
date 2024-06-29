import os

from Utils.logger import logger


def directory_creator(new_directory_path):
    if not os.path.exists(new_directory_path):
        os.makedirs(new_directory_path)
        logger.warning(f"Directory '{new_directory_path}' created.")
    else:
        logger.warning(f"Directory '{new_directory_path}' already exists.")

    return new_directory_path