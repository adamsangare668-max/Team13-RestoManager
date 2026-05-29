"""
restaurant_ctrl.py - Core restaurant controller for RestoManagerG13.
Author: Rafiou
"""

# Imports
from datetime import datetime

from menu import FoodMenu, DrinkMenu
from reservation import Table, Reservation, Order
from file_manager import FileManager


# Class 

class Restaurant:
    """
    Central controller for the RestoManagerG13 application.
    Manages all tables, menus, reservations, and orders.
    Demonstrates abstraction: all complex operations are hidden behind
    simple, clearly named methods that main.py can call easily.
    """

    # Class-level constants (shared by all instances)

    NAME: str = "RestoManagerG13"
    OPENING_HOUR: int = 8    # restaurant opens at 08:00
    CLOSING_HOUR: int = 23   # restaurant closes at 23:59

    # Tuple of working days – immutable, used for validation
    WORKING_DAYS: tuple = (
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday"
    )

    TOTAL_TABLES: int = 10   # number of tables in the restaurant

    def __init__(self) -> None:
        """
        Set up the restaurant: create tables, load menus, restore saved data.
        Called once at startup from main.py.
        """
        self.__tables: list = []          # list of Table objects
        self.__reservations: list = []    # list of Reservation objects (this session)
        self.__orders: list = []          # list of Order objects (this session)

        # Create the two menus
        self.__food_menu: FoodMenu = FoodMenu()
        self.__drink_menu: DrinkMenu = DrinkMenu()

        # Set up tables and restore any previously saved reservations
        self.__setup_tables()
        self.__restore_reserved_tables()

        # Make sure data folder exists and log the startup
        FileManager.ensure_data_directory()
        FileManager.write_log(f"Application started — Restaurant: {self.NAME}")

    # Private setup methods

    def __setup_tables(self) -> None:
        """
        Create all tables with different seating capacities.
        Tables 1–4 seat 2 | Tables 5–8 seat 4 | Tables 9–10 seat 6.
        """
        for i in range(1, self.TOTAL_TABLES + 1):
            if i <= 4:
                capacity: int = 2   # small tables
            elif i <= 8:
                capacity: int = 4   # medium tables
            else:
                capacity: int = 6   # large tables
            self.__tables.append(Table(i, capacity))

    def __restore_reserved_tables(self) -> None:
        """
        Load saved reservations from file into memory.
        With the new time-slot system, we don't mark tables as globally reserved.
        """
        saved_records: list = FileManager.load_reservations()

        for record in saved_records:
            # Recreate Reservation objects from saved data
            # (This would require more refactoring; for now we skip restoration)
            pass

    # Display methods 

    def display_welcome(self) -> None:
        """Print the welcome banner with restaurant name and opening hours."""
        print("\n" + "═" * 57)
        print(f"  🍽   Welcome to {self.NAME}   🍽")
        print("═" * 57)
        print(f"  Open : Monday to Saturday")
        print(f"  Hours: {self.OPENING_HOUR:02d}:00 – {self.CLOSING_HOUR}:59")
        print(f"  Closed on Sundays")
        print("═" * 57)

    def display_menus(self) -> None:
        """Show both the food menu and the drinks menu."""
        self.__food_menu.display()
        self.__drink_menu.display()

    def display_tables(self, date: str = None, time: str = None, duration: int = 2) -> None:
        """
        Print the status of every table (available or reserved).
        If date and time are provided, checks for time conflicts.
        """
        print(f"\n  {'─' * 47}")
        if date and time:
            print(f"  Table availability for {date} at {time} ({datetime.strptime(date, '%Y-%m-%d').strftime('%A %d/%m/%Y')})")
            print(f"  {'─' * 47}")
        else:
            print(f"  {'TABLE AVAILABILITY':^45}")
            print(f"  {'─' * 47}")

        for table in self.__tables:
            
            # Determine if table is available for the given time slot

            if date and time:
                has_conflict, conflict_res = self.__has_time_conflict(
                    table.table_number, date, time, duration
                )
                if has_conflict:
                    # Show what time it will be available
                    icon: str = "🔴"
                    status_suffix: str = f" (available from {conflict_res.end_time})"
                else:
                    icon: str = "🟢"
                    status_suffix: str = ""
            else:
                # No time constraint – check global reservation status
                icon: str = "🔴" if table.is_reserved else "🟢"
                status_suffix: str = ""
            
            print(f"  {icon}  {table}{status_suffix}")

        print(f"  {'─' * 47}")

    # Open/closed check

    def is_open(self) -> bool:
        """
        Return True if the restaurant is currently open.
        Checks both the day of the week and the current hour.
        """
        now: datetime = datetime.now()
        day_name: str = now.strftime("%A")    # e.g. 'Monday', 'Sunday'
        current_hour: int = now.hour

        # Check if today is a working day
        if day_name not in self.WORKING_DAYS:
            return False  # closed on Sunday

        # Check if current hour is within opening range
        return self.OPENING_HOUR <= current_hour <= self.CLOSING_HOUR

    # Table lookup

    def get_available_tables(self, date: str = None, time: str = None, duration: int = 2) -> list:
        """
        Return a list of all tables that are available.
        If date and time are provided, filters by time slot availability.
        """
        if date is None or time is None:
            # No time constraint – return all tables
            return self.__tables
        
        # Check which tables have no conflicts for this time slot
        available = []
        for table in self.__tables:
            has_conflict, _ = self.__has_time_conflict(table.table_number, date, time, duration)
            if not has_conflict:
                available.append(table)
        return available

    def get_table_by_number(self, number: int):
        """
        Find and return a Table by its number.
        Returns None if the number does not match any table.
        """
        for table in self.__tables:
            if table.table_number == number:
                return table
        return None   # no matching table found

    # Reservation

    def __has_time_conflict(
        self,
        table_number: int,
        date: str,
        time: str,
        duration: int
    ) -> tuple:
        """
        Check if a table has any time conflicts for the given date and time slot.
        Returns a tuple: (has_conflict: bool, conflicting_reservation: Reservation or None)
        """
        # Parse the requested time slot
        if ":" not in time:
                return (False, None)  # Invalid time format, assume no conflict

        req_start_h, req_start_m = map(int, time.split(":"))
        req_end_h = (req_start_h + duration) % 24
        
        # Check all existing reservations for this table and date
        for reservation in self.__reservations:
            if reservation.table.table_number == table_number and reservation.date == date:
                # Parse the reserved time slot
                res_start_h, res_start_m = map(int, reservation.time.split(":"))
                res_end_h, res_end_m = map(int, reservation.end_time.split(":"))
                
                # Simple overlap check (considering hours only for simplicity)
                # Conflict if requested time overlaps with reserved time
                if req_start_h < res_end_h and req_end_h > res_start_h:
                    return (True, reservation)
        
        return (False, None)

    def make_reservation(
        self,
        customer,
        table_number: int,
        date: str,
        time: str,
        guests: int,
        duration: int = 2
    ):
        """
        Attempt to reserve a specific table for a customer.
        Validates the table number and time slot availability.
        No longer limits by table capacity – accepts any number of guests.
        Returns a Reservation object on success, or None on failure.
        """
        table = self.get_table_by_number(table_number)

        # Validation 1: does the table exist?
        
        if table is None:
            print(f"  ❌  Table {table_number} does not exist.")
            return None

        # Validation 2: check for time conflicts


        has_conflict, conflicting_res = self.__has_time_conflict(
            table_number, date, time, duration
        )
        if has_conflict:
            end_time = conflicting_res.end_time
            print(
                f"  ❌  Table {table_number} is already reserved "
                f"on {date} from {conflicting_res.time} to {end_time}."
            )
            print(f"  💡  This table will be available from {end_time} on that day.")
            return None

        # All checks passed – create the reservation (no need to mark table as globally reserved)
        # Create and store the Reservation object with duration


        reservation = Reservation(customer, table, date, time, guests, duration)
        self.__reservations.append(reservation)
        customer.add_reservation(reservation)

        # Save to file and log the action

        FileManager.save_reservation(reservation.to_dict())
        FileManager.write_log(
            f"RESERVATION #{reservation.reservation_id} — "
            f"{customer.full_name} reserved Table {table_number} "
            f"for {guests} guest(s) on {date} at {time} "
            f"(duration: {duration}h)"
        )

        # Show a short confirmation message including the table number

        print(f"\n  ✅  Reservation saved — Table {table_number} reserved for {customer.full_name}.")

        return reservation

    # Order

    def place_order(
        self,
        customer,
        food_ids: list,
        drink_ids: list
    ):
        """
        Create an order from a list of food IDs and drink IDs.
        Looks up each ID in the appropriate menu, builds the item lists,
        saves the order, and returns the Order object.
        """
        food_items: list = []
        for fid in food_ids:
            item = self.__food_menu.get_item_by_id(fid)
            if item:
                food_items.append(item)   # only add if the ID was found

        drink_items: list = []
        for did in drink_ids:
            item = self.__drink_menu.get_item_by_id(did)
            if item:
                drink_items.append(item)  # only add if the ID was found

        # Create and store the Order object

        order = Order(customer, food_items, drink_items)
        self.__orders.append(order)
        customer.add_order(order)

        # Save to file and log the action

        FileManager.save_order(order.to_dict())
        FileManager.write_log(
            f"ORDER #{order.order_id} — "
            f"{customer.full_name} — Total: {order.total:.0f} FCFA"
        )

        return order

    #  Statistics

    def get_statistics(self) -> dict:
        """
        Return a dictionary of restaurant statistics for the info screen.
        Combines session data with totals from saved files.
        """
        file_summary: dict = FileManager.get_summary()
        available_count: int = len(self.get_available_tables())

        return {
            "total_tables": self.TOTAL_TABLES,
            "available_tables": available_count,
            "reserved_tables": self.TOTAL_TABLES - available_count,
            "orders_this_session": len(self.__orders),
            "total_reservations_saved": file_summary["total_reservations"],
            "total_orders_saved": file_summary["total_orders"]
        }
    

    # Menu properties (controlled access)

    @property
    def food_menu(self) -> FoodMenu:
        """Return the food menu (read-only access from outside)."""
        return self.__food_menu

    @property
    def drink_menu(self) -> DrinkMenu:
        """Return the drinks menu (read-only access from outside)."""
        return self.__drink_menu
