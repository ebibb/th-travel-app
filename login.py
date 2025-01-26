
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://joyceyouu:OOISu8HkaOAeRQgE@cluster0.ky6x6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB! haha")


except Exception as e:
    print(e)

try:
    database = client["joyceyouu"]
    collection = database["j"]
    # start example code here
    result = collection.insert_one({ "<field name>" : "<value>" })

    print(result.acknowledged)

    # end example code here
    client.close()
except Exception as e:
    raise Exception(
        "The following error occurred: ", e)

