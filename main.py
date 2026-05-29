"""
main.py - Entry point for RestoManagerG13.
Author: Adam (Group Leader)

RestoManagerG13 is a restaurant management system that lets customers:
  1. Reserve a table   (Monday–Saturday, 08:00–23:59)
  2. Order food and/or drinks from the menu
  3. View menus, table availability, and restaurant information

Run this file to start the application:
    python main.py
"""

# Imports
import sys                     # used to exit the program cleanly
from datetime import datetime, timedelta  # used to show the current date, time, and date math

from restaurant_ctrl import Restaurant
from person import Customer
from file_manager import FileManager


# Helper functions

def get_customer_info() -> Customer:
    """
    Prompt the user to enter their full name and phone number.
    Validates both inputs and returns a Customer object.
    """
    print("\n  ── Enter your personal information ──────────────")

    # Keep asking for a name until the user gives a valid one (≥3 characters)
    while True:
        full_name: str = input("  Full name     : ").strip()
        if len(full_name) >= 3:
            break   # valid name entered
        print("  ⚠  Name must be at least 3 characters. Please try again.")

    # Keep asking for a phone number until the user gives a valid one
    while True:
        phone: str = input("  Phone number  : ").strip()
        if phone.isdigit() and len(phone) >= 8:
            break   # valid phone number entered
        print("  ⚠  Phone must contain digits only and be at least 8 digits.")

    return Customer(full_name, phone)


def get_reservation_date(restaurant: Restaurant) -> tuple[str, object]:
    """
    Ask the user for a reservation day/date and return the selected date.
    Accepts English weekdays or a date in YYYY-MM-DD format.
    """
    print("\n  ── Reservation date selection ───────────────────")
    print("  Enter a weekday (Monday–Saturday) or a date (YYYY-MM-DD).")
    print("  The restaurant is open Monday to Saturday only.")

    day_mapping: dict = {
        day.lower(): day for day in restaurant.WORKING_DAYS
    }

    today_date = datetime.now().date()

    while True:
        user_input = input("  Day / date      : ").strip()
        if not user_input:
            print("  ⚠  Please enter a weekday or a date.")
            continue

        normalized = user_input.lower()
        if normalized in day_mapping:
            requested_day = day_mapping[normalized]
            target_weekday = restaurant.WORKING_DAYS.index(requested_day)
            days_ahead = (target_weekday - today_date.weekday() + 7) % 7
            reservation_date = today_date if days_ahead == 0 else today_date + timedelta(days=days_ahead)
        else:
            try:
                reservation_date = datetime.strptime(user_input, "%Y-%m-%d").date()
            except ValueError:
                print("  ⚠  Invalid date. Use YYYY-MM-DD or an English weekday.")
                continue
            if reservation_date.weekday() == 6:
                print("  ⚠  The restaurant is closed on Sunday. Choose another day.")
                continue

        if reservation_date < today_date:
            print("  ⚠  The reservation date cannot be in the past.")
            continue

        selected_day_name = restaurant.WORKING_DAYS[reservation_date.weekday()]
        print(
            f"  ✅  Selected date: {reservation_date} "
            f"({selected_day_name})"
        )
        return reservation_date.strftime("%Y-%m-%d"), reservation_date


def handle_reservation(restaurant: Restaurant) -> None:
    """
    Walk the customer through the table reservation process.
    Shows available tables, collects booking details, and confirms.
    """
    print("\n  ══════════════════════════════════════════════════")
    print(f"  {'🪑  TABLE RESERVATION':^48}")
    print("  ══════════════════════════════════════════════════")

    # Collect customer info
    customer: Customer = get_customer_info()

    # Ask for the requested reservation date / weekday and validate it
    visit_date, visit_date_obj = get_reservation_date(restaurant)

    while True:
        visit_time: str = input(
            "  Arrival time  (HH:MM, or Enter for 12:00)      : "
        ).strip()
        if not visit_time:
            visit_time = "12:00"

        # Validate time format
        try:
            parts = visit_time.split(":")
            if len(parts) != 2:
                raise ValueError
            h, m = map(int, parts)
            if not (0 <= h <= 23 and 0 <= m <= 59):
                raise ValueError
        except (ValueError, IndexError):
            print("  ⚠  Invalid time format. Please use HH:MM.")
            continue

        # Combine reservation date and the provided time; ensure not in the past
        reservation_dt = datetime.combine(visit_date_obj, datetime.min.time()).replace(hour=h, minute=m)
        if reservation_dt < datetime.now():
            print("  ⚠  You cannot reserve for a past time. Please choose a future date/time.")
            continue

        visit_time = f"{h:02d}:{m:02d}"
        break

    print(f"\n  ✅  Reservation requested for {visit_date_obj.strftime('%A %d/%m/%Y')} at {visit_time}.")

    # Ask for the duration of the reservation
    while True:
        try:
            duration_input = input(
                "  How many hours will you occupy the table? "
                "(1–12, Enter = 2 hours): "
            ).strip()
            if not duration_input:
                duration = 2
                break
            duration = int(duration_input)
            if 1 <= duration <= 12:
                break
            print("  ⚠  Duration must be between 1 and 12 hours.")
        except ValueError:
            print("  ⚠  Enter a valid hour count or press Enter for 2 hours.")

    # Check if any table is available for this time slot
    available: list = restaurant.get_available_tables(visit_date, visit_time, duration)
    if not available:
        print("  ❌  Sorry, no tables are available for that date and time.")
        return

    # Show available tables for this time slot
    restaurant.display_tables(visit_date, visit_time, duration)

    # Ask which table they want
    while True:
        try:
            table_no: int = int(input("\n  Table number to reserve : ").strip())
            break
        except ValueError:
            print("  ⚠  Please enter a valid number.")

    # Ask how many guests will be attending
    while True:
        try:
            guests: int = int(input("  Number of guests                              : ").strip())
            if guests >= 1:
                break
            print("  ⚠  At least 1 guest is required.")
        except ValueError:
            print("  ⚠  Please enter a valid number.")

    # Attempt to create the reservation in the restaurant controller
    reservation = restaurant.make_reservation(
        customer, table_no, visit_date, visit_time, guests, duration
    )

    # Show the receipt if reservation was successful
    if reservation:
        reservation.display_receipt()
    else:
        print("\n  ❌  Reservation could not be completed. Please try again.\n")


