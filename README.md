# TIS FINAL PROJECT - SPRING 2024 
Author: Tithi Raval

## Description
This project is an MVP of a monthly carbon footprint tracker and calculator that helps users understand, predict, and manage their carbon emissions from key carbon emitting activities (driving, flying, and electricity). The goal is that this project integrates into a user's monthly review process along with reviewing finances, health goals, etc. This project can be extended into package tracking, purchases tracking, and other use cases available within the Carbon Interface API and other APIs. 

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
1. Sign up for a Carobn Interface API here: https://docs.carboninterface.com/#/?id=introduction
2. Test the API with the instructions listed here: https://docs.carboninterface.com/#/?id=authentication 
3. Navigate to where you want to host the project and clone the repository: 
    git clone https://github.com/traval0/TIS-final-project-Spring2024
4. Ensure you are in the main project directory (same level as app.py). Create a .env file and copy/paste the following line with your API key.
    CARBON_INTERFACE_API_KEY = "YOUR KEY HERE"
5. Create a virtual environment:
    python3 -m venv <myenvname>
6. Install required projects by copying/pasting this code into the terminal: 
    pip install -r requirements.txt
6. Initalize the database: 
    flask db upgrade
7. Run the application using one of the below run options:
    python3 app.py, or
    flask run
8. If successful, the terminal will provide a local host like (http://127.0.0.1:5000/). Click on or navigate to this host to access the website.

## Files
- app.py - the main project file where flask is run from. This file contains all the routing between pages and coordination between the front-end, database tables, and charts.
- calculations.py - this file contains all of the modules to call the Carbon Interface API and calculate carbon footprint results.
- models.py - this file defines the tables for the SQLAlchemy databases.
- forms.py - this file defines the forms to be used in the front-end webpages.
- templates/ - HTML templates that are the user interface of this project.
- static/ - CSS file for overall styling of the website.

## Author
Tithi Raval - traval0@uchicago.edu

## Acknowledgements
- Thank you Professor Chelsea Troy and TA June Cong with all the support on this project
- Carbon Interface API for backend carbon footprint calculations
- Miguel Grinber's Flask Mega-Tutorial
- Julian Nash's tutorial on Flask messaging
- Chart.js for dashboard visuals
- ChatGPT assisted with troubleshooting help