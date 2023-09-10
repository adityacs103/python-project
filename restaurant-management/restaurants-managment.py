import datetime


class User:
    def __init__(self, name, mobile, password, dob, address=None):
        self.name = name
        self.mobile = mobile
        self.password = password
        self.dob = dob
        self.address = address
        self.orders = []


class Order:
    order_id_counter = 1

    def __init__(self, user, order_type):
        self.order_id = f"A{Order.order_id_counter:03d}"
        Order.order_id_counter += 1
        self.user = user
        self.order_type = order_type
        self.items = []
        self.total_amount = 0
        self.timestamp = datetime.datetime.now()


class MenuItem:
    def __init__(self, item_id, name, price):
        self.item_id = item_id
        self.name = name
        self.price = price


menu = [
    MenuItem(1, "Noodles", 2),
    MenuItem(2, "Sandwich", 4),
    MenuItem(3, "Dumpling", 6),
    MenuItem(4, "Muffins", 8),
    MenuItem(5, "Pasta", 10),
    MenuItem(6, "Pizza", 20),
]

drinks_menu = [
    MenuItem(1, "Coffee", 2),
    MenuItem(2, "Colddrink", 4),
    MenuItem(3, "Shake", 6),
]

users = []


def validate_mobile(mobile):
    return mobile.isdigit() and len(mobile) == 10 and mobile.startswith("0")


def validate_password(password):
    if not password[0].isalpha() or not password[-1].isdigit():
        return False
    if not any(char in ['@', '&'] for char in password):
        return False
    return True

    # return password[0].isalpha() and password[-1].isdigit() and password in ['@', '&']


def validate_dob(dob):
    try:
        year = int(dob.split('/')[-1])
        current_year = datetime.datetime.now().year
        return current_year - year >= 16
    except:
        return False


def signup():
    while True:
        print("Sign Up:")
        name = input("Please enter your name: ")
        address = input(
            "Please enter your address (optional, press Enter to skip): ")
        mobile = input("Please enter your mobile number: ")
        if not validate_mobile(mobile):
            print("Invalid mobile number. It should start with 0 and have 10 digits.")
            continue
        password = input("Please enter your password: ")
        if not validate_password(password):
            print("Invalid password format.")
            continue
        confirm_password = input("Please confirm your password: ")
        if password != confirm_password:
            print("Passwords do not match.")
            continue
        dob = input("Please enter your Date of Birth (DD/MM/YYYY): ")
        if not validate_dob(dob):
            print("Invalid Date of Birth. You must be at least 16 years old.")
            continue

        users.append(User(name, mobile, password, dob, address))
        print("You have Successfully Signed up.")
        break


def signin():
    mobile = input("Please enter your Username (Mobile Number): ")
    password = input("Please enter your password: ")
    for user in users:
        if user.mobile == mobile and user.password == password:
            print("You have successfully Signed in.")
            return user
    print("Login failed. Invalid credentials.")
    return None


def order_food(user):
    while True:
        print("Ordering:")
        print("Please Enter 1 for Dine in.")
        print("Please Enter 2 Order Online.")
        print("PLease Enter 3 to go to Login Page.")
        choice = input("Please enter your choice: ")

        if choice == '1':
            dine_in(user)
        elif choice == '2':
            order_online(user)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please select a valid option.")


def dine_in(user):
    print("Dine In Ordering:")
    order = Order(user, "Dine In")
    while True:
        display_menu()
        choice = input(
            "Enter the ID of the item you want to order (7 to proceed to Drink Menu): ")
        if choice == '7':
            break
        item_id = int(choice)
        if item_id < 1 or item_id > 6:
            print("Invalid choice. Please select a valid item.")
            continue
        item = menu[item_id - 1]
        order.items.append(item)
        order.total_amount += item.price
        print(f"{item.name} added to your order.")

    while True:
        display_drinks_menu()
        choice = input(
            "Enter the ID of the drink you want to order (4 to Checkout): ")
        if choice == '4':
            calculate_total_amount(order)
            confirm_order(user, order)
            break
        drink_id = int(choice)
        if drink_id < 1 or drink_id > 3:
            print("Invalid choice. Please select a valid drink.")
            continue
        drink = drinks_menu[drink_id - 1]
        order.items.append(drink)
        order.total_amount += drink.price
        print(f"{drink.name} added to your order.")


