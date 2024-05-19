from dotenv import load_dotenv
import os
import requests
import pandas as pd


load_dotenv()
CARBON_INTERFACE_API_KEY = os.getenv('CARBON_INTERFACE_API_KEY')
url = 'https://www.carboninterface.com/api/v1/estimates'

# FRONT END TO DO: User information to collect at registration:
#     1) Username
#     2) Password
#     3) Own car? If so, make of vehicle
#     4) Diet habit (card profile)
#     5) Country
#     6) State


# DATA INITIALIZATION

# 1) Pandas dataframe for airport codes
airport_codes_df = pd.read_csv('data/airport-codes.csv')

# 2) Dictionary of vehicle makes and vehicle_make_IDs
def vehicle_makes():
    vehicle_makes_dict = {}
    headers = {'Authorization': f'Bearer {CARBON_INTERFACE_API_KEY}'}
    response_json = requests.get('https://www.carboninterface.com/api/v1/vehicle_makes', headers=headers).json()
    for item in response_json:
        vehicle_makes_dict[item['data']['attributes']['name']] = item['data']['id']
    return vehicle_makes_dict
vehicle_makes = vehicle_makes()

def vehicle_models(make):
    vehicle_make_id = vehicle_makes[make]
    vehicle_models_dict = {}
    headers = {'Authorization': f'Bearer {CARBON_INTERFACE_API_KEY}'}
    response_json = requests.get(f'https://www.carboninterface.com/api/v1/vehicle_makes/{vehicle_make_id}/vehicle_models', headers=headers).json()
    for item in response_json:
        vehicle_models_dict[item['data']['attributes']['name']] = item['data']['id']
    return vehicle_models_dict

# 3) Diet habits
diet_habits = ['vegan', 'vegetarian', 'plant_based', 'omnivore']

# 4) Activity types (for carbon calculator and logging activity) - TO-DO: UPDATE THIS AS MORE ACTIVITIES ARE CODED
activity_types = ['flight', 'driving']


# STANDARD HTTP REQUEST
def get_carbon_data(json_data):
    url = 'https://www.carboninterface.com/api/v1/estimates'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {CARBON_INTERFACE_API_KEY}',
    }

    response_json = requests.post(url, headers=headers, json=json_data).json() # returns a dictionary

    carbon_data = {
        'carbon_g': response_json['data']['attributes']['carbon_g'],
        'carbon_lb': response_json['data']['attributes']['carbon_lb'],
        'carbon_kg': response_json['data']['attributes']['carbon_kg'],
        'carbon_mt': response_json['data']['attributes']['carbon_mt'],
    }
    return carbon_data

# VEHICLE CALCULATIONS

# Returns the model id based on the car selected; useful for querying based on rideshares, carpooling, etc.
def get_model_id(make, model):
    make_id = vehicle_makes[make]
    vehicle_models_dict = vehicle_models(make)
    model_id = vehicle_models_dict[model]
    return model_id # returns a string

def calculate_vehicle_footprint(distance_value, make_of_vehicle, model_of_vehicle):
    vehicle_model_id = get_model_id(make_of_vehicle, model_of_vehicle)
    json_data = {
        'type': 'vehicle',
        'distance_unit': 'mi',
        'distance_value': distance_value,
        'vehicle_model_id': vehicle_model_id,
    }
    return get_carbon_data(json_data)


# FLIGHT CALCULATIONS

def get_airport_by_iata(iata_code):
    airport = airport_codes_df[airport_codes_df['iata_code'] == iata_code]
    return airport # returns a pandas dataframe

def calculate_flight_footprint(departure_airport, arrival_airport):
    json_data = {
        'type': 'flight',
        'passengers': '1',
        'legs': [
            {
                'departure_airport': departure_airport,
                'destination_airport': arrival_airport,
            }
        ]
    }
    return get_carbon_data(json_data)

# ELECTRICITY CALCULATIONS
def calculate_electricity_footprint(electricity_unit, electricity_usage, country, state):
    json_data = {
        'type': 'electricity',
        'electricity_unit': electricity_unit,
        'electricity_value': electricity_usage,
        'country': country,
        'state': state
    }
    return get_carbon_data(json_data)


# MONTHLY ACTIVITIES CALCULATIONS
def calculate_monthly_carbon_footprint(month_year, flights, driving_miles, vehicle_make, vehicle_model, electricity_usage, 
                                       kwh_or_mwh, state):
    total_carbon_footprint = 0
    monthly_result = {
        'month-year': month_year,
        'total_carbon_footprint': 0, # 'kg
        'flights': 0,
        'driving': 0,
        'electricity': 0
    }
    if flights:
        individual_flights_footprint = {}
        flights_list = flights.split(',')
        for flight in flights_list:
            departure_airport, arrival_airport = flight.split('-')
            flight_carbon = calculate_flight_footprint(departure_airport, arrival_airport)
            total_carbon_footprint += flight_carbon['carbon_kg']
            individual_flights_footprint[flight] = flight_carbon['carbon_kg'] # Currently not returning this!!
            monthly_result['flights'] += flight_carbon['carbon_kg'] 
    if driving_miles:
        vehicle_carbon = calculate_vehicle_footprint(driving_miles, vehicle_make, vehicle_model)
        total_carbon_footprint += vehicle_carbon['carbon_kg']
        monthly_result['driving'] = vehicle_carbon['carbon_kg']
    if electricity_usage:
        electricity_carbon = calculate_electricity_footprint(kwh_or_mwh, electricity_usage, 'US', state)
        total_carbon_footprint += electricity_carbon['carbon_kg']
        monthly_result['electricity'] = electricity_carbon['carbon_kg']
    monthly_result['total_carbon_footprint'] = total_carbon_footprint
    return monthly_result