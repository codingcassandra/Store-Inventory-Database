import mysql.connector
import warnings


# removes miscellaneous deprecation warnings that are not relevant to this project
warnings.filterwarnings("ignore", category=DeprecationWarning)

current_user_id = None
current_username = None
current_role = None  

# connects to the sql code
def get_connection():
    #changes the username and password 
    return mysql.connector.connect(
        host="localhost",
        user="guest",
        password="guest",
        database="project4"
    )


# creating a new user
def registerNewUser():
    # changes the username and password
    username = input("What is your desired username?\n>> ")
    password = input("What is your desired password?\n>> ")

#creates the new user with the info from the input
    try:
        db_connection = get_connection()
        cursor = db_connection.cursor()
        cursor.callproc("registerNewUser", [username, password])
        db_connection.commit()
        print("Account created successfully.")

    except mysql.connector.Error as e:
        print(f"Error: {e.msg}")

#ensures all connections and cursors are closed after use
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals():
            db_connection.close()

# when you want to log in with an existing account
def loginWithCreds():
    global current_user_id, current_username, current_role

    username = input("What is your username?\n>> ")
    password = input("What is your password?\n>> ")

    try:
        db_connection = get_connection()
        cursor = db_connection.cursor()
        cursor.callproc("loginWithCreds", [username, password])

        current_user_id = None
        current_username = None
        current_role = None

        result = cursor.stored_results()
        row = None

        for r in result:
            row = r.fetchone()

        if row:
            current_user_id = row[0]
            current_username = row[1]
            current_role = row[2]

        if current_user_id:
            print(f"Welcome, {current_username}.")
        else:
            print("Login failed.")

    except mysql.connector.Error as e:
        print(f"Error: {e.msg}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals():
            db_connection.close()


# when the admin wants to add a new product
def submitNewProduct():
    name = input("What is the product name?\n>> ")
    price = float(input("What is the product price?\n>> "))

    try:
        db_connection = get_connection()
        cursor = db_connection.cursor()
        cursor.callproc("submitNewProduct", [name, price])
        db_connection.commit()
        print("Product added successfully.")

    except mysql.connector.Error as e:
        print(f"Error: {e.msg}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals():
            db_connection.close()

# when the admins wants to edit an already existing product
def editExistingProduct():
    prod_id = int(input("What product ID do you want to edit?\n>> "))
    name = input("What is the product name?\n>> ")
    price = float(input("What is the product price?\n>> "))

    try:
        db_connection = get_connection()
        cursor = db_connection.cursor()
        cursor.callproc("editExistingProduct", [prod_id, name, price])
        db_connection.commit()
        print("Product updated successfully.")

    except mysql.connector.Error as e:
        print(f"Error: {e.msg}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals():
            db_connection.close()

# when you want to see all the products
def getAllProducts():
    print("Now displaying all products.")

    try:
        db_connection = get_connection()
        cursor = db_connection.cursor()
        cursor.callproc("getAllProducts")

        result = cursor.stored_results()
        for r in result:
            rows = r.fetchall()
            for row in rows:
                print(f"{row[0]} {row[1]} {row[2]}")

    except mysql.connector.Error as e:
        print(f"Error: {e.msg}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals():
            db_connection.close()


# when the admin wants to see the total sales
def getSalesTotal():
    try:
        db_connection = get_connection()
        cursor = db_connection.cursor()
        cursor.callproc("getSalesTotal")

        result = cursor.stored_results()
        for r in result:
            row = r.fetchone()
            if row:
                print(f"The total Sales is ${row[0]:.2f}.")

    except mysql.connector.Error as e:
        print(f"Error: {e.msg}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals():
            db_connection.close()

# when a customer wants a new order
def submitOrder():
    prod_id = int(input("What product ID do you want to order?\n>> "))
    qty = int(input("How many do you want to order?\n>> "))

    try:
        db_connection = get_connection()
        cursor = db_connection.cursor()
        cursor.callproc("submitOrder", [prod_id, current_user_id, qty])
        db_connection.commit()

        total_price = None
        prod_name = None

        result = cursor.stored_results()
        for r in result:
            row = r.fetchone()
            if row:
                total_price = row[0]

        cursor2 = db_connection.cursor()
        cursor2.execute("SELECT prodName FROM product WHERE id = %s", (prod_id,))
        row = cursor2.fetchone()
        if row:
            prod_name = row[0]
        cursor2.close()

        if total_price and prod_name:
            print(f"Your order of {qty} {prod_name} has been placed for a total of ${total_price:.2f}.")

    except mysql.connector.Error as e:
        print(f"Error: {e.msg}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals():
            db_connection.close()

# when a customer wants to view all of their previous orders
def viewCustomerOrders():
    print("Now displaying all of your orders.")

    try:
        db_connection = get_connection()
        cursor = db_connection.cursor()
        cursor.callproc("viewCustomerOrders", [current_user_id])

        result = cursor.stored_results()
        for r in result:
            rows = r.fetchall()
            for row in rows:
                print(f"{row[0]} {row[2]}x {row[1]} ${row[3]:.2f}")

    except mysql.connector.Error as e:
        print(f"Error: {e.msg}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals():
            db_connection.close()

# when a customer wants to cancel an existing order
def cancelOrder():
    sale_id = int(input("Which order would you like to cancel?\n>> "))

    try:
        db_connection = get_connection()
        cursor = db_connection.cursor()
        cursor.callproc("cancelOrder", [sale_id, current_user_id])
        db_connection.commit()
        print("The order has been cancelled.")

    except mysql.connector.Error as e:
        print(f"Error: {e.msg}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals():
            db_connection.close()


# admin user menu
def admin_menu():
    while True:
        print(f"\nWelcome, {current_username}. What do you want to do?")
        print("1 = Add New Product")
        print("2 = Edit Existing Product")
        print("3 = See All Products")
        print("4 = View Sales Total")
        print("5 = Logout")

        choice = input(">> ")

        if choice == "1":
            submitNewProduct()
        elif choice == "2":
            editExistingProduct()
        elif choice == "3":
            getAllProducts()
        elif choice == "4":
            getSalesTotal()
        elif choice == "5":
            logout()
            break
        else:
            print("Invalid option.")

# customer user menu
def customer_menu():
    while True:
        print(f"\nWelcome, {current_username}. What do you want to do?")
        print("1 = Submit New Order")
        print("2 = Cancel Existing Order")
        print("3 = View My Orders")
        print("4 = See All Products")
        print("5 = Logout")

        choice = input(">> ")

        if choice == "1":
            submitOrder()
        elif choice == "2":
            cancelOrder()
        elif choice == "3":
            viewCustomerOrders()
        elif choice == "4":
            getAllProducts()
        elif choice == "5":
            logout()
            break
        else:
            print("Invalid option.")

# logs out the current user and resets
def logout():
    global current_user_id, current_username, current_role
    current_user_id = None
    current_username = None
    current_role = None


# default menu 
def main():
    while True:
        print("\nWelcome. Please choose an option.")
        print("1 = Register New User")
        print("2 = Login with Existing Account")

        choice = input(">> ")

        if choice == "1":
            registerNewUser()
        elif choice == "2":
            loginWithCreds()

            if current_role == 1:
                admin_menu()
            elif current_role == 2:
                customer_menu()
        else:
            print("Invalid option.")

# entry point of the program
if __name__ == "__main__":
    main()