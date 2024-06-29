# Specify the CSV file path
import csv

from Utils.logger import logger


def csv_saver(data, file):

    """Extract field names from the dictionary (assuming all dictionaries have the same keys)"""
    fields = list(data[0].keys())

    # Write dictionary to CSV file
    with open(file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)

        # Write header
        writer.writeheader()

        # Write data
        for row in data:
            writer.writerow(row)

    logger.info(f"CSV file '{file}' has been created successfully.")