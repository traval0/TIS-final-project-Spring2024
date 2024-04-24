from flask import Flask
from dotenv import load_dotenv
import os
import requests


load_dotenv()

CARBON_INTERFACE_API_KEY = os.getenv('CARBON_INTERFACE_API_KEY')

app = Flask(__name__)

# routing URL on website to a home page
@app.route('/')   
def index():
    return 'This is the home page'


if __name__ == "__main__":   # We only start the webserver when this file is called directly
    app.run(debug=True)   # This starts the app


    #testing updates
