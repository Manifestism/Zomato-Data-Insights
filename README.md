## Zomato Data Insights Project 🍴📊

This project is a Streamlit-based web application that manages and analyzes data for Zomato-like food delivery services. It leverages MySQL for database operations and Faker for generating synthetic data, providing insights and CRUD operations for customers, restaurants, orders, and deliveries.

---

## 🚀 Features

- *Database Setup*: Automated creation of tables for Customers, Restaurants, Orders, and Deliveries.  
- *Data Generation*: Insert synthetic data using the Faker library for testing and analysis.  
- *CRUD Operations*: Perform Create, Read, Update, and Delete operations on all database tables.  
- *Custom Table Alterations*: Add or drop columns dynamically from tables.  
- *Interactive Data View*: Display table samples in a user-friendly format.  

---

## 📋 Project Structure

```bash
📁 Zomato_Data_Insights
├── app.py             # Main Streamlit application
├── requirements.txt    # Dependencies file
└── README.md           # Project Documentation
💻 Tech Stack
Frontend: Streamlit
Backend: MySQL
Data Simulation: Faker
Programming Language: Python
🔧 Setup Instructions
Clone the Repository:

bash
Copy
Edit
git clone https://github.com/your_username/zomato-data-insights.git
cd zomato-data-insights
Install Dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Configure MySQL Database:

Update the DB_CONFIG dictionary in app.py with your MySQL credentials.

python
Copy
Edit
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sara@123',
    'database': 'zomoto'
}
Run the Application:

bash
Copy
Edit
streamlit run app.py
Explore the App:

Setup the database
Generate and insert synthetic data
Perform CRUD operations
View table samples
📊 Sample Data Tables
Customers	Restaurants	Orders	Deliveries
200	200	200	200
🔍 Future Enhancements
Add data visualization for insights into order trends and customer preferences
Implement user authentication and role-based access
Enhance delivery tracking with GPS-based simulation
Add real-world datasets for better insights
🤝 Contributions
Contributions are welcome! Please fork the repository and create a pull request for any feature additions or bug fixes.

📜 License
This project is licensed under the MIT License.

📬 Contact
Author: Sarala Varadharajan
Email: saralav91@gmail.com