def order_online(user):
    print("Order Online:")
    while True:
        print("Enter 1 for Self-Pickup")
        print("Enter 2 for Home Delivery")
        print("Enter 3 to go to Previous Menu")
        choice = input("Please enter your choice: ")

        if choice == '1':
            self_pickup(user)
            break
        elif choice == '2':
            home_delivery(user)
            break
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please select a valid option.")


def self_pickup(user):
    print("Self Pickup:")
    order = Order(user, "Self Pickup")

    while True:
        display_menu()
        choice = input(
            "Enter the ID of the item you want to order (7 to proceed to Drink Menu): ")
        if choice == '7':
            break
        item_id = int(choice)
        if item_id < 1 or item_id > 6:
            print("Invalid choice. Please select a valid item.")
            continue
        item = menu[item_id - 1]
        order.items.append(item)
        order.total_amount += item.price
        print(f"{item.name} added to your order.")

    while True:
        display_drinks_menu()
        choice = input(
            "Enter the ID of the drink you want to order (4 to Checkout): ")
        if choice == '4':
            calculate_total_amount(order)
            confirm_order(user, order)
            break
        drink_id = int(choice)
        if drink_id < 1 or drink_id > 3:
            print("Invalid choice. Please select a valid drink.")
            continue
        drink = drinks_menu[drink_id - 1]
        order.items.append(drink)
        order.total_amount += drink.price
        print(f"{drink.name} added to your order.")


def home_delivery(user):
    print("Home Delivery:")
    if not user.address:
        print("You need to provide your address before proceeding with delivery.")
        choice = input("Enter 'Y' to enter your address or 'N' to go back: ")
        if choice == 'Y' or choice == 'y':
            user.address = input("Please enter your address: ")
        else:
            return

    distance = int(
        input("Please enter the distance from the restaurant (in Kms): "))
    if distance <= 5:
        delivery_charge = 3

    elif distance <= 10:
        delivery_charge = 6

    elif distance <= 15:
        delivery_charge = 10

    else:
        print("We're sorry, we don't deliver to locations more than 15 Kms away.")
        return

    # print(f"Delivery charge: AUD {delivery_charge}")
    order = Order(user, "Delivery")

    while True:
        display_menu()
        choice = input(
            "Enter the ID of the item you want to order (7 to proceed to Drink Menu): ")
        if choice == '7':
            break
        item_id = int(choice)
        if item_id < 1 or item_id > 6:
            print("Invalid choice. Please select a valid item.")
            continue
        item = menu[item_id - 1]
        order.items.append(item)
        order.total_amount += item.price
        print(f"{item.name} added to your order.")

    while True:
        display_drinks_menu()
        choice = input(
            "Enter the ID of the drink you want to order (4 to Checkout): ")
        if choice == '4':
            calculate_total_amount_home(order, delivery_charge)
            confirm_order(user, order)
            break
        drink_id = int(choice)
        if drink_id < 1 or drink_id > 3:
            print("Invalid choice. Please select a valid drink.")
            continue
        drink = drinks_menu[drink_id - 1]
        order.items.append(drink)
        order.total_amount += drink.price
        print(f"{drink.name} added to your order.")


def calculate_total_amount_home(order, delivery_charge):
    if order.order_type == "Delivery":
        order.total_amount += delivery_charge  # Adding delivery charge


def calculate_total_amount(order):
    if order.order_type == "Dine In":
        order.total_amount *= 1.15  # Adding 15% service charge


def confirm_order(user, order):
    for item in order.items:
        print(f"{item.item_id}: {item.name} - Price: AUD {item.price}")
    print(f"Total Amount needed to be paid: AUD {order.total_amount:.2f}")

    proceed_to_checkout = input(
        "Please Enter Y to Proceed to Checkout or Enter N to cancel the Order: ")
    if proceed_to_checkout == 'Y' or proceed_to_checkout == 'y':
        if order.order_type == "Dine In":
            print("Please provide booking details:")
            num_persons = int(input("Number of Persons: "))
            date_of_visit = input("Date of Visit (DD/MM/YYYY): ")
            time_of_visit = input("Time of Visit (HH:MM): ")
            # ... (you can add further logic to handle bookings)
        elif order.order_type == "Self Pickup":
            print("Please provide pickup details:")
            date_of_pickup = input("Date of Pickup (DD/MM/YYYY): ")
            time_of_pickup = input("Time of Pickup (HH:MM): ")
            name_of_person = input("Name of Person Picking up: ")
            # ... (you can add further logic to handle pickup details)
        elif order.order_type == "Delivery":
            print("Please provide delivery details:")
            date_of_delivery = input("Date of Delivery (DD/MM/YYYY): ")
            time_of_delivery = input("Time of Delivery (HH:MM): ")
            # ... (you can add further logic to handle delivery details)

        print("Thank you for your order, your order has been confirmed.")
        user.orders.append(order)

    else:
        cancel_order(user, order)


