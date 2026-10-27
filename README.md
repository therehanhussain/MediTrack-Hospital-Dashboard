# MediTrack – Hospital Patient Management System

MediTrack is a college project built to understand how SQL and Python can work together to manage hospital information. It started as a MySQL database project and was extended into an interactive dashboard using Streamlit.

The main idea is simple: keep patient, doctor, appointment, prescription, and billing information organized in one database, then make that information easier to explore through a dashboard.

## Project Overview

The project uses **MySQL** to store and manage data and **Python with Streamlit** to display it through a simple web interface.

The dashboard reads the existing MediTrack database and presents its records in tables, summary metrics, and charts. It is designed as a beginner-friendly project that demonstrates database management, SQL queries, and basic data visualization.

## Technologies Used

- **MySQL** – Relational database and SQL queries
- **Python** – Application logic and database connectivity
- **Streamlit** – Interactive web dashboard
- **Pandas** – Data handling and tabular display
- **mysql-connector-python** – Connection between Python and MySQL

## Database Structure

The original project contains five main tables:

| Table | Purpose | Original Records |
|---|---|---:|
| `Patients` | Patient details and contact information | 20 |
| `Doctors` | Doctor profiles, specializations, fees, and experience | 15 |
| `Appointments` | Patient appointments, dates, doctors, and status | 10 |
| `Prescriptions` | Medicines and prescription details linked to appointments | 13 |
| `Billing` | Bill amounts, payment methods, and payment status | 10 |

The project also includes a `Departments` table as an extension for organizing doctors by specialization.

Primary keys and foreign-key relationships help connect related records across the database.

## Dashboard Features

### 1. Hospital Overview
- Displays total patients, doctors, appointments, and prescriptions.
- Shows the total billing amount.
- Visualizes appointment status and payment methods.

### 2. Patient Management
- View patient records from MySQL.
- Search using patient name, ID, email, or contact information.

### 3. Doctors and Departments
- View doctor profiles and specializations.
- Explore department information and doctor assignments.
- Display the number of doctors by specialization.

### 4. Appointment Management
- View appointment records.
- Filter appointments by status.
- Review appointment history.

### 5. Prescription Records
- View the existing prescription data, including medicine, dosage, and duration.

### 6. Billing and Payments
- View bills and payment methods.
- Calculate total billed and paid amounts.
- Display outstanding balances when the relevant columns are available.

## SQL Concepts Demonstrated

The database project explores practical SQL concepts, including:

- Database and table creation
- Primary and foreign keys
- Table relationships and joins
- Filtering, sorting, grouping, and aggregate functions
- Subqueries and reporting queries
- Indexes and views
- Transactions and rollback
- Data integrity checks
- Department management and appointment scheduling queries
- Billing and payment-balance calculations

## Project Structure

The dashboard repository contains:

```text
MediTrack-Hospital-Dashboard/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

- `app.py` – Streamlit dashboard and MySQL connection logic.
- `requirements.txt` – Python packages required to run the dashboard.
- `README.md` – Project documentation.
- `.gitignore` – Excludes selected temporary and sensitive files from Git.

The original SQL scripts are maintained separately in the MediTrack SQL project folder. They include the database schema and data, department management, appointment scheduling, billing improvements, management reports, and testing queries.

## Getting Started

### Prerequisites

Before running the dashboard, make sure you have:

- Python installed
- MySQL Server installed and running
- The existing `MediTrack` database created in MySQL Workbench
- The required database tables available

### 1. Clone the repository

```bash
git clone https://github.com/therehanhussain/MediTrack-Hospital-Dashboard.git
cd MediTrack-Hospital-Dashboard
```

### 2. Install the dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Start the dashboard

```bash
python -m streamlit run app.py
```

Streamlit should open the application in your browser, usually at:

```text
http://localhost:8501
```

### 4. Connect to MySQL

Enter your MySQL connection details in the dashboard sidebar:

- Host: `localhost`
- Port: `3306` (or your configured MySQL port)
- Username: your MySQL username
- Password: your MySQL password
- Database: `MediTrack`

Click **Connect to MediTrack** to load the existing records.

## Data Integrity

The dashboard is intended to read the existing database. It does not insert, update, or delete records.

The original dataset contains 20 patients, 15 doctors, 10 appointments, 13 prescriptions, and 10 bills. The original billing amounts total 6,800.00 in the database's stored amount units.

No additional patient, doctor, appointment, prescription, or billing records are intentionally created by the dashboard.

## Learning Outcomes

Building this project helped me practice:

- Designing and querying a relational database
- Connecting Python applications to MySQL
- Displaying database records in a web interface
- Creating charts and summary metrics from real database data
- Organizing a project into manageable files
- Using Git and GitHub to maintain and share source code

## Future Improvements

Some features that could be added in future versions include:

- More advanced search and filtering
- CSV export for reports
- Improved dashboard styling and light/dark themes
- Better database error handling
- Role-based access and authentication
- More detailed appointment and revenue analytics

## Author

**MD Rehan Hussain**

GitHub: [@therehanhussain](https://github.com/therehanhussain)


This project was developed as a learning exercise to apply SQL, Python, database connectivity, and dashboard development to a practical hospital-management use case.
