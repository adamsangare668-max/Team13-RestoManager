"""
menu.py - Defines MenuItem, Menu, FoodMenu, and DrinkMenu for RestoManagerG13.
Author: Aimerance
"""

# No external imports needed for this module 


# Classes

class MenuItem:
    """
    Represents a single item on the restaurant menu.
    Can be a food item or a drink item.
    Uses encapsulation: all attributes are private.
    """

    def __init__(
        self,
        item_id: int,
        name: str,
        price: float,
        category: str,
        available: bool = True
    ) -> None:
        """Initialize a menu item with its ID, name, price, category, and availability."""
        self.__item_id: int = item_id
        self.__name: str = name
        self.__price: float = price        # price in FCFA
        self.__category: str = category
        self.__available: bool = available

    # Properties 

    @property
    def item_id(self) -> int:
        """Return the item ID."""
        return self.__item_id

    @property
    def name(self) -> str:
        """Return the item name."""
        return self.__name

    @property
    def price(self) -> float:
        """Return the item price in FCFA."""
        return self.__price

    @property
    def category(self) -> str:
        """Return the item category (e.g. 'Rice', 'Grilled', 'Juice')."""
        return self.__category

    @property
    def available(self) -> bool:
        """Return True if the item is currently available."""
        return self.__available

    @available.setter
    def available(self, status: bool) -> None:
        """Allow changing the availability of an item (e.g. sold out)."""
        self.__available = status

    #  Methods 

    def to_dict(self) -> dict:
        """Convert this menu item to a dictionary (useful when saving data)."""
        return {
            "id": self.__item_id,
            "name": self.__name,
            "price": self.__price,
            "category": self.__category,
            "available": self.__available
        }

    def __str__(self) -> str:
        """Return a formatted line showing the item's details in the menu."""
        check: str = "✓" if self.__available else "✗"
        return (
            f"  [{self.__item_id:>3}] {self.__name:<30} "
            f"{self.__price:>7.0f} FCFA  {check}"
        )


class Menu:
    """
    Base class for a restaurant menu (food or drinks).
    Stores a list of MenuItem objects and provides display and search methods.
    Demonstrates abstraction: the internal list is hidden, accessed via methods.
    """

    def __init__(self, menu_type: str) -> None:
        """Initialize the menu with a type label and an empty item list."""
        self.__menu_type: str = menu_type
        self._items: list = []   # protected so child classes can add items

    # Properties 

    @property
    def menu_type(self) -> str:
        """Return the type of this menu (e.g. 'Food' or 'Drinks')."""
        return self.__menu_type

    @property
    def items(self) -> list:
        """Return all items in this menu."""
        return self._items

    # Methods

    def add_item(self, item: MenuItem) -> None:
        """Add a MenuItem to this menu."""
        self._items.append(item)

    def get_available_items(self) -> list:
        """Return only items that are currently available (not sold out)."""
        # List comprehension: keep only available items
        return [item for item in self._items if item.available]

    def get_item_by_id(self, item_id: int):
        """
        Search for and return a MenuItem by its ID.
        Returns None if no item with that ID is found.
        """
        for item in self._items:
            if item.item_id == item_id:
                return item  # found
        return None  # not found

    def display(self) -> None:
        """Print a formatted table of all available items in this menu."""
        separator: str = "─" * 53

        print(f"\n  {'═' * 53}")
        print(f"  ║  {'  ★  ' + self.__menu_type.upper() + ' MENU  ★':<49}║")
        print(f"  {'═' * 53}")
        print(f"  {'No.':<7} {'Item':<30} {'Price':>9}   {'OK'}")
        print(f"  {separator}")

        available_items: list = self.get_available_items()

        if available_items:
            for item in available_items:
                print(item)
        else:
            print("  No items are currently available.")

        print(f"  {separator}")

    def __str__(self) -> str:
        """Return a brief summary of this menu."""
        count: int = len(self.get_available_items())
        return f"{self.__menu_type} Menu — {count} items available"


