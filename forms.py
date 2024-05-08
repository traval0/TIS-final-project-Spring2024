from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField, DateField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError
from models import User
from calculations import vehicles_dict, diet_habits, activity_types

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=20)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField('Register')
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

class CreateProfileForm(FlaskForm):
    birthday = DateField('Enter Your Birthday')
    number_in_household = IntegerField('Number of people in your household')
    diet_habit = SelectField('Diet Habit', choices=diet_habits)
    own_car = BooleanField('I own a car')
    make_of_vehicle = SelectField('Make of Vehicle', choices=vehicles_dict.keys())
    submit = SubmitField('Complete Profile')

class FlightForm(FlaskForm):
    departure_airport = StringField('Departure Airport (3 letter code)', validators=[InputRequired(), Length(min=3, max=3)])
    arrival_airport = StringField('Arrival Airport (3 letter code)', validators=[InputRequired(), Length(min=3, max=3)])
    calculate = SubmitField('Calculate Carbon Footprint')
    log_activity = SubmitField('Log This Activity')
    

class VehicleForm(FlaskForm):
    distance = IntegerField('How many miles did you drive', validators=[InputRequired()])
    number_of_passengers = IntegerField('How many passengers were in the vehicle?', validators=[InputRequired()])
    make_of_vehicle = SelectField('Make of Vehicle', choices=vehicles_dict.keys())
    calculate = SubmitField('Calculate Carbon Footprint')
    log_activity = SubmitField('Log This Activity')

