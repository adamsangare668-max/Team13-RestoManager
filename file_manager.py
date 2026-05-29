"""
file_manager.py - Handles reading and writing data to files for RestoManagerG13.
Author: Pulchérie
"""

# Imports
import json           # used to read and write structured text data
import os             # used to check if files/folders exist
from datetime import datetime   # used to timestamp log entries


# Constants
DATA_DIR: str = "data"                               # folder that holds all data files
RESERVATIONS_FILE: str = "data/reservations.txt"   # stores all reservation records
ORDERS_FILE: str = "data/orders.txt"               # stores all order records
LOG_FILE: str = "data/activity_log.txt"             # plain-text log of all activity


# Class 

class FileManager:
    """
    Manages all file input and output for RestoManagerG13.
    Saves and loads reservations and orders using text files.
    Writes a plain-text activity log.
    Demonstrates abstraction: the rest of the application does not need to know
    how or where the data is stored — it just calls these methods.
    """

    @staticmethod
    def ensure_data_directory() -> None:
        """Create the data/ directory if it does not already exist."""
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)   # create the folder

    @staticmethod
    def __read_data_file(filepath: str) -> list:
        """
        Read a structured text file and return its contents as a list.
        Returns an empty list if the file does not exist or is corrupted.
        This is a private method: only FileManager uses it internally.
        """
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # File is missing or unreadable – return empty list safely
            return []

    @staticmethod
    def __write_data_file(filepath: str, data: list) -> None:
        """
        Write a list of dictionaries to a structured text file with nice indentation.
        Private method: called internally by save_reservation and save_order.
        """
        FileManager.ensure_data_directory()  # make sure the folder exists
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    # Reservation file methods

    @staticmethod
    def save_reservation(reservation_dict: dict) -> None:
        """
        Add a new reservation to the reservations file.
        Loads existing records, appends the new one, then saves everything.
        """
        existing: list = FileManager.__read_data_file(RESERVATIONS_FILE)
        existing.append(reservation_dict)   # add the new reservation
        FileManager.__write_data_file(RESERVATIONS_FILE, existing)

    @staticmethod
    def load_reservations() -> list:
        """
        Load and return all saved reservations as a list of dictionaries.
        Returns an empty list if no reservations have been saved yet.
        """
        return FileManager.__read_data_file(RESERVATIONS_FILE)
