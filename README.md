# 💰 Suvaron - The Smart Expense Tracker

**Suvaron** is a full-stack financial management application built to help users track, categorize, and visualize their daily spending. This project demonstrates a robust implementation of **CRUD operations**, **User Authentication**, and **Data Visualization** using a modern Python web stack.



## 🚀 Features
* **Secure Authentication:** User registration and login system using `Flask-Login` and `Werkzeug` for secure password hashing (PBKDF2).
* **Expense Management:** Full CRUD (Create, Read, Update, Delete) functionality for managing personal transactions.
* **Interactive Analytics:** Dynamic data visualization using `Chart.js`, providing users with a visual breakdown of spending by category (Food, Bills, Transport, etc.).
* **Relational Database:** Designed a structured **MySQL** schema to manage one-to-many relationships between users and their data.
* **Responsive Design:** Clean and modern UI built with **Bootstrap 5**, ensuring accessibility across all devices.

## 🛠️ Tech Stack
* **Backend:** Python (Flask)
* **Database:** MySQL
* **ORM:** SQLAlchemy
* **Frontend:** HTML5, CSS3, JavaScript (Chart.js), Bootstrap 5
* **Environment:** Python-dotenv (Secure credential management)

## 📂 Project Structure
```text
expense_tracker/
│
├── app.py              # Application factory & Route handling
├── models.py           # Database Schema (User & Expense)
├── static/             # CSS styling and JS logic
├── templates/          # Jinja2 Templates (Base, Dashboard, Login, Register)
├── .env                # Secret environment variables (Excluded from Git)
├── .gitignore          # File to ignore venv/ and .env during commits
└── requirements.txt    # List of project dependencies