def handle_order(restaurant: Restaurant) -> None:
    """
    Walk the customer through placing a food and/or drink order.
    Displays menus, collects item selections, and prints the receipt.
    """
    print("\n  ══════════════════════════════════════════════════")
    print(f"  {'🍽  FOOD & DRINK ORDER':^48}")
    print("  ══════════════════════════════════════════════════")

    # Get customer info before showing the menu
    customer: Customer = get_customer_info()

    # Display the full menu (food + drinks)
    restaurant.display_menus()

    # Collect food item selections
    food_ids: list = []
    print("\n  Enter food item numbers separated by spaces")
    print("  Example: 1 3 6   — Press Enter to skip food")
    food_input: str = input("  Food choices  : ").strip()

    if food_input:
        # Convert each space-separated entry to an integer ID
        for part in food_input.split():
            if part.isdigit():
                food_ids.append(int(part))

    # Collect drink item selections
    drink_ids: list = []
    print("\n  Enter drink item numbers separated by spaces")
    print("  Example: 1 2 3  — Press Enter to skip drinks")
    drink_input: str = input("  Drink choices : ").strip()

    if drink_input:
        for part in drink_input.split():
            if part.isdigit():
                drink_ids.append(int(part))

    # At least one item must be selected
    if not food_ids and not drink_ids:
        print("\n  ⚠  No items selected. Order cancelled.\n")
        return

    # Ask the customer to confirm before placing the order
    confirm: str = input("\n  Confirm order? (yes / no) : ").strip().lower()
    if confirm not in ("yes", "y", "oui", "o"):
        print("  ❌  Order cancelled.\n")
        return

    # Place the order through the restaurant controller
    order = restaurant.place_order(customer, food_ids, drink_ids)
    order.display_receipt()


def display_main_menu() -> None:
    """Print the main navigation menu."""
    print("\n  ┌─────────────────────────────────────────────┐")
    print("  │              HOME INTERFACE                 │")
    print("  ├─────────────────────────────────────────────┤")
    print("  │  1.  Reserve a table                        │")
    print("  │  2.  Order food / drinks                    │")
    print("  │  3.  View menus                             │")
    print("  │  4.  View table availability                │")
    print("  │  5.  Restaurant information                 │")
    print("  │  0.  Exit                                   │")
    print("  └─────────────────────────────────────────────┘")
    print("  Your choice : ", end="")


def display_restaurant_info(restaurant: Restaurant) -> None:
    """
    Display restaurant details, current status, and session statistics.
    Uses the get_statistics() method from the restaurant controller.
    """
    stats: dict = restaurant.get_statistics()
    now_str: str = datetime.now().strftime("%A %d %B %Y — %H:%M")
    status: str = "🟢  OPEN" if restaurant.is_open() else "🔴  CLOSED"

    print("\n  ══════════════════════════════════════════════════")
    print(f"  {'RESTAURANT INFORMATION':^48}")
    print("  ══════════════════════════════════════════════════")
    print(f"  Name        : {Restaurant.NAME}")
    print(f"  Status      : {status}")
    print(f"  Now         : {now_str}")
    print(f"  Hours       : {Restaurant.OPENING_HOUR:02d}:00 – {Restaurant.CLOSING_HOUR}:59")
    print(f"  Working days: Monday to Saturday (Closed Sunday)")
    print("  ──────────────────────────────────────────────────")
    print(f"  Tables       : {stats['available_tables']} available "
          f"/ {stats['total_tables']} total")
    print(f"  Orders (session)         : {stats['orders_this_session']}")
    print(f"  Total reservations saved : {stats['total_reservations_saved']}")
    print(f"  Total orders saved       : {stats['total_orders_saved']}")
    print("  ══════════════════════════════════════════════════")


# Main function

def main() -> None:
    """
    Entry point for RestoManagerG13.
    Creates the restaurant, shows the welcome banner, and runs the main loop.
    """
    # Create the restaurant (loads tables, menus, and saved data)
    restaurant: Restaurant = Restaurant()

    # Show the welcome banner
    restaurant.display_welcome()

    # Main loop — keeps running until the user chooses to exit
    while True:
        display_main_menu()
        choice: str = input().strip()

        if choice == "1":
            # Start the table reservation flow
            handle_reservation(restaurant)

        elif choice == "2":
            # Start the order flow
            handle_order(restaurant)

        elif choice == "3":
            # Show both menus without ordering
            restaurant.display_menus()

        elif choice == "4":
            # Show current table availability
            restaurant.display_tables()

        elif choice == "5":
            # Show restaurant info and statistics
            display_restaurant_info(restaurant)

        elif choice == "0":
            # Log the exit and close the application
            FileManager.write_log("Application closed by user.")
            print("\n  Thank you for visiting RestoManagerG13! Goodbye! 👋\n")
            sys.exit(0)

        else:
            # Invalid input — prompt again
            print("  ⚠  Invalid choice. Please enter a number from 0 to 5.")


# Program entry point

if __name__ == "__main__":
    main()
