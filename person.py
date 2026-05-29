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


