from typing import List

# Constants for list_attributes
ORDER_ID = 0
NAME = 1
PHONE = 2
ADDRESS = 3
NOTE = 4

# Constants for Address List
NUM = 0
STREET = 1
POSTAL_CODE = 2

# TO ADD AN ADDITIONAL ATTRIBUTE TO THE ORDER CLASS, REMEMBER:
# - that it must be inserted before NOTE
# - to increment NOTE (and any others) by 1
# - to add a default attribute in class order
# - to change the Order __init__ and __str__ method if necessary
# - that create_delivery function may need some changes


class Order:
    """
    Each order contains the order number, name of the costumer, phone number, and address for delivery.

    The name of costumer is a string containing the name of the costumer.

    The phone number is a string of the phone number in the following format: '(###)-###-####'

    The Address attribute is a list containing the following elements in the following order:
    - the number
    - street name
    - postal code
    """

    order_id = "ORDER"
    name = "NAME"
    phone = "(###)-###-####"
    address = [0, "ADDRESS AVE", "A1A 1A1"]
    note = "N/A"

    def __init__(self, list_attributes: list) -> None:
        """The list of attributes must be formatted in the following order:

        [ORDER_ID, NAME, PHONE, ADDRESS, (NOTE)]

        - the note at the end is optional and is not required
        """

        self.order_id = list_attributes[ORDER_ID]
        self.name = list_attributes[NAME]
        self.phone = list_attributes[PHONE]
        self.address = list_attributes[ADDRESS]
        if len(list_attributes) == NOTE + 1:
            self.note = list_attributes[NOTE]

    def __str__(self) -> str:
        return '{}, {}, {}, {}, {}'.format(self.order_id, self.name, self.phone, self.address, self.note)


class Delivery:
    """
    Each Delivery contains a dictionary attribute named orders containing the name and
    order objects in the following format:

    {'Order 1': Order 1 Object, 'Order 2': Order 2 object}

    It also contains the number of orders in the delivery, under the attribute:
    order_count

    Contains search methods to find specified orders.
    """

    orders = {}
    order_count = 0

    def __init__(self, dict_of_orders: dict, order_count: int) -> None:
        self.orders = dict_of_orders
        self.order_count = order_count

    def address_search(self, num, street, postal_code) -> Order:
        """Returns the order number/order id which has the matching address"""

        for order in self.orders.values():
            if num == order.address[NUM] and street == order.address[STREET] and postal_code == order.address[POSTAL_CODE]:
                return order

        # raise Exception("Order not found")


def create_delivery(file_name) -> Delivery:
    """
    Creates a delivery object from a list of Order objects from info from a text file.

    Each order block is started and ended by a line containing 'END'.
    Each order block it will be formatted as the following:

    END                             - Start of order block
    Order0                          - Order number
    NAME                            - Name of costumer
    (###)-###-####                  - Phone number
    [0, ADDRESS AVE, A1A 1A1]       - Address
    Order notes                     - Additional Order information (optional line)
    END                             - End of order block
    """

    current_order = []
    dict_of_orders = {}
    order_count = 0

    with open(file_name, 'r') as order_file:
        for line in order_file:
            clean_line = line.strip()

            if clean_line == "END":
                if order_count != 0:
                    dict_of_orders[current_order[0]] = Order(current_order)
                    order_count += 1
                    current_order = []
                else:
                    order_count += 1

            elif clean_line.startswith('['):
                clean_line = clean_line.lower()
                clean_line = clean_line[1:-1].split(', ')
                clean_line[0] = int(clean_line[0])
                current_order.append(clean_line)

            else:
                current_order.append(clean_line)
    if clean_line != "END":
        raise AttributeError

    order_count -= 1
    return Delivery(dict_of_orders, order_count)


def print_orders(file_name):
    delivery = create_delivery(file_name)

    for key in sorted(delivery.orders.keys()):
        print(delivery.orders[key])


def print_route(delivery: Delivery, route: List[str], name="No Route Name Given"):
    """Prints order details based on a list of order ids given by the route"""

    print(name)
    for order_id in route:
        print(delivery.orders[order_id])


def cls():
    """Used to create space in the console to make content more presentable"""
    print("\n"*50)


def search_delivery(search_action: str, delivery: Delivery) -> Order:
    """
    Searches delivery based on search_action

    Search by order id is search_action == 'id' or 'ID'

    Search by address is search_action == 'a' or 'A'
    """

    if search_action.lower() == "id":
        order_id = input("\nInput Order ID: ")
        return delivery.orders[order_id]

    if search_action.lower() == "a":
        address = input("\nInput Address (Format address as '0, ADDRESS AVE, A1A 1A1'): ").split(", ")

        num = int(address[NUM])
        street = address[STREET].lower()
        postal_code = address[POSTAL_CODE].lower()

        return delivery.address_search(num, street, postal_code)


if __name__ == "__main__":
    program_run = True
    main_menu = True

    # list1 = ["Order2", "Order5", "Order3", "Order4", "Order1"]
    # print_orders()
    # print_route(list1, "Route 1")
    while program_run:
        # SELECT FILE
        delivery_file = input("Name of delivery file: ")
        try:
            print()
            print_orders(delivery_file)
            print()
        except AttributeError:
            print("Please check the format of the file. Check if END is placed correctly in the file.")
            program_run = False
            continue
        except FileNotFoundError:
            print("Can not find file name\n\n")
            continue

        confirmation = input("Confirm this delivery, [Y]es, [N]o: ")

        cls()

        if confirmation.lower() == "y":
            current_delivery = create_delivery(delivery_file)
            print("Delivery has been created\n")
        elif confirmation.lower() == "n":
            if input("Would you like to Exit [E] or input new filename [N]?\n\n\n").lower() == "e":
                program_run = False
            else:
                print("Please input new delivery filename.\n")
            continue

        # MAIN MENU
        while main_menu:
            main_action = input("Choose what to do: \n"
                                "Search [S]\n"
                                "Enter route [R]\n"
                                "Exit [E]\n")

            cls()

            # SEARCH MENU
            if main_action.lower() == "s":
                while True:
                    search_action = input("Search by:\n"
                                          "Order_id [ID]\n"
                                          "Address [A]\n")
                    try:
                        current_order1 = search_delivery(search_action, current_delivery)
                        print("\n" + str(current_order1) + "\n")
                        break
                    except KeyError:
                        print("\nCan not find order, please enter correct order id\n")
                    except (ValueError, IndexError):
                        print("\nInvalid address format, please try again\n")

            elif main_action.lower() == "r":
                route_name = input("\n\nEnter Route Name: ")
                route_list = input("\n\nEnter route (format by order id as such: "
                                   "Order Id 1, Order Id 2...): ").split(", ")
                print()
                print_route(current_delivery, route_list, route_name)
                print()

            elif main_action.lower() == "e":
                main_menu = False
            else:
                cls()
                print("Not a valid action please try again\n")
        # If there is any loop after this, make sure to set main_menu = True

        # TERMINATE PROGRAM (MUST BE LAST IN WHILE LOOP)
        terminate = input("Terminate Program, [Y]es, [N]o: ")
        if terminate.lower() == "y":
            program_run = False
        elif terminate.lower() == "n":
            main_menu = True
            print("\n\n\n")
        else:
            print("Not a valid action.")
            program_run = False

    print("Program has been terminated")
