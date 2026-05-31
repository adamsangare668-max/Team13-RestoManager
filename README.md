# RestoManagerG13

A restaurant management system written in Python, developed as part of a group project for the **Programming I with Python** course at the Burkina Institute of Technology (BIT).

RestoManagerG13 is a terminal-based application that simulates the core operations of a restaurant. Customers can reserve a table for a specific date and time, place food and drink orders from the menu, view table availability, and consult restaurant information. The program validates all user inputs, prevents double-booking through time-slot conflict detection, persists reservations and orders to files, and generates formatted receipts for both reservations and orders.

---

## 1. Project Title and Description

**RestoManagerG13** — Restaurant Table Reservation and Order Management System

RestoManagerG13 is a command-line application that allows customers to interact with a restaurant's services. Upon launch, the user is presented with a main menu offering five options: reserve a table, order food or drinks, view the menus, check table availability, and display restaurant information. When reserving a table, the customer enters their name and phone number, selects a date, time, and duration, and the system checks for time-slot conflicts before confirming the booking and printing a receipt. When placing an order, the customer chooses food and drink items by their menu numbers, and the system calculates the total and prints an itemised receipt. All reservations and orders are saved to text files so that data persists between sessions. An activity log records every significant action with a timestamp.

---

## 2. How to Run the Project

**Python version required:** Python 3.10 or above

**External dependencies:** None — the project uses only the Python standard library.

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_GROUP_REPO/RestoManagerG13.git

# 2. Navigate into the project folder
cd RestoManagerG13

# 3. Run the application
python main.py
```

On first run, the program will automatically create a `data/` folder in the same directory to store the following files:

- `data/reservations.txt` — all reservation records
- `data/orders.txt` — all order records
- `data/activity_log.txt` — timestamped log of every action

No additional setup or installation steps are required.

---

## 3. Features

- **Table reservation** — Reserve a table for a specific date and time slot (Monday to Saturday, 08:00–23:59). The system validates the date, time format, and duration, and checks for time-slot conflicts before confirming.
- **Food and drink ordering** — Browse the food menu (12 dishes) and drinks menu (13 beverages), select items by their number, and receive an itemised receipt with the total in FCFA.
- **Menu display** — View the full food menu and drinks menu separately, with item names, prices, and availability status.
- **Table availability** — Check which tables are available for a given date and time slot. Tables that are already reserved show the time they will become available again.
- **Restaurant information** — Display the restaurant name, current open/closed status, opening hours, and session statistics (available tables, orders this session, total reservations and orders saved).
- **Input validation** — Customer name must be at least 3 characters; phone number must be at least 8 digits; time must be in HH:MM format; duration must be between 1 and 12 hours.
- **Data persistence** — All reservations and orders are saved to text files using JSON format, so data is retained between program runs.
- **Activity logging** — Every reservation, order, application start, and application exit is recorded in a plain-text log file with a timestamp.

---

## 4. Technologies Used

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Programming language |
| `os` | Standard library | Checking and creating the `data/` directory |
| `uuid` | Standard library | Generating unique reservation and order IDs |
| `datetime` | Standard library | Timestamps, date formatting, and open/close checks |
| `sys` | Standard library | Clean program exit |

No external packages or third-party libraries are used.

---

## 5. Project Structure

```
RestoManagerG13/
|
├── main.py              # Entry point — main loop, user menus, and interaction flows
├── restaurant_ctrl.py   # Restaurant class — core business logic (reservations, orders, statistics)
├── file_manager.py      # FileManager class — all file I/O (read/write reservations, orders, log)
├── menu.py              # MenuItem, Menu, FoodMenu, DrinkMenu classes — menu data and display
├── person.py            # Person, Customer, Staff classes — people in the system
├── reservation.py       # Table, Reservation, Order classes — tables, bookings, and orders
|
└── data/                # Auto-created on first run
    ├── reservations.txt  # Saved reservation records (JSON format)
    ├── orders.txt        # Saved order records (JSON format)
    └── activity_log.txt  # Timestamped log of all actions
```

| File | Description |
|---|---|
| `main.py` | Contains the main loop, the five menu options, helper functions for collecting customer info, reservation details, and order details, and the entry point `if __name__ == "__main__"`. |
| `restaurant_ctrl.py` | The `Restaurant` class that manages all tables, menus, reservations, and orders. It provides methods for making reservations, placing orders, displaying menus and tables, and checking if the restaurant is currently open. |
| `file_manager.py` | The `FileManager` class that handles all reading and writing of data files. It saves and loads reservations and orders as JSON, and maintains a plain-text activity log. |
| `menu.py` | Defines `MenuItem` (a single dish or drink), `Menu` (base class for any menu), `FoodMenu` (pre-loaded with 12 West African and international dishes), and `DrinkMenu` (pre-loaded with 13 beverages). |
| `person.py` | Defines `Person` (base class with name and phone), `Customer` (extends Person with order and reservation history), and `Staff` (extends Person with a job role). |
| `reservation.py` | Defines `Table` (a physical table with number and capacity), `Reservation` (a table booking with time slot and guest count), and `Order` (a food/drink order with total calculation). |

---

## 6. OOP Structure

### Class Overview

| Class | File | Inherits From | Key Methods |
|---|---|---|---|
| `Person` | person.py | — | `get_info()`, `__str__()` |
| `Customer` | person.py | `Person` | `add_order()`, `add_reservation()`, `get_info()` *(override)* |
| `Staff` | person.py | `Person` | `get_info()` *(override)* |
| `MenuItem` | menu.py | — | `to_dict()`, `__str__()` |
| `Menu` | menu.py | — | `add_item()`, `get_available_items()`, `get_item_by_id()`, `display()` |
| `FoodMenu` | menu.py | `Menu` | `display()` *(override)* |
| `DrinkMenu` | menu.py | `Menu` | `display()` *(override)* |
| `Table` | reservation.py | — | `reserve()`, `free()`, `__str__()` |
| `Reservation` | reservation.py | — | `to_dict()`, `display_receipt()`, `__str__()` |
| `Order` | reservation.py | — | `to_dict()`, `display_receipt()`, `__str__()` |
| `FileManager` | file_manager.py | — | `save_reservation()`, `load_reservations()`, `save_order()`, `load_orders()`, `write_log()`, `get_summary()` |
| `Restaurant` | restaurant_ctrl.py | — | `make_reservation()`, `place_order()`, `display_menus()`, `display_tables()`, `is_open()`, `get_statistics()` |

### Inheritance Diagram

```
Person
├── Customer
└── Staff

