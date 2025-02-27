from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

client = MongoClient("mongodb+srv://stark:stark@unvexed.mkdmnkj.mongodb.net/")

try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("Connected successfully!!!")
except ConnectionFailure as e:
    print(f"Could not connect to MongoDB: {e}")
    exit(1)

db = client["AIVALD"]
accounts = db["ACCOUNTS"]
subjects = db["SUBJECTS"]
students = db["STUDENTS"]
