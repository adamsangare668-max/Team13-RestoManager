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

    # Order file methods

    @staticmethod
    def save_order(order_dict: dict) -> None:
        """
        Add a new order to the orders file.
        Loads existing records, appends the new one, then saves everything.
        """
        existing: list = FileManager.__read_data_file(ORDERS_FILE)
        existing.append(order_dict)     # add the new order
        FileManager.__write_data_file(ORDERS_FILE, existing)

    @staticmethod
    def load_orders() -> list:
        """
        Load and return all saved orders as a list of dictionaries.
        Returns an empty list if no orders have been saved yet.
        """
        return FileManager.__read_data_file(ORDERS_FILE)

    # Activity log

    @staticmethod
    def write_log(message: str) -> None:
        """
        Append a timestamped message to the plain-text activity log.
        This records every significant action (reservation, order, start, exit).
        """
        FileManager.ensure_data_directory()
        timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry: str = f"[{timestamp}]  {message}\n"

        # Open in append mode so previous entries are not overwritten
        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)

    # Summary

    @staticmethod
    def get_summary() -> dict:
        """
        Return a dictionary with the total count of saved reservations and orders.
        Used by the restaurant controller to show statistics.
        """
        reservations: list = FileManager.load_reservations()
        orders: list = FileManager.load_orders()

        return {
            "total_reservations": len(reservations),
            "total_orders": len(orders)
        }
