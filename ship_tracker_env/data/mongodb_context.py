from pymongo import MongoClient
from data.db_connection.connection_data import Connection_Data

def create_connection_with_mongodb():
    client = MongoClient(Connection_Data.CONNECTION_STRING)
    db = client[Connection_Data.DATABASE_NAME]
    return db

def get_the_tracking_collection(db):
    collection = db[Connection_Data.TRACKING_COLLECTION]
    return collection