def cancel_order(user, order):
    confirm = input("Are you sure you want to cancel this order? (Y/N): ")
    if confirm == 'Y' or confirm == 'y':
        print("Your Order is Cancelled.\nNow you can create a new order.")
        order_food(user)
    else:
        print("Order cancellation has been canceled.")


def display_menu():
    print("Menu:")
    for item in menu:
        print(f"{item.item_id}: {item.name} - Price: AUD {item.price}")
    print("Enter 7 for Drinks Menu:")



def display_drinks_menu():
    print("Drinks Menu:")
    for item in drinks_menu:
        print(f"{item.item_id}: {item.name} - Price: AUD {item.price}")
    print("Please Enter 4 for Checkout.")


def print_statistics(user):
    while True:
        print("2.2")
        print("Please enter the option to print the statistics.")
        print("1- All Dine in orders.")
        print("2- All pick up orders.")
        print("3- All deliveries.")
        print("4- All orders (ascending order)")
        print("5- Total amount spent on all orders.")
        print("6- Go to the previous menu")

        option = input("Please enter your choice: ")

        if option == '1':
            print("Option 1: All Dine in orders")
            print("Order ID, Date, Total Amount Paid, Type of Order")
            for order in user.orders:
                if order.order_type == "Dine In":
                    print(
                        f"{order.order_id}, {order.timestamp}, AUD {order.total_amount:.2f}, {order.order_type}")

        elif option == '2':
            print("Option 2: All Pickup Orders")
            print("Order ID, Date, Total Amount Paid, Type of Order")
            for order in user.orders:
                if order.order_type == "Self Pickup":
                    print(
                        f"{order.order_id}, {order.timestamp}, AUD {order.total_amount:.2f}, {order.order_type}")

        elif option == '3':
            print("Option 3: All Deliveries")
            print("Order ID, Date, Order Amount Paid, Type of Order")
            for order in user.orders:
                if order.order_type == "Delivery":
                    print(
                        f"{order.order_id}, {order.timestamp}, AUD {order.total_amount:.2f}, {order.order_type}")

        elif option == '4':
            print("Option 4: All Orders in Descending order (based on amount)")
            print("Order ID, Date, Order Amount Paid, Type of Order")
            sorted_orders = sorted(
                user.orders, key=lambda x: x.total_amount, reverse=True)
            for order in sorted_orders:
                print(
                    f"{order.order_id}, {order.timestamp}, AUD {order.total_amount:.2f}, {order.order_type}")

        elif option == '5':
            print("Option 5: Total Amount Spent (All Types of Orders)")
            total_amount_spent = sum(
                order.total_amount for order in user.orders)
            print(
                f"Total amount spent on all orders: AUD {total_amount_spent:.2f}")

        elif option == '6':
            break

        else:
            print("Invalid choice. Please select a valid option.")


def main():
    while True:
        print("Main Menu:")
        print("Please Enter 1 for Sign Up.")
        print("Please Enter 2 for Sign In.")
        print("Please Enter 3 for Quit.")
        choice = input("Please enter your choice: ")

        if choice == '1':
            signup()
        elif choice == '2':
            user = signin()
            if user:
                while user:
                    print("PLease Enter 2.1 to Start Ordering.")
                    print("Please Enter 2.2 to Print Statistics")
                    print("Please Enter 2.3 for Logout")
                    inner_choice = input("Please enter your choice: ")
                    if inner_choice == '2.1':
                        order_food(user)
                    elif inner_choice == '2.2':
                        print_statistics(user)
                    elif inner_choice == '2.3':
                        print("You have been logged out.")
                        user = None
                    else:
                        print("Invalid choice. Please select a valid option.")
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
