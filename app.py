from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from models import db, User, UserProfile
from forms import LoginForm, RegisterForm, CreateProfileForm, FlightActivityForm, VehicleActivityForm 
import calculations as calc
from dotenv import load_dotenv
import os
import requests
from flask_bcrypt import Bcrypt

load_dotenv()

CARBON_INTERFACE_API_KEY = os.getenv('CARBON_INTERFACE_API_KEY')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)  # Initialize db with the app
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'thisisasecretkey'

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')   
@app.route('/<user>')   # can have multiple routes to the same function
def index(user=None):
    # return render_template('user.html', user=user)
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])   
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])   
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('create_profile'))
    return render_template('register.html', form=form)

@app.route('/createprofile', methods=['GET', 'POST'])  
@login_required 
def create_profile():
    form = CreateProfileForm()
    if form.validate_on_submit():
        # Add user profile information to user_profile database
        user_profile = UserProfile(user_id=current_user.id, user=current_user, birthday=form.birthday.data, 
                                   number_in_household=form.number_in_household.data, diet_habit=form.diet_habit.data, 
                                   own_car=form.own_car.data, make_of_vehicle=form.make_of_vehicle.data, 
                                   model_of_vehicle=form.model_of_vehicle.data)
        db.session.add(user_profile)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('create_profile.html', form=form)

@app.route('/profile/<username>')   # variable name here is the same one we want to pass into the function; if not using string, have to specify
def profile(username):
    return render_template("profile.html", username=username)

@app.route('/dashboard', methods=['GET', 'POST'])   
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.username)

# @app.route('/test', methods=['GET', 'POST'])   
# def test():
#     form = MainForm()
#     return render_template("test.html", form=form)

@app.route('/carbon_calculator', methods=['GET', 'POST'])   
def carbon_calculator():
    return render_template("carbon_calculator.html")

@app.route('/flight_calculator', methods=['GET', 'POST'])   
def flight_calculator():
    form = FlightActivityForm()
    if form.validate_on_submit():
        departure_airport = form.departure_airport.data
        arrival_airport = form.arrival_airport.data
        response = calc.calculate_flight_footprint(departure_airport, arrival_airport)

    return render_template("flight_calculator.html", form=form)

@app.route('/vehicle_calculator', methods=['GET', 'POST'])   
def vehicle_calculator():
    form = VehicleActivityForm()
    if form.validate_on_submit():
        distance = form.distance.data
        number_of_passengers = form.number_of_passengers.data    # What to do with this?
        make = form.make_of_vehicle.data
        model = form.model_of_vehicle.data
        response = calc.calculate_vehicle_footprint(distance, make, model)
        flash(f"Your carbon footprint from this activity: {response['carbon_kg']} kg")
        # return render_template("vehicle_calculator.html", form=form, carbon_data=carbon_data)
    return render_template("vehicle_calculator.html", form=form)

@app.route('/log_activity', methods=['GET', 'POST'])   
def log_activity():
    return render_template("log_activity.html")

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

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


