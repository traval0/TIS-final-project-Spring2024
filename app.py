from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from models import db, User
from forms import LoginForm, RegisterForm
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


# routing URL on website to a login & signup page
@app.route('/')   
@app.route('/<user>')   # can have multiple routes to the same function
def index(user=None):
    # return render_template('user.html', user=user)
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])   
def login():
    form = LoginForm()
    # print(form.validate_on_submit())
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
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# features - dashboard, calculator, log
@app.route('/home')   
def home():
    return 'This is the home page with dashboard, calculator, & log'

# routing URL on website to a profile page
@app.route('/myprofile')   
def myprofile():
    return 'This is my profile page'

# routing URL on website to a specific user profile
@app.route('/profile/<username>')   # variable name here is the same one we want to pass into the function; if not using string, have to specify
def profile(username):
    return render_template("profile.html", username=username)

# routing URL on website to a dashboard
@app.route('/dashboard', methods=['GET', 'POST'])   
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.username)

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


