import streamlit as st
import mysql.connector
from mysql.connector import Error
from faker import Faker
import pandas as pd

# Initialize Faker for synthetic data generation
faker = Faker()

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sara@123',  # Update this with your MySQL root password
    'database': 'SAR'  # Update this with your database name
}

# Establish database connection
def create_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG, connection_timeout=300)
        if conn.is_connected():
            return conn
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Create database and tables
def setup_database():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("CREATE DATABASE IF NOT EXISTS SAR;")
            conn.database = 'SAR'

            # Create Customers Table
            cursor.execute('''CREATE TABLE IF NOT EXISTS Customers (
                customer_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255),
                phone VARCHAR(15),
                location VARCHAR(255),
                signup_date DATE,
                is_premium BOOLEAN,
                preferred_cuisine VARCHAR(100),
                total_orders INT,
                average_rating FLOAT
            );''')

            # Create Restaurants Table
            cursor.execute('''CREATE TABLE IF NOT EXISTS Restaurants (
                restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                cuisine_type VARCHAR(100),
                location VARCHAR(255),
                owner_name VARCHAR(255),
                average_delivery_time INT,
                contact_number VARCHAR(20),
                rating FLOAT,
                total_orders INT,
                is_active BOOLEAN
            );''')

            # Create Orders Table
            cursor.execute('''CREATE TABLE IF NOT EXISTS Orders (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                restaurant_id INT,
                order_date DATETIME,
                delivery_time DATETIME,
                status VARCHAR(50),
                total_amount FLOAT,
                payment_mode VARCHAR(50),
                discount_applied FLOAT,
                feedback_rating INT,
                FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE,
                FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id) ON DELETE CASCADE
            );''')

            # Create Deliveries Table
            cursor.execute('''CREATE TABLE IF NOT EXISTS Deliveries (
                delivery_id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT,
                delivery_status VARCHAR(50),
                distance FLOAT,
                delivery_time INT,
                estimated_time INT,
                delivery_fee FLOAT,
                vehicle_type VARCHAR(50),
                FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE
            );''')

            conn.commit()
            st.success("Database and tables created successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

# Generate synthetic data for all tables
def generate_data():
    customer_data = [
        (
            faker.name(), faker.email(), faker.phone_number()[:15],
            faker.address(), faker.date_this_decade(), faker.boolean(),
            faker.word(ext_word_list=['Indian', 'Chinese', 'Italian', 'Mexican']),
            faker.random_int(min=1, max=100), faker.random_number(digits=2)
        ) for _ in range(200)
    ]

    restaurant_data = [
        (
            faker.company(), faker.word(ext_word_list=['Indian', 'Chinese', 'Italian']),
            faker.city(), faker.name(), faker.random_int(15, 90), faker.phone_number()[:15],
            round(faker.random_number(digits=1) % 5, 1), faker.random_int(1, 500), faker.boolean()
        ) for _ in range(200)
    ]

    order_data = [
        (
            faker.random_int(1, 200), faker.random_int(1, 200),
            faker.date_time_this_year(), faker.date_time_this_year(),
            faker.word(ext_word_list=['Delivered', 'Pending', 'Cancelled']),
            faker.random_number(digits=3), faker.word(ext_word_list=['Credit Card', 'Cash', 'UPI']),
            faker.random_number(digits=2), faker.random_int(1, 5)
        ) for _ in range(200)
    ]

    delivery_data = [
        (
            faker.random_int(1, 200), faker.word(ext_word_list=['In Transit', 'Delivered', 'Failed']),
            faker.random_number(digits=3), faker.random_int(10, 120),
            faker.random_int(10, 120), faker.random_number(digits=2),
            faker.word(ext_word_list=['Bike', 'Car', 'Scooter'])
        ) for _ in range(200)
    ]

    return customer_data, restaurant_data, order_data, delivery_data

# Insert data into tables
def insert_data(data, query):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            for i in range(0, len(data), 10):  # Batch insertion
                cursor.executemany(query, data[i:i+10])
                conn.commit()
            st.success("Data inserted successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

# CRUD Operations
def handle_crud_operations():
    operation = st.radio("Select Operation", ["Create", "Read", "Update", "Delete", "Alter"])
    table_choice = st.selectbox("Select Table", ["Customers", "Restaurants", "Orders", "Deliveries"])

    conn = create_connection()
    if conn:
        cursor = conn.cursor()

        if operation == "Create":
            if table_choice == "Customers":
                name = st.text_input("Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
                location = st.text_input("Location")
                if st.button("Add Customer"):
                    try:
                        cursor.execute('''INSERT INTO Customers (name, email, phone, location, signup_date, is_premium, preferred_cuisine, total_orders, average_rating) VALUES (%s, %s, %s, %s, NOW(), FALSE, 'Indian', 0, 0.0);''',
                                       (name, email, phone, location))
                        conn.commit()
                        st.success("Customer added successfully!")
                    except Error as e:
                        st.error(f"Error: {e}")

        elif operation == "Read":
            try:
                cursor.execute(f"SELECT * FROM {table_choice};")
                rows = cursor.fetchall()
                if rows:
                    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
                    st.dataframe(df)
                else:
                    st.info("No data available.")
            except Error as e:
                st.error(f"Error: {e}")

        elif operation == "Update":
            if table_choice == "Customers":
                customer_id = st.number_input("Enter Customer ID to Update", step=1)
                name = st.text_input("New Name")
                email = st.text_input("New Email")
                phone = st.text_input("New Phone")
                location = st.text_input("New Location")
                if st.button("Update Customer"):
                    try:
                        cursor.execute('''UPDATE Customers 
                                        SET name = %s, email = %s, phone = %s, location = %s 
                                        WHERE customer_id = %s;''',
                                      (name, email, phone, location, customer_id))
                        conn.commit()
                        st.success("Customer updated successfully!")
                    except Error as e:
                        st.error(f"Error: {e}")

            elif table_choice == "Restaurants":
                restaurant_id = st.number_input("Enter Restaurant ID to Update", step=1)
                name = st.text_input("New Name")
                cuisine_type = st.text_input("New Cuisine Type")
                location = st.text_input("New Location")
                if st.button("Update Restaurant"):
                    try:
                        cursor.execute('''UPDATE Restaurants 
                                        SET name = %s, cuisine_type = %s, location = %s 
                                        WHERE restaurant_id = %s;''',
                                      (name, cuisine_type, location, restaurant_id))
                        conn.commit()
                        st.success("Restaurant updated successfully!")
                    except Error as e:
                        st.error(f"Error: {e}")

            elif table_choice == "Orders":
                order_id = st.number_input("Enter Order ID to Update", step=1)
                status = st.text_input("New Status")
                total_amount = st.number_input("New Total Amount", step=0.01)
                if st.button("Update Order"):
                    try:
                        cursor.execute('''UPDATE Orders 
                                        SET status = %s, total_amount = %s 
                                        WHERE order_id = %s;''',
                                      (status, total_amount, order_id))
                        conn.commit()
                        st.success("Order updated successfully!")
                    except Error as e:
                        st.error(f"Error: {e}")

            elif table_choice == "Deliveries":
                delivery_id = st.number_input("Enter Delivery ID to Update", step=1)
                delivery_status = st.text_input("New Delivery Status")
                delivery_fee = st.number_input("New Delivery Fee", step=0.01)
                if st.button("Update Delivery"):
                    try:
                        cursor.execute('''UPDATE Deliveries 
                                        SET delivery_status = %s, delivery_fee = %s 
                                        WHERE delivery_id = %s;''',
                                      (delivery_status, delivery_fee, delivery_id))
                        conn.commit()
                        st.success("Delivery updated successfully!")
                    except Error as e:
                        st.error(f"Error: {e}")

        elif operation == "Delete":
            if table_choice == "Customers":
                customer_id = st.number_input("Enter Customer ID to Delete", step=1)
                if st.button("Delete Customer"):
                    try:
                        cursor.execute("DELETE FROM Customers WHERE customer_id = %s", (customer_id,))
                        conn.commit()
                        st.success("Customer deleted successfully!")
                    except Error as e:
                        st.error(f"Error: {e}")

        elif operation == "Alter":
            if table_choice == "Customers":
                st.subheader("Alter Customers Table")
                alter_choice = st.radio("Select Alter Operation", ["Add Column", "Drop Column"])

                if alter_choice == "Add Column":
                    column_name = st.text_input("Enter New Column Name")
                    column_type = st.selectbox("Select Column Type", ["VARCHAR(255)", "INT", "FLOAT", "BOOLEAN", "DATE"])
                    if st.button("Add Column"):
                        try:
                            cursor.execute(f"ALTER TABLE Customers ADD COLUMN {column_name} {column_type};")
                            conn.commit()
                            st.success(f"Column '{column_name}' added successfully!")
                        except Error as e:
                            st.error(f"Error: {e}")

                elif alter_choice == "Drop Column":
                    cursor.execute("SHOW COLUMNS FROM Customers;")
                    columns = [row[0] for row in cursor.fetchall()]
                    column_to_drop = st.selectbox("Select Column to Drop", columns)
                    if st.button("Drop Column"):
                        try:
                            cursor.execute(f"ALTER TABLE Customers DROP COLUMN {column_to_drop};")
                            conn.commit()
                            st.success(f"Column '{column_to_drop}' dropped successfully!")
                        except Error as e:
                            st.error(f"Error: {e}")

        cursor.close()
        conn.close()

# Streamlit App Interface
st.title("Zomato Data Insights Project")

menu_options = ["Setup Database", "Generate and Insert Data", "View Table Samples", "CRUD Operations"]
menu_choice = st.sidebar.selectbox("Select an Option", menu_options)

if menu_choice == "Setup Database":
    if st.button("Create Database and Tables"):
        setup_database()

elif menu_choice == "Generate and Insert Data":
    if st.button("Generate and Insert Data"):
        customer_data, restaurant_data, order_data, delivery_data = generate_data()
        insert_data(customer_data, '''INSERT INTO Customers (name, email, phone, location, signup_date, is_premium, preferred_cuisine, total_orders, average_rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);''')
        insert_data(restaurant_data, '''INSERT INTO Restaurants (name, cuisine_type, location, owner_name, average_delivery_time, contact_number, rating, total_orders, is_active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);''')
        insert_data(order_data, '''INSERT INTO Orders (customer_id, restaurant_id, order_date, delivery_time, status, total_amount, payment_mode, discount_applied, feedback_rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);''')
        insert_data(delivery_data, '''INSERT INTO Deliveries (order_id, delivery_status, distance, delivery_time, estimated_time, delivery_fee, vehicle_type) VALUES (%s, %s, %s, %s, %s, %s, %s);''')

elif menu_choice == "View Table Samples":
    table_choice = st.selectbox("Select Table to View", ["Customers", "Restaurants", "Orders", "Deliveries"])
    handle_crud_operations()

elif menu_choice == "CRUD Operations":
    handle_crud_operations()


# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sara@123',  # Update this with your MySQL root password
    'database': 'SAR'  # Update this with your database name
}

# Establish database connection
def create_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG, connection_timeout=300)
        if conn.is_connected():
            return conn
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Execute SQL query and return results as a DataFrame
def fetch_data(query):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return pd.DataFrame(rows, columns=columns)
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
    return pd.DataFrame()

# Home Page
def home_page():
    st.title("Zomato Data Insights Dashboard")
    st.write("Welcome to the Zomato data insights project!")

# MySQL Questions Page
def mysql_questions_page():
    st.title("MySQL CRUD & ALTER Interview Questions")
    st.subheader("20 Essential MySQL Questions & Answers")

    questions_answers = [
        ("Insert a Customer Record", '''INSERT INTO Customers (name, email, phone, location, signup_date, is_premium, preferred_cuisine, total_orders, average_rating) 
        VALUES ('John Doe', 'john.doe@example.com', '9876543210', 'Chennai', '2023-01-01', TRUE, 'Indian', 5, 4.5);'''),

        ("Select All Customers", "SELECT * FROM Customers;"),

        ("Update Customer Phone", "UPDATE Customers SET phone = '9123456789' WHERE customer_id = 1;"),

        ("Delete a Customer Record", "DELETE FROM Customers WHERE customer_id = 1;"),

        ("Add Loyalty Points Column to Customers", "ALTER TABLE Customers ADD loyalty_points INT DEFAULT 0;"),

        ("Insert a Restaurant Record", '''INSERT INTO Restaurants (name, cuisine_type, location, owner_name, average_delivery_time, contact_number, rating, total_orders, is_active) 
        VALUES ('Food Paradise', 'Chinese', 'Bangalore', 'Jane Doe', 30, '9876543222', 4.2, 50, TRUE);'''),

        ("Select All Restaurants", "SELECT * FROM Restaurants;"),

        ("Update Restaurant Rating", "UPDATE Restaurants SET rating = 4.8 WHERE restaurant_id = 1;"),

        ("Delete a Restaurant Record", "DELETE FROM Restaurants WHERE restaurant_id = 1;"),

        ("Rename Owner Name Column in Restaurants", "ALTER TABLE Restaurants CHANGE owner_name manager_name VARCHAR(255);"),

        ("Insert an Order Record", '''INSERT INTO Orders (customer_id, restaurant_id, order_date, delivery_time, status, total_amount, payment_mode, discount_applied, feedback_rating) 
        VALUES (1, 1, '2025-02-01 10:00:00', '2025-02-01 11:00:00', 'Delivered', 500.00, 'Credit Card', 50.00, 5);'''),

        ("Select All Orders", "SELECT * FROM Orders;"),

        ("Update Order Status", "UPDATE Orders SET status = 'In Transit' WHERE order_id = 1;"),

        ("Delete an Order Record", "DELETE FROM Orders WHERE order_id = 1;"),

        ("Add Delivery Notes Column to Orders", "ALTER TABLE Orders ADD delivery_notes TEXT;"),

        ("Drop the Deliveries Table", "SELECT * FROM CUSTOMERS WHERE CUSTOMER_ID=2;")

        
    ]

    for q, a in questions_answers:
        st.markdown(f"*{q}*")
        st.code(a, language="sql")
        
        # Add a "Run Query" button for each query
        if st.button(f"Run Query: {q}"):
            execute_query(a)

# Execute SQL query
def execute_query(query):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            if query.strip().lower().startswith("select"):
                rows = cursor.fetchall()
                if rows:
                    st.dataframe(rows)  # Display results in a table
                else:
                    st.info("No data returned.")
            else:
                conn.commit()
                st.success("Query executed successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

# Define pages
pages = [
    st.Page(home_page, title="Home", icon="🏠"),
    st.Page(mysql_questions_page, title="MySQL CRUD & ALTER Questions", icon="📄"),
]

# Run navigation
pg = st.navigation(pages)
pg.run()