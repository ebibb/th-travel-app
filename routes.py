# from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bcrypt
# app = Flask(__name__)

# # two decorators, same function
# @app.route('/')
# def index():
#     return render_template('home.html', the_title='Tiger Home Page')

# @app.route('/symbol.html')
# def symbol():
#     return render_template('symbol.html', the_title='Tiger As Symbol')

# @app.route('/myth.html')
# def myth():
#     return render_template('myth.html', the_title='Tiger in Myth and Legend')

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bcrypt
from flask_cors import CORS
import os
import secrets


app = Flask(__name__)

load_dotenv()

API_KEY = os.environ.get("TRIP_ADVISOR_API_KEY")

URL = "https://api.content.tripadvisor.com/api/v1/location/search"
URLIMG = "https://api.content.tripadvisor.com/api/v1/location/locationId/photos"
URLRVW = "https://api.content.tripadvisor.com/api/v1/location/locationId/reviews"

# two decorators, same function

uri = "mongodb+srv://joyceyouu:OOISu8HkaOAeRQgE@cluster0.ky6x6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
database = client["joyceyouu"]
collection = database["users"]
@app.route('/')
def index():
    return render_template('home.html', the_title='Tiger Home Page')

# @app.route('/profile')
# def profile():
#     return render_template('profile.html', the_title='Tiger Home Page')

@app.route('/createnewacc', methods=['POST'])
def register_page():
    data = request.json
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    age = data.get("age")
    people = data.get("people")
    kids = data.get("kids")
    activities = data.get("activities")
    geo = data.get("geo")

    # Check for duplicate username
    if collection.find_one({"username": username}):
        return jsonify({"success": False, "message": "Username already exists."}), 400

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert new user into the database
    result = collection.insert_one({
        "username": username,
        "password": hashed_password.decode('utf-8'),
        "age": age,
        "people": people,
        "kids": kids,
        "activities": activities,
        "geo": geo,
    })

    if result.acknowledged:
        return jsonify({"success": True, "message": "Account created successfully!"}), 201
    return jsonify({"success": False, "message": "Failed to create account."}), 500


@app.route('/city')
def city():
    # city search ##################
    search_info = request.args.get('q')
    
    params = {
        'key': API_KEY,
        'searchQuery': search_info,
        'category': "attractions",
        'language': 'en'
    }
    
    res = requests.get(URL, params=params)
    results_data = res.json()
    
    # img search ####################
    
    # params_id = {
    #     'locationId': 
    #     'key': API_KEY,
    #     'language': 'en',
    #     'limit': '1',
    #     'offset': '0'
    # }
    
    location_id = []
    for i in results_data.get('data'):
        location_id.append(i.get('location_id'))
        
    
        
    
    # reviews search
    
    return render_template('city.html', results=results_data)

BASE_URL = 'https://aa-api-edbb11e7d431.herokuapp.com/'
AIRPORTS_BASE = '/airports?code=<code>'

@app.route('/airport')
def airport():
    res = requests.get(BASE_URL + AIRPORTS_BASE.replace('<code>', 'DFW'))
    results_data = res.json()
    
    return results_data





@app.route('/profile.html')
def profile():
    return render_template('profile.html', the_title='profile')

@app.route('/myth.html')
def myth():
    return render_template('myth.html', the_title='Tiger in Myth and Legend')

@app.route('/createacc.html')
def createacc():
    return render_template('createacc.html', the_title='Acccount Creation')



if __name__ == '__main__':
    app.run(debug=True)
