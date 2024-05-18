from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import desc
from flask_migrate import Migrate
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from models import db, User, UserProfile, MonthlyCarbonData
from forms import LoginForm, RegisterForm, CreateProfileForm, FlightActivityForm, VehicleActivityForm, LogMonthlyActivitiesForm, ElectricityActivityForm
import calculations as calc
from dotenv import load_dotenv
import os
from flask_bcrypt import Bcrypt
from datetime import datetime

load_dotenv()

CARBON_INTERFACE_API_KEY = os.getenv('CARBON_INTERFACE_API_KEY')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)  # Initialize db with the app
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'thisisasecretkey'

with app.app_context():
    # db.drop_all()   # Uncomment to reset the tables
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
                                   model_of_vehicle=form.model_of_vehicle.data, state=form.state.data)
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
    monthly_data = get_monthly_data(current_user.id)
    labels = [month[0].strftime("%Y-%m") for month in monthly_data]
    data = [month[1]['total_carbon_footprint'] for month in monthly_data] 
    # this_month_data = get_this_months_data(current_user.id)
    this_month_labels = ['flights_carbon_total_kg', 'driving_carbon_total_kg', 'electricity_carbon_total_kg']
    latest_month = get_latest_month_data(current_user.id)
    latest_month_chart_data = [latest_month['flights_carbon_total_kg'], latest_month['driving_carbon_total_kg'], 
                               latest_month['electricity_carbon_total_kg']]
    print(get_latest_month_data(current_user.id))
    print(this_month_labels)
    print(latest_month_chart_data)
    return render_template("dashboard.html", username=current_user.username, labels=labels, data=data, 
                           monthly_data=monthly_data, this_month_data=latest_month_chart_data, this_month_labels=this_month_labels)

def get_monthly_data(input_user_id):
    monthly_data_list = []   # list of tuples where 1st element is month_year and 2nd element is dictionary of monthly results
    monthly_data = MonthlyCarbonData.query.filter_by(user_id=input_user_id).all()
    for month in monthly_data:
        # month_dict = {}
        # month_dict['flights'] = month.flights
        # month_dict['driving_miles'] = month.driving_miles
        # month_dict['electricity_usage'] = month.electricity_usage
        # month_dict['kwh_or_mwh'] = month.kwh_or_mwh
        # month_dict['flights_carbon_total_kg'] = month.flights_carbon_total_kg
        # month_dict['driving_carbon_total_kg'] = month.driving_carbon_total_kg
        # month_dict['electricity_carbon_total_kg'] = month.electricity_carbon_total_kg
        # month_dict['total_carbon_footprint'] = month.total_carbon_footprint
        # monthly_data_list.append((month.month_year, month_dict))
        monthly_data_list.append((month.month_year, monthly_carbon_to_dict(month)))
    return monthly_data_list

def monthly_carbon_to_dict(monthly_carbon_data):
    month_dict = {}
    month_dict['flights'] = monthly_carbon_data.flights
    month_dict['driving_miles'] = monthly_carbon_data.driving_miles
    month_dict['electricity_usage'] = monthly_carbon_data.electricity_usage
    month_dict['kwh_or_mwh'] = monthly_carbon_data.kwh_or_mwh
    month_dict['flights_carbon_total_kg'] = monthly_carbon_data.flights_carbon_total_kg
    month_dict['driving_carbon_total_kg'] = monthly_carbon_data.driving_carbon_total_kg
    month_dict['electricity_carbon_total_kg'] = monthly_carbon_data.electricity_carbon_total_kg
    month_dict['total_carbon_footprint'] = monthly_carbon_data.total_carbon_footprint
    return month_dict

def get_this_months_data(input_user_id):
    today = datetime.today()
    this_month = datetime(today.year, today.month, 1)
    monthly_data = MonthlyCarbonData.query.filter_by(user_id=input_user_id, month_year=this_month).first()
    if monthly_data:
        return monthly_carbon_to_dict(monthly_data)
    else:
        return None

def get_latest_month_data(input_user_id):
    latest_month_data = MonthlyCarbonData.query.filter_by(user_id=input_user_id).order_by(
        desc(MonthlyCarbonData.month_year)).first()    
    return monthly_carbon_to_dict(latest_month_data)

