# TIS FINAL PROJECT - SPRING 2024 
Author: Tithi Raval

## Description
This project is an MVP of a monthly carbon footprint tracker and calculator that helps users understand, predict, and manage their carbon emissions from key carbon emitting activities (driving, flying, and electricity). This project can be extended into package tracking, purchase tracking, and other use cases.

## Getting Started
### Dependencies
Dependencies are detailed in the `requirements.txt` to facilitate easy installation.
- Python 3.6+
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF

### Installation
To install this project on your local machine, follow the below instructions:
1. Log into Github from your terminal 
2. Navigate to where you want to host the project and clone the repository: 
    git clone https://github.com/traval0/TIS-final-project-Spring2024
3. Ensure you are in the project directory. Install required projects by copying/pasting this code into the terminal: 
    pip install -r requirements.txt
4. Initalize the database: 
    flask db upgrade
5. Run the application using one of the below run options:
    python3 app.py, or
    flask run
6. If successful, the terminal will provide a local host like (http://127.0.0.1:5000/). Click on or navigate to this host to access the website.

## Author
Tithi Raval - traval0@uchicago.edu

## Acknowledgements
- Thank you Professor Chelsea Troy and TA June Cong with all the support on this project
- Carbon Interface API for backend carbon footprint calculations
- Miguel Grinber's Flask Mega-Tutorial
- Julian Nash's tutorial on Flask messaging
- Chart.js for dashboard visuals
- ChatGPT assisted with troubleshooting help


