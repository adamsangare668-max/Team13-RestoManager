"""
reservation.py - Defines Table, Reservation, and Order classes for RestoManagerG13.
Author: Savadogo Oumou
"""

# Imports
import uuid                      # generates unique IDs for reservations and orders
from datetime import datetime    # used to timestamp reservations and orders


# Classes

class Table:
    """
    Represents a physical table in the restaurant.
    Tracks the table number, seating capacity, and reservation status.
    Uses encapsulation: reservation state is controlled by reserve() and free().
    """

    def __init__(self, table_number: int, capacity: int) -> None:
        """Initialize a table with a number, capacity, and available status."""
        self.__table_number: int = table_number
        self.__capacity: int = capacity
        self.__is_reserved: bool = False   # False = available by default
        self.__reserved_by: str = ""       # name of the customer who reserved it

    # Properties

    @property
    def table_number(self) -> int:
        """Return the table number."""
        return self.__table_number

    @property
    def capacity(self) -> int:
        """Return the maximum number of people this table can accommodate."""
        return self.__capacity

    @property
    def is_reserved(self) -> bool:
        """Return True if this table is currently reserved."""
        return self.__is_reserved

    @property
    def reserved_by(self) -> str:
        """Return the name of the customer who reserved this table."""
        return self.__reserved_by

    # Methods

    def reserve(self, customer_name: str) -> bool:
        """
        Mark this table as reserved for a given customer.
        Returns True if the reservation succeeded, False if already taken.
        """
        if self.__is_reserved:
            return False  # table already reserved – cannot double-book
        self.__is_reserved = True
        self.__reserved_by = customer_name
        return True

    def free(self) -> None:
        """Release this table so it becomes available again."""
        self.__is_reserved = False
        self.__reserved_by = ""

    def __str__(self) -> str:
        """Return a readable description of the table and its status."""
        if self.__is_reserved:
            status: str = f"Reserved by {self.__reserved_by}"
        else:
            status = "Available"
        return f"Table {self.__table_number:02d} | {status}"


class Reservation:
    """
    Represents a table reservation made by a customer.
    Stores who reserved, which table, when, and for how many guests.
    """

    def __init__(
        self,
        customer,
        table: Table,
        date: str,
        time: str,
        guests: int,
        duration: int = 2
    ) -> None:
        """Initialize a reservation with all required booking information."""
        # Generate a short unique ID for this reservation (e.g. 'A3F9B2C1')
        self.__reservation_id: str = str(uuid.uuid4())[:8].upper()
        self.__customer = customer        # Customer object (from person.py)
        self.__table: Table = table
        self.__date: str = date           # e.g. '2026-06-01'
        self.__time: str = time           # e.g. '12:30'
        self.__guests: int = guests
        self.__duration: int = duration   # duration in hours (default 2 hours)
        self.__created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Properties

    @property
    def reservation_id(self) -> str:
        """Return the unique reservation ID."""
        return self.__reservation_id

    @property
    def customer(self):
        """Return the Customer object associated with this reservation."""
        return self.__customer

    @property
    def table(self) -> Table:
        """Return the Table object associated with this reservation."""
        return self.__table

    @property
    def date(self) -> str:
        """Return the reservation date."""
        return self.__date

    @property
    def time(self) -> str:
        """Return the reservation time."""
        return self.__time

    @property
    def guests(self) -> int:
        """Return the number of guests for this reservation."""
        return self.__guests

    @property
    def duration(self) -> int:
        """Return the duration of this reservation in hours."""
        return self.__duration

    @property
    def end_time(self) -> str:
        """Calculate and return the end time of this reservation."""
        # Parse the start time
        time_parts = self.__time.split(":")
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        
        # Add duration hours
        end_hour = (hour + self.__duration) % 24
        return f"{end_hour:02d}:{minute:02d}"

    @property
    def formatted_date(self) -> str:
        """Return the reservation date in a more readable English format."""
        date_obj = datetime.strptime(self.__date, "%Y-%m-%d").date()
        return date_obj.strftime("%A %d/%m/%Y")

    # Methods

    def to_dict(self) -> dict:
        """
        Convert this reservation to a plain dictionary.
        Used by FileManager to save reservation data to a text file.
        """
        return {
            "reservation_id": self.__reservation_id,
            "customer_name": self.__customer.full_name,
            "customer_phone": self.__customer.phone_number,
            "table_number": self.__table.table_number,
            "date": self.__date,
            "time": self.__time,
            "end_time": self.end_time,
            "guests": self.__guests,
            "duration": self.__duration,
            "created_at": self.__created_at
        }

    def display_receipt(self) -> None:
        """Print a formatted reservation confirmation receipt."""
        line: str = "─" * 47
        print(f"\n  {'═' * 47}")
        print(f"  ║{'  ✅  RESERVATION CONFIRMED':^45}║")
        print(f"  {'═' * 47}")
        print(f"  {line}")
        print(f"  Reservation ID : #{self.__reservation_id}")
        print(f"  Customer       : {self.__customer.full_name}")
        print(f"  Phone          : {self.__customer.phone_number}")
        print(f"  Table          : N°{self.__table.table_number:02d}")
        print(f"  Date           : {self.formatted_date}")
        print(f"  Time slot      : {self.__time} — {self.end_time}")
        print(f"  Duration       : {self.__duration} hour(s)")
        print(f"  Guests         : {self.__guests}")
        print(f"  Confirmed at   : {self.__created_at}")
        print(f"  {line}")
        print("  🎉  Your table is waiting for you. See you soon!")
        print(f"  {'═' * 47}\n")

    def __str__(self) -> str:
        """Return a one-line summary of this reservation."""
        return (
            f"Reservation #{self.__reservation_id} | "
            f"{self.__customer.full_name} | "
            f"Table {self.__table.table_number} | "
            f"{self.__date} at {self.__time}"
        )