@app.route('/carbon_calculator', methods=['GET', 'POST'])   
def carbon_calculator():
    return render_template("carbon_calculator.html")

@app.route('/carbon_calculator/flight_calculator', methods=['GET', 'POST'])   
def flight_calculator():
    form = FlightActivityForm()
    if form.validate_on_submit():
        departure_airport = form.departure_airport.data
        arrival_airport = form.arrival_airport.data
        response = calc.calculate_flight_footprint(departure_airport, arrival_airport)
        print(response)
    return render_template("flight_calculator.html", form=form)

@app.route('/carbon_calculator/vehicle_calculator', methods=['GET', 'POST'])   
def vehicle_calculator():
    form = VehicleActivityForm()
    if form.validate_on_submit():
        distance = form.distance.data
        number_of_passengers = form.number_of_passengers.data    # What to do with this?
        make = form.make_of_vehicle.data
        model = form.model_of_vehicle.data
        response = calc.calculate_vehicle_footprint(distance, make, model)
        print(response)
        # FIX THIS
        flash(f"Your carbon footprint from this activity: {response['carbon_kg']} kg")
        # return render_template("vehicle_calculator.html", form=form, carbon_data=carbon_data)
    return render_template("vehicle_calculator.html", form=form)

@app.route('/carbon_calculator/electricity_calculator', methods=['GET', 'POST'])   
def electricity_calculator():
    form = ElectricityActivityForm()
    if form.validate_on_submit():
        electricity_usage = form.electricity_usage.data
        kwh_or_mwh = form.kwh_or_mwh.data
        # NEED TO UPDATE THIS TO GET STATE AND COUNTRY INFO FROM USER PROFILE TABLE
        response = calc.calculate_electricity_footprint(kwh_or_mwh, electricity_usage, "US", "IL")
        print(response)
    return render_template("electricity_calculator.html", form=form)

@app.route('/log_activities', methods=['GET', 'POST'])   
def log_activities():
    form = LogMonthlyActivitiesForm()
    if form.validate_on_submit():
        month_year = form.month_year.data
        flights = form.flights.data
        driving_miles = form.driving_miles.data
        electricity_usage = form.electricity_usage.data
        kwh_or_mwh = form.kwh_or_mwh.data

        # # GET DEFAULT DATA FROM USER PROFILE - done
        default_data = get_default_data(current_user.id)
        state = default_data['state']
        vehicle_make = default_data['vehicle_make']
        vehicle_model = default_data['vehicle_model']

        # CALCULATE THE CARBON FOOTPRINT FOR ALL ACTIVITIES - done
        carbon_footprint_results_dict = calc.calculate_monthly_carbon_footprint(month_year, flights, driving_miles, vehicle_make, 
                                                                           vehicle_model, electricity_usage, kwh_or_mwh, state)
        
        # ADD TO DATABASE TO BE ABLE TO TRACK OVER TIME - done
        monthly_data = MonthlyCarbonData(user_id=current_user.id, 
                                            user=current_user, 
                                            month_year=month_year, 
                                            flights=flights, 
                                            driving_miles=driving_miles, 
                                            electricity_usage=electricity_usage, 
                                            kwh_or_mwh=kwh_or_mwh,
                                            flights_carbon_total_kg=carbon_footprint_results_dict['flights'],
                                            driving_carbon_total_kg=carbon_footprint_results_dict['driving'],
                                            electricity_carbon_total_kg=carbon_footprint_results_dict['electricity'],
                                            total_carbon_footprint=carbon_footprint_results_dict['total_carbon_footprint']
                                        )
        db.session.add(monthly_data)
        db.session.commit()

        # TO-DO: Figure out how to display the results
    return render_template("log_activities.html", form=form)

def get_default_data(input_user_id):
    state = UserProfile.query.with_entities(UserProfile.state).filter_by(user_id=input_user_id).first()
    make = UserProfile.query.with_entities(UserProfile.make_of_vehicle).filter_by(user_id=input_user_id).first()
    model = UserProfile.query.with_entities(UserProfile.model_of_vehicle).filter_by(user_id=input_user_id).first()
    result = {
        'state': state[0],
        'vehicle_make': make[0],
        'vehicle_model': model[0]
    }
    return result


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)


