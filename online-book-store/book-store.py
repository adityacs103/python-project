# define the book class

class Book:
    def __init__(self, title, author, price, quantity, book_type):
        self.title = title
        self.author = author
        self.price = price
        self.quantity = quantity
        self.book_type = book_type

    def getTitle(self):
        return self.title

    def getAuthor(self):
        return self.author

    def getPrice(self):
        return self.price

    def getQuantity(self):
        return self.quantity

    def getType(self):
        return self.book_type

    def setPrice(self, newPrice):
        self.price = newPrice

    def setQuantity(self, newQuantity):
        self.quantity = newQuantity

    def __repr__(self):
        return f"Book(title={self.title}, author={self.author}, price={self.price}, quantity={self.quantity}, type={self.book_type})"

# define the user class


class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.orders = []

    def getUsername(self):
        return self.username

    def getEmail(self):
        return self.email

    def setEmail(self, newEmail):
        self.email = newEmail

    def setPassword(self, newPassword):
        self.password = newPassword

    def __repr__(self):
        return f"User(username={self.username}, email={self.email})"

# create order class


class Order:
    def __init__(self, order_id, user, book, quantity):
        self.order_id = order_id
        self.user = user
        self.book = book
        self.quantity = quantity

    def getOrderId(self):
        return self.order_id

    def getBook(self):
        return self.book

    def getQuantity(self):
        return self.quantity

    def setQuantity(self, newQuantity):
        self.quantity = newQuantity

    def __repr__(self):
        return f"Order(order_id={self.order_id}, user={self.user.getUsername()}, book={self.book.getTitle()}, quantity={self.quantity})"


# Load books from CSV
def load_books_from_csv(filename):
    books = []
    with open(filename, 'r') as file:
        lines = file.readlines()[1:]
        for line in lines:
            book_info = line.strip().split(',')
            title, author, price, quantity, book_type = book_info
            books.append(Book(title, author, float(
                price), int(quantity), book_type))
    return books

# User management functions

# signup function


def signup():
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    user = User(username, email, password)
    users.append(user)
    print("User signed up successfully!\n")

# login function


def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    for user in users:
        if user.username == username and user.password == password:
            return user
    print("Invalid username or password.")
    return None

# function for emails change


def change_email(user):
    new_email = input("Enter new email: ")
    user.setEmail(new_email)
    print("Email changed successfully!")

# function for password change


def change_password(user):
    new_password = input("Enter new password: ")
    user.setPassword(new_password)
    print("Password changed successfully!")

# Book inventory management functions


def display_books(books):
    print("\nAvailable Books:")
    for idx, book in enumerate(books, start=1):
        print(
            f"{idx}. {book.getTitle()} by {book.getAuthor()} ({book.getQuantity()} available)")

# book searching functions


def search_books(books, keyword):
    matching_books = [book for book in books if keyword.lower()
                      in book.getTitle().lower()]
    return matching_books

# Order processing functions


def place_order(user, book, quantity):
    order_id = f"ORD{len(user.orders) + 1}"
    order = Order(order_id, user, book, quantity)
    user.orders.append(order)
    book.setQuantity(book.getQuantity() - quantity)    


# Main program
books = load_books_from_csv('books.csv')
users = []  # List to store user objects
current_user = None  # To track the logged-in user


while True:
    print("Welcome to Bookiverse:")
    if current_user:
        print("1. Logout")
        print("2. Change Email")
        print("3. Change Password")
        print("4. Display Available Books")
        print("5. Search Books")
        print("6. Place Order")
        print("7. View Cart")
    else:
        print("1. Signup")
        print("2. Login")
    print("8. Exit")

    choice = input("Enter your choice: ")

    if current_user:
        if choice == '1':
            current_user = None
            print("Logged out.")
        elif choice == '2':
            change_email(current_user)
        elif choice == '3':
            change_password(current_user)
        elif choice == '4':
            display_books(books)
        elif choice == '5':
            keyword = input("Enter keyword to search: ")
            matching_books = search_books(books, keyword)
            display_books(matching_books)
        elif choice == '6':
            display_books(books)
            book_idx = int(input("Enter the book number to order: ")) - 1
            quantity = int(input("Enter the quantity: "))
            if 0 < book_idx < len(books) and 0 < quantity <= books[book_idx].getQuantity():
                place_order(current_user, books[book_idx], quantity)
                print("Books added to cart successfully")
            else:
                print("Invalid input or insufficient quantity.")
        elif choice == '7':
            print("\nUser Cart:")
            for order in current_user.orders:
                print(order)
            order_choice = input("Do you want to confirm the orders? (y/n): ")
            if order_choice.lower() == 'y':
                # for order in current_user.orders:
                place_order(current_user, order.getBook(), order.getQuantity())
                current_user.orders = []
                print("Orders confirmed and placed!")
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")
    else:
        if choice == '1':
            signup()
        elif choice == '2':
            current_user = login()
            if current_user:
                print("Login successful!")
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")