Student Management System A simple Flask + SQLite web application for managing student records with user authentication. This project allows users to register, log in, add, edit, delete, and view students, as well as access student data via an API.

Features

User authentication (Register, Login, Logout)
Add new students (Name, Age, Course)
View all students in a table
Edit student details
Delete student records
REST API endpoint to fetch student data in JSON format
SQLite database integration
Session-based login system
Tech Stack

Backend: Flask (Python)
Database: SQLite
Frontend: HTML (Jinja2 templates)
API: JSON response using Flask’s jsonify
Installation & Setup

Clone the repository git clone https://github.com/your-username/student-management-flask.git cd student-management-flask
Create a virtual environment (optional but recommended) python -m venv venv source venv/bin/activate # On Linux/Mac venv\Scripts\activate # On Windows
Install dependencies pip install flask
Run the application python app.py
Open in browser http://127.0.0.1:5000/