class Order:
    """
    Represents a food and/or drink order placed by a customer.
    Calculates the total price and generates a printable receipt.
    """

    def __init__(
        self,
        customer,
        food_items: list,
        drink_items: list
    ) -> None:
        """Initialize an order with a customer and lists of food and drink items."""
        self.__order_id: str = str(uuid.uuid4())[:8].upper()  # unique order ID
        self.__customer = customer
        self.__food_items: list = food_items    # list of MenuItem objects (food)
        self.__drink_items: list = drink_items  # list of MenuItem objects (drinks)
        self.__created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__total: float = self.__calculate_total()  # compute once at creation

    # Properties

    @property
    def order_id(self) -> str:
        """Return the unique order ID."""
        return self.__order_id

    @property
    def customer(self):
        """Return the Customer object associated with this order."""
        return self.__customer

    @property
    def total(self) -> float:
        """Return the total price of this order in FCFA."""
        return self.__total

    # Private helper

    def __calculate_total(self) -> float:
        """
        Add up the prices of all food and drink items.
        Private method: the calculation is an internal detail.
        """
        food_total: float = sum(item.price for item in self.__food_items)
        drink_total: float = sum(item.price for item in self.__drink_items)
        return food_total + drink_total

    # Public methods

    def to_dict(self) -> dict:
        """
        Convert this order to a plain dictionary.
        Used by FileManager to save order data to a text file.
        """
        return {
            "order_id": self.__order_id,
            "customer_name": self.__customer.full_name,
            "customer_phone": self.__customer.phone_number,
            "food_items": [item.name for item in self.__food_items],
            "drink_items": [item.name for item in self.__drink_items],
            "total_fcfa": self.__total,
            "created_at": self.__created_at
        }

    def display_receipt(self) -> None:
        """Print a detailed, itemised receipt for this order."""
        line: str = "─" * 47
        print(f"\n  {'═' * 47}")
        print(f"  ║{'  🧾  ORDER RECEIPT':^45}║")
        print(f"  {'═' * 47}")
        print(f"  Order ID  : #{self.__order_id}")
        print(f"  Customer  : {self.__customer.full_name}")
        print(f"  Phone     : {self.__customer.phone_number}")
        print(f"  Date/Time : {self.__created_at}")
        print(f"  {line}")

        # Print food items (if any were ordered)
        if self.__food_items:
            print("\n  🍽  Food Items:")
            for item in self.__food_items:
                print(f"      {item.name:<32} {item.price:>6.0f} FCFA")

        # Print drink items (if any were ordered)
        if self.__drink_items:
            print("\n  🥤  Drink Items:")
            for item in self.__drink_items:
                print(f"      {item.name:<32} {item.price:>6.0f} FCFA")

        # Print total at the bottom
        print(f"\n  {line}")
        print(f"  {'TOTAL':.<42} {self.__total:>6.0f} FCFA")
        print(f"  {line}")
        print("  ✅  Order confirmed! Thank you for dining with us.")
        print(f"  {'═' * 47}\n")

    def __str__(self) -> str:
        """Return a one-line summary of this order."""
        return (
            f"Order #{self.__order_id} | "
            f"{self.__customer.full_name} | "
            f"Total: {self.__total:.0f} FCFA"
        )