class FoodMenu(Menu):
    """
    The restaurant food menu.
    Inherits from Menu and pre-loads all local and international dishes.
    Demonstrates inheritance: FoodMenu IS-A Menu with food-specific data.
    Also demonstrates polymorphism: overrides the display() method.
    """

    def __init__(self) -> None:
        """Initialize the food menu and automatically load all dishes."""
        super().__init__("Food")     # call parent constructor with type label
        self.__load_food_items()     # populate items when menu is created

    def __load_food_items(self) -> None:
        """
        Load all food items into the menu using a dictionary.
        Each key is the item ID, and the value is a tuple: (name, price, category).
        """
        # Dictionary: item_id -> (name, price, category)
        food_data: dict = {
            1:  ("Riz sauce arachide",     1500, "Rice Dishes"),
            2:  ("Riz sauce gombo",        1500, "Rice Dishes"),
            3:  ("Riz sauce tomate",       1200, "Rice Dishes"),
            4:  ("Tô avec sauce feuille",  1000, "Traditional"),
            5:  ("Tô avec sauce gombo",    1000, "Traditional"),
            6:  ("Poulet braisé (1/2)",    3500, "Grilled"),
            7:  ("Poulet braisé entier",   6500, "Grilled"),
            8:  ("Poisson braisé",         2500, "Grilled"),
            9:  ("Thiéboudienne",          2000, "Rice Dishes"),
            10: ("Omelette et frites",     1500, "Fast Food"),
            11: ("Salade composée",        1000, "Salad"),
            12: ("Sandwich poulet",        1200, "Fast Food"),
        }

        # Add each food item to the menu using a for loop
        for item_id, (name, price, category) in food_data.items():
            self.add_item(MenuItem(item_id, name, float(price), category))

    def display(self) -> None:
        """
        Override parent display to add a food-specific header line.
        Polymorphism: same method name as DrinkMenu.display(), different output.
        """
        print("\n    Food Menu — Available Mon to Sat, 08:00–23:59")
        super().display()  # call the parent display method for the table


class DrinkMenu(Menu):
    """
    The restaurant drinks menu.
    Inherits from Menu and pre-loads water, juices, mixed drinks, and sodas.
    Demonstrates inheritance and polymorphism (overrides display).
    """

    def __init__(self) -> None:
        """Initialize the drinks menu and automatically load all beverages."""
        super().__init__("Drinks")    # call parent constructor
        self.__load_drink_items()     # populate drinks immediately

    def __load_drink_items(self) -> None:
        """
        Load all drink items using a tuple of tuples.
        Demonstrates meaningful use of tuples (immutable structured data).
        Each entry: (item_id, name, price, category)
        """
        # Tuple of tuples: each inner tuple describes one drink
        drink_data: tuple = (
            (1, "Still Water (500ml)",        300,  "Water"),
            (2, "Still Water (1.5L)",         600,  "Water"),
            (3, "Sparkling Water (500ml)",    400,  "Water"),
            (4, "Orange Juice (fresh)",       700,  "Juice"),
            (5, "Mango Juice (fresh)",        700,  "Juice"),
            (6, "Bissap (hibiscus)",          500,  "Juice"),
            (7, "Zoom-koom (millet drink)",   400,  "Juice"),
            (8, "Tamarind Juice",             500,  "Juice"),
            (9, "Orange Juice + Water",       500,  "Mixed"),
            (10, "Mango Juice + Water",        500,  "Mixed"),
            (11, "Bissap + Sparkling Water",   550,  "Mixed"),
            (12, "Coca-Cola (33cl)",           500,  "Soda"),
            (13, "Fanta (33cl)",               500,  "Soda"),
        )

        # Iterate over the tuple to add each drink item
        for item_id, name, price, category in drink_data:
            self.add_item(MenuItem(item_id, name, float(price), category))

    def display(self) -> None:
        """
        Override parent display to add a drinks-specific header line.
        Polymorphism: same method name as FoodMenu.display(), different output.
        """
        print("\n  🥤  Drinks Menu — Water, Juices, Mixed Drinks & Sodas")
        super().display()  # call the parent display method for the table
