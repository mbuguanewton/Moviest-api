import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(verbose=True)
MONGO_URI = os.getenv('MONGODB_URI')


client = MongoClient(MONGO_URI,connect=False, connectTimeoutMS=40000)
cursor = client.get_database('movie_data')
