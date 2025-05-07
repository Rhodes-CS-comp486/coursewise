Coursewise: The Wise Way to Choose Courses
Project Description
Coursewise is a web-based platform that utilizes historical enrollment data to predict future course demand, helping students, departments, and administrators make informed decisions about course selection and offering. The application addresses the common problem of overwhelming course demand and insufficient resources to anticipate that demand accurately.
Our solution empowers:
Students to create class schedules that satisfy degree requirements by providing insights into their likelihood of getting into specific courses
Departments to predict course demand and make data-driven decisions about course offerings, seat allocation, and professor assignments
Administrators to set effective guidelines and mitigate issues between student needs and department resources
Key Features
Personalized Likelihood Prediction based on:
Professor demand history
Class year enrollment patterns
Student's declared major
Historical course demand data
Data-Driven Decision Making tools for faculty and administration
Course Planning Tools that help students stay on track with degree requirements
Resource Allocation Insights for departments to optimize course offerings
Bottleneck Identification for academic program improvements
 
Our application follows the standard Django architecture:
Frontend: User interface and data visualization components
Backend: API server built with Django, handling business logic and predictions
Database: SQLite storage for historical enrollment data from multiple sources

Project Dependencies
Software Libraries
Python: General programming language
Django: Web development framework for backend and frontend connection
SQLite: Database backend for storing and querying enrollment data
Runtime Environment
PyCharm
Backend Services and Products
Database:
SQLite 
Data Sources:
CSV files from primary course demand page
Files from Registrar's office with detailed enrollment information
Course catalog data (prerequisites and current offerings)
Quick Start Guide
Installation Instructions
Local Installation			
Clone the repository: 
	Clone the repository using VCS option on Pycharm/Python IDE or use ‘git clone’ in the terminal
Ex: git clone https://github.com/Rhodes-CS-comp486/coursewise.git


Create/activate a virtual environment


Install dependencies:
Install the following packages through your Python IDE
Django
asgiref
pip
psycopg
setuptools
sqlparse
typing-extensions
wheel


Run Instructions
Local Development Server
Ensure your virtual environment is activated
Start the development server
Access the application at http://localhost:8000
	- Run the program and access the link