Menu
├── FoodMenu
└── DrinkMenu
```

### OOP Principles Demonstrated

- **Encapsulation** — All class attributes are private (e.g. `__full_name`, `__price`, `__is_reserved`) and are accessed through `@property` decorators. No attribute is accessed directly from outside its class.
- **Abstraction** — The `Restaurant` class hides all complex logic (time-slot conflict detection, table lookup, order calculation) behind simple method calls like `make_reservation()` and `place_order()`. The `FileManager` class hides all file operations so the rest of the application never touches files directly.
- **Inheritance** — `Customer` and `Staff` both extend `Person`, inheriting the name and phone attributes while adding their own specific behaviour. `FoodMenu` and `DrinkMenu` both extend `Menu`, inheriting the item list and search methods while loading their own specific data.
- **Polymorphism** — The `get_info()` method behaves differently in `Person`, `Customer`, and `Staff`: each class overrides it to add its own information. Similarly, the `display()` method is overridden in `FoodMenu` and `DrinkMenu` to add menu-specific headers before calling the parent's display logic.

---

## 7. Acknowledgements

- Python official documentation: https://docs.python.org/3/
- Python `uuid` module: https://docs.python.org/3/library/uuid.html
- Python `datetime` module: https://docs.python.org/3/library/datetime.html
- PEP 8 Style Guide: https://pep8.org/
- Course lectures and practical sessions — Programming I with Python, BIT, 2026

---

## 8. Group Members & Contributions

Every group member has a personal GitHub profile and has contributed significantly to the repository in a progressive workflow.

### Summary of Contributions

| Name | Role / Domain | Main File | GitHub Profile |
| :--- | :--- | :--- | :--- |
| **SANGARE Séri Porna Adam** | Group Leader — User Interface and Main Entry Point | `main.py` | [github.com/adam](https://github.com/adamsangare668-max) |
| **SANDWIDI Abdoul Rafiou** | Central Controller and Business Logic | `restaurant_ctrl.py` | [github.com/rafiou](https://github.com/SANDWIDI-Rafiou-beep) |
| **SAWADOGO Pulchérie** | Data Persistence and File I/O | `file_manager.py` | [github.com/pulcherie](https://github.com/sawadogopulcherie544-art) |
| **SANA Shekinia Aimerance** | Menu and Catalog Modeling | `menu.py` | [github.com/aimerance](https://github.com/sanashekiniaaimerence-cmyk) |
| **SANOU Eunice** | Basic Design and User Management | `person.py` | [github.com/eunice](https://github.com/eunicesanou099-arch) |
| **SAVADOGO Oumou** | Reservation and Table Logic | `reservation.py` | [github.com/oumou](https://github.com/oumou-savadogo) |

---

### Detailed Contributions

#### 1. SANOU Eunice — Basic Design & User Management
* **File:** `person.py`
* **Contribution:** She designed and wrote the core user structures. She implemented the parent class `Person` and its child classes (`Customer` and `Staff`), ensuring the mandatory **Inheritance** principle. She also handled the **Encapsulation** of sensitive user details.

#### 2. SANA Shekinia Aimerence — Menu & Catalog Modeling
* **File:** `menu.py`
* **Contribution:** She constructed the restaurant's menu catalog system. She created the `Menu` and `MenuItem` classes to handle food items and drinks. Her code manages dynamic price displays and item instantiations.

#### 3. SAVADOGO Oumou — Reservation & Table Logic
* **File:** `reservation.py`
* **Contribution:** She developed the functional core of the system's booking engine. She designed the `Reservation` and `Table` classes, encapsulating time-slot conflict detection, table capacity checks, and using lists and dictionaries to track the restaurant's status in real-time.

#### 4. SAWADOGO Pulchérie — Data Persistence & File I/O
* **File:** `file_manager.py`
* **Contribution:** She built the entire data persistence infrastructure. She structured the `FileManager` class to handle reading from and writing to external text files using JSON format, ensuring that reservations and orders are retained across sessions.

#### 5. SANDWIDI Abdoul Rafiou — Central Controller (Business Logic)
* **File:** `restaurant_ctrl.py`
* **Contribution:** He designed the "brain" of the application by developing the `Restaurant` controller class. He successfully applied **Abstraction** by hiding all complex background tasks (file syncing, checking operational hours) behind clean, top-level methods.

#### 6. SANGARE Séri Porna Adam — User Interface, Main Entry & Project Lead
* **File:** `main.py`
* **Contribution:** As the **Group Leader**, he coordinated the global software architecture, managed the GitHub repository workflows, and enforced PEP 8 standards. Technically, he built the final execution script (`main.py`), including the main interactive loop (`while loop`), user inputs with type conversion, and f-string formatted receipts.
