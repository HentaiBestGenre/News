from pymongo import MongoClient
import json

client = MongoClient("localhost", 27017)
texts = client['news_classification']['Texts']

with open("/home/vadim/Projects/news_classifire/Data/cleanArticles.json", 'r') as f:
    data = json.load(f)

data = [[json.loads(k) for k in i['tokenized_text'] ] for i in data]
# texts.insert_many(data)
