# from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
# from typing import Optional
# import sqlalchemy as sa
# import sqlalchemy.orm as so
# from app import db, app

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    profile = db.relationship('UserProfile', back_populates='user', uselist=False, cascade="all, delete-orphan")
    # activity = db.relationship('Activity', back_populates='user')  
    monthly_carbon_data = db.relationship('MonthlyCarbonData', back_populates='user', uselist=False, cascade="all, delete-orphan")

class UserProfile(db.Model, UserMixin):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', back_populates='profile')
    birthday = db.Column(db.DateTime)
    number_in_household = db.Column(db.Integer)
    diet_habit = db.Column(db.String(30))
    own_car = db.Column(db.Boolean)
    make_of_vehicle = db.Column(db.String(80))
    model_of_vehicle = db.Column(db.String(80))
    state = db.Column(db.String(2))


class MonthlyCarbonData(db.Model, UserMixin):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User')
    month_year = db.Column(db.DateTime)
    flights = db.Column(db.String(100))
    driving_miles = db.Column(db.Float)
    electricity_usage = db.Column(db.Float)
    kwh_or_mwh = db.Column(db.String(3))
    flights_carbon_total_kg = db.Column(db.Float)
    driving_carbon_total_kg = db.Column(db.Float)
    electricity_carbon_total_kg = db.Column(db.Float)
    total_carbon_footprint = db.Column(db.Float)


# # OLD MODEL WHEN I WAS PLANNING TO DO DAILY ACTIVITY LOGGING
# class Activity(db.Model, UserMixin):
#     activity_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship('User', back_populates='activity')
#     flight_activity = db.relationship('FlightActivity', back_populates='activity')
#     vehicle_activity = db.relationship('VehicleActivity', back_populates='activity')

#     # TO-DO: WOULD CARBON EMISSIONS DATA GO HERE OR AT THE DETAILED LEVEL? I THINK HERE

# class FlightActivity(db.Model, UserMixin):
#     flight_activity_id = db.Column(db.Integer, primary_key=True)
#     activity_id = db.Column(db.Integer, db.ForeignKey('activity.activity_id'))
#     activity = db.relationship('Activity', back_populates='flight_activity')
#     departure_airport = db.Column(db.String(3), nullable=False)
#     arrival_airport = db.Column(db.String(3), nullable=False)

# class VehicleActivity(db.Model, UserMixin):
#     vehicle_activity_id = db.Column(db.Integer, primary_key=True)
#     activity_id = db.Column(db.Integer, db.ForeignKey('activity.activity_id'))
#     activity = db.relationship('Activity', back_populates='vehicle_activity')

