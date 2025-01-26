from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bcrypt

# MongoDB connection URI
uri = "mongodb+srv://joyceyouu:OOISu8HkaOAeRQgE@cluster0.ky6x6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
database = client["joyceyouu"]
collection = database["users"]
@app.route('/')
def home():
    return redirect(url_for('register_page'))

@app.route('/createacc', methods=['POST'])
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        data = request.json
        username = data.get("username").strip()
        password = data.get("password").strip()

        # Retrieve user from the database
        user = collection.find_one({"username": username})
        if not user:
            return jsonify({"success": False, "message": "Invalid username or password."}), 401

        # Verify the password
        if bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            session['username'] = username
            return jsonify({"success": True, "message": "Login successful!"}), 200
        else:
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
# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print("Connection error:", e)
#     exit()

# try:
#     # Access database and collection
#     database = client["joyceyouu"]
#     collection = database["users"]  # Changed collection name to 'users'

#     # Get account details from the user
#     username = input("Enter username: ").strip()
#     password = input("Enter password: ").strip()

#     # Check for duplicate username
#     if collection.find_one({"username": username}):
#         print("Error: Username already exists. Please choose a different username.")
#     else:
#         # Hash the password for security
#         hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#         # Insert new user into the database
#         result = collection.insert_one({
#             "username": username,
#             "password": hashed_password.decode('utf-8')  # Store hashed password as a string
#         })

#         if result.acknowledged:
#             print("Account created successfully!")
#         else:
#             print("Failed to create account.")

#     # Close the database connection
#     client.close()
# except Exception as e:
#     print("An error occurred:", e)