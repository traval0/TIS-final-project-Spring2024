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
# print(vehicle_makes)

def vehicle_models(make):
    # print(vehicle_makes)
    vehicle_make_id = vehicle_makes[make]
    vehicle_models_dict = {}
    headers = {'Authorization': f'Bearer {CARBON_INTERFACE_API_KEY}'}
    response_json = requests.get(f'https://www.carboninterface.com/api/v1/vehicle_makes/{vehicle_make_id}/vehicle_models', headers=headers).json()
    for item in response_json:
        vehicle_models_dict[item['data']['attributes']['name']] = item['data']['id']
    return vehicle_models_dict
# print(vehicle_models('db5875e5-4986-44c5-aabc-02bbfa78c282'))


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
    print(response_json)

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
    # print(make_of_vehicle)
    vehicle_model_id = get_model_id(make_of_vehicle, model_of_vehicle)
    print(f"Make of vehicle: {make_of_vehicle}, Make of vehicle: {model_of_vehicle}, Model ID: {vehicle_model_id}")
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


# TESTING - everything below works!!
# print(calculate_vehicle_footprint(10, '7268a9b7-17e8-4c8d-acca-57059252afe9'))
# print(get_vehicle_models())
# print(vehicles_dict)
# get_airport_by_iata('JFK')
# print(get_model_id_by_make('Tesla'))
# print(calculate_flight_footprint('JFK', 'LAX')) 
# # print(calculate_vehicle_footprint(10, '1c2a69d5-54d3-4796-a424-ffbdf8b538d1'))
# print(calculate_vehicle_footprint(10, 'Volvo'))
# print(get_model_id('Tesla', 'Model S'))
# print(vehicle_makes['Tesla'])
# print(vehicle_models('Tesla'))


