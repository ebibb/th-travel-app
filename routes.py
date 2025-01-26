# from flask import Flask, render_template
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
app.secret_key = secrets.token_hex(32)

# Configure CORS with specific origins and methods
CORS(app, resources={
    r"/createacc": {
        "origins": ["http://127.0.0.1:5500", "http://localhost:5500"],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

CORS(app, resources={
    r"/login": {
        "origins": ["http://127.0.0.1:5500", "http://localhost:5500"],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# MongoDB connection
uri = "mongodb+srv://joyceyouu:OOISu8HkaOAeRQgE@cluster0.ky6x6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
database = client["joyceyouu"]
collection = database["users"]

@app.route('/')
def home():
    return redirect(url_for('register_page'))

@app.route('/createacc', methods=['GET', 'POST'])
def register_page():
    if request.method == 'GET':
        return render_template('createacc.html')
    elif request.method == 'POST':
        try:
            data = request.json  # Parse JSON from the frontend
            username = data.get("username", "").strip()
            password = data.get("password", "").strip()
            age = data.get("age")
            people = data.get("people")
            kids = data.get("kids")
            activities = data.get("activities")
            geo = data.get("geo")

            # Check if username already exists
            if collection.find_one({"username": username}):
                return jsonify({"success": False, "message": "Username already exists."}), 400

            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insert user into the database
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
        except Exception as e:
            return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


# @app.route('/login', methods=['GET', 'POST', 'OPTIONS'])
# def login():
#     if request.method == 'OPTIONS':
#         # Handle CORS preflight request
#         response = jsonify(success=True)
#         response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:5500')
#         response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#         response.headers.add('Access-Control-Allow-Methods', 'POST')
#         return response

#     if request.method == 'GET':
#         return render_template('login.html')
#     else:
#         data = request.json
#         username = data.get("username", "").strip()
#         password = data.get("password", "").strip()

#         # Retrieve user from the database
#         user = collection.find_one({"username": username})
#         if not user:
#             return jsonify({"success": False, "message": "Invalid username or password."}), 401

#         # Verify the password
#         if bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
#             session['username'] = username
#             return jsonify({"success": True, "message": "Login successful!"}), 200
#         return jsonify({"success": False, "message": "Invalid username or password."}), 401

# Existing MongoDB and login route code remains the same
@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:5500')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data received."}), 400

    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    user = collection.find_one({"username": username})
    if not user:
        return jsonify({"success": False, "message": "Invalid username or password."}), 401

    if bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
        session['username'] = username
        return jsonify({"success": True, "message": "Login successful!"}), 200

    return jsonify({"success": False, "message": "Invalid username or password."}), 401

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return f"Welcome, {session['username']}! <a href='/logout'>Logout</a>"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
