from flask import Flask, request, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from forms import LoginForm, RegisterForm
from dotenv import load_dotenv
import os
import requests


load_dotenv()

CARBON_INTERFACE_API_KEY = os.getenv('CARBON_INTERFACE_API_KEY')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app) 
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = 'thisisasecretkey'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

with app.app_context():
    db.create_all()

# routing URL on website to a login & signup page
# features - login, signup
@app.route('/')   
@app.route('/<user>')   # can have multiple routes to the same function
def index(user=None):
    # return render_template('user.html', user=user)
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])   
def login():
    form = LoginForm()
    print(form.validate_on_submit())
    return render_template('login.html', form=form)

@app.route('/register')   
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)

# routing URL on website to a home page
# features - dashboard, calculator, log
@app.route('/home')   
def home():
    return 'This is the home page with dashboard, calculator, & log'

@app.route('/test', methods=['GET', 'POST'])   # need to specify POST because default is GET
def test():
    if request.method == 'POST':
        return 'This is a POST request'
    else:
        return 'This is a GET request'
    #return f'Method used: {request.method}'
    #return 'This is the home page with dashboard, calculator, & log'

# routing URL on website to a profile page
@app.route('/myprofile')   
def myprofile():
    return 'This is my profile page'

# routing URL on website to a specific user profile
@app.route('/profile/<username>')   # variable name here is the same one we want to pass into the function; if not using string, have to specify
def profile(username):
    return render_template("profile.html", username=username)

# routing URL on website to a dashboard
@app.route('/dashboard')   
def dashboard():
    return 'This is my dashboard'

def calculate_carbon_footprint(CARBON_INTERFACE_API_KEY, activity_type, activity_value):
    url = "https://www.carboninterface.com/api/v1/estimates"
    headers = {
        "Authorization": f"Bearer {CARBON_INTERFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "type": "vehicle",
        "attributes": {
            "vehicle_model_id": activity_type,  # Adjust based on actual usage
            "distance_value": activity_value,
            "distance_unit": "mi",
            "fuel_efficiency_unit": "mpg"
        }
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

if __name__ == "__main__":   # We only start the webserver when this file is called directly
    app.run(debug=True)   # This starts the app


