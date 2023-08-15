from pymongo import MongoClient
import json
import pandas as pd


client = MongoClient(host='localhost:27017')
db = client['news_classification']


with open('Data/CleanFranchises.json', 'r') as f:
    franchises = [{
        "_id": i+1,
        **v
    }for i, v in enumerate(json.load(f))]
    db['Franchises'].insert_many(franchises)
    


with open('Data/Developers.json', 'r') as f:
    developers = [{
        "_id": i+1,
        **v
    }for i, v in enumerate(json.load(f))]
    db['Companies'].insert_many(developers)