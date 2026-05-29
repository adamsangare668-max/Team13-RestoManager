"""
person.py - Defines the Person and Customer classes for RestoManagerG13.
Author: Eunice
"""

# Imports
from datetime import datetime


# Classes

class Person:
    """
    Base class representing any person (customer or staff).
    Uses encapsulation: name and phone are stored as private attributes.
    """

    def __init__(self, full_name: str, phone_number: str) -> None:
        """Initialize a Person with a full name and phone number."""
        self.__full_name: str = full_name        # private – hidden from outside
        self.__phone_number: str = phone_number  # private – accessed via property

    # Properties (encapsulation: controlled access)

    @property
    def full_name(self) -> str:
        """Return the person's full name."""
        return self.__full_name

    @property
    def phone_number(self) -> str:
        """Return the person's phone number."""
        return self.__phone_number

    # Methods

    def get_info(self) -> str:
        """Return a formatted string with basic person information."""
        return f"Name: {self.__full_name} | Phone: {self.__phone_number}"

    def __str__(self) -> str:
        """Return a readable string when printing a Person object."""
        return self.get_info()


class Customer(Person):
    """
    Represents a restaurant customer.
    Inherits from Person and adds orders and reservations tracking.
    Demonstrates: inheritance, encapsulation, polymorphism (overrides get_info).
    """

    def __init__(self, full_name: str, phone_number: str) -> None:
        """Initialize a Customer with name, phone, and empty activity lists."""
        super().__init__(full_name, phone_number)  # call the parent constructor
        self.__orders: list = []                   # list of Order objects
        self.__reservations: list = []             # list of Reservation objects
        self.__registered_at: str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Properties

    @property
    def orders(self) -> list:
        """Return the list of orders placed by this customer."""
        return self.__orders

    @property
    def reservations(self) -> list:
        """Return the list of reservations made by this customer."""
        return self.__reservations

    @property
    def registered_at(self) -> str:
        """Return the date and time this customer object was created."""
        return self.__registered_at

    # Methods

    def add_order(self, order) -> None:
        """Attach an Order object to this customer's history."""
        self.__orders.append(order)

    def add_reservation(self, reservation) -> None:
        """Attach a Reservation object to this customer's history."""
        self.__reservations.append(reservation)

    def get_info(self) -> str:
        """
        Override parent get_info to include order and reservation counts.
        This demonstrates polymorphism: same method name, richer output.
        """
        base: str = super().get_info()
        return (
            f"{base} | Orders: {len(self.__orders)} | "
            f"Reservations: {len(self.__reservations)}"
        )

    def __str__(self) -> str:
        """Return a readable string when printing a Customer object."""
        return self.get_info()

from datetime import datetime


# Classes

class Person:
    """
    Base class representing any person (customer or staff).
    Uses encapsulation: name and phone are stored as private attributes.
    """

    def __init__(self, full_name: str, phone_number: str) -> None:
        """Initialize a Person with a full name and phone number."""
        self.__full_name: str = full_name        # private – hidden from outside
        self.__phone_number: str = phone_number  # private – accessed via property

    # Properties (encapsulation: controlled access)

    @property
    def full_name(self) -> str:
        """Return the person's full name."""
        return self.__full_name

    @property
    def phone_number(self) -> str:
        """Return the person's phone number."""
        return self.__phone_number

    # Methods

    def get_info(self) -> str:
        """Return a formatted string with basic person information."""
        return f"Name: {self.__full_name} | Phone: {self.__phone_number}"

    def __str__(self) -> str:
        """Return a readable string when printing a Person object."""
        return self.get_info()


class Customer(Person):
    """
    Represents a restaurant customer.
    Inherits from Person and adds orders and reservations tracking.
    Demonstrates: inheritance, encapsulation, polymorphism (overrides get_info).
    """

    def __init__(self, full_name: str, phone_number: str) -> None:
        """Initialize a Customer with name, phone, and empty activity lists."""
        super().__init__(full_name, phone_number)  # call the parent constructor
        self.__orders: list = []                   # list of Order objects
        self.__reservations: list = []             # list of Reservation objects
        self.__registered_at: str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Properties

    @property
    def orders(self) -> list:
        """Return the list of orders placed by this customer."""
        return self.__orders

    @property
    def reservations(self) -> list:
        """Return the list of reservations made by this customer."""
        return self.__reservations

    @property
    def registered_at(self) -> str:
        """Return the date and time this customer object was created."""
        return self.__registered_at

    # Methods

    def add_order(self, order) -> None:
        """Attach an Order object to this customer's history."""
        self.__orders.append(order)

    def add_reservation(self, reservation) -> None:
        """Attach a Reservation object to this customer's history."""
        self.__reservations.append(reservation)

    def get_info(self) -> str:
        """
        Override parent get_info to include order and reservation counts.
        This demonstrates polymorphism: same method name, richer output.
        """
        base: str = super().get_info()
        return (
            f"{base} | Orders: {len(self.__orders)} | "
            f"Reservations: {len(self.__reservations)}"
        )

    def __str__(self) -> str:
        """Return a readable string when printing a Customer object."""
        return self.get_info()


class Staff(Person):
    """
    Represents a restaurant staff member.
    Inherits from Person and adds a role attribute.
    Second child class – demonstrates inheritance with a different purpose.
    """

    # Tuple of allowed roles (immutable, used for validation)
    VALID_ROLES: tuple = ("Waiter", "Chef", "Manager", "Cashier")

    def __init__(self, full_name: str, phone_number: str, role: str) -> None:
        """Initialize a Staff member with name, phone, and a job role."""
        super().__init__(full_name, phone_number)
        # Only assign role if it is valid, otherwise default to Waiter
        self.__role: str = role if role in self.VALID_ROLES else "Waiter"

    @property
    def role(self) -> str:
        """Return the staff member's role."""
        return self.__role

    def get_info(self) -> str:
        """
        Override parent get_info to include the staff role.
        Polymorphism: same method name as Customer.get_info, different output.
        """
        base: str = super().get_info()
        return f"{base} | Role: {self.__role}"

    def __str__(self) -> str:
        """Return a readable string when printing a Staff object."""
        return self.get_info()
