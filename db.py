from pymongo import MongoClient


DB_NAME = "v-luminat"

DB_HOST = "mongodb+srv://waqas-jani:waqas786_@cluster0-elnjz.mongodb.net/v-luminat?retryWrites=true&w=majority"
DB_PORT = ""
DB_USER = "waqas-jani"
DB_PASS = "waqas786_"

connection = MongoClient(DB_HOST)
# db = connection.resumas
db = connection[DB_NAME]
# db.authenticate()