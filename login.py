from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bcrypt

# MongoDB connection URI
uri = "mongodb+srv://joyceyouu:OOISu8HkaOAeRQgE@cluster0.ky6x6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Connection error:", e)
    exit()

try:
    # Access database and collection
    database = client["joyceyouu"]
    collection = database["users"]  # Changed collection name to 'users'

    # Get account details from the user
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    # Check for duplicate username
    if collection.find_one({"username": username}):
        print("Error: Username already exists. Please choose a different username.")
    else:
        # Hash the password for security
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert new user into the database
        result = collection.insert_one({
            "username": username,
            "password": hashed_password.decode('utf-8')  # Store hashed password as a string
        })

        if result.acknowledged:
            print("Account created successfully!")
        else:
            print("Failed to create account.")

    # Close the database connection
    client.close()
except Exception as e:
    print("An error occurred:", e)
