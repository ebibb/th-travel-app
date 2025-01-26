from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bcrypt

# MongoDB connection URI
uri = "mongodb+srv://joyceyouu:OOISu8HkaOAeRQgE@cluster0.ky6x6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

# Flask app
app = Flask(__name__)

# Database setup
database = client["joyceyouu"]
collection = database["users"]  # Collection for user data

@app.route('/create-account', methods=['POST'])
def create_account():
    try:
        # Get data from the form
        data = request.form
        username = data.get("username").strip()
        password = data.get("password").strip()
        full_name = data.get("name").strip()
        email = data.get("email").strip()
        age = int(data.get("age").strip())
        people = int(data.get("people").strip())
        kids = data.get("kids").strip().lower()
        activities = data.get("activities").strip().lower()

        # Check if username already exists
        if collection.find_one({"username": username}):
            return jsonify({"error": "Username already exists"}), 400

        # Hash the password for security
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create user document with profile information
        user_document = {
            "username": username,
            "password": hashed_password.decode('utf-8'),  # Store hashed password as a string
            "profile": {
                "full_name": full_name,
                "email": email,
                "age": age,
                "people": people,
                "kids": kids,
                "activities": activities
            }
        }

        # Insert the user into the database
        result = collection.insert_one(user_document)

        if result.acknowledged:
            return jsonify({"message": "Account created successfully"}), 201
        else:
            return jsonify({"error": "Failed to create account"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
