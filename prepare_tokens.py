import nltk
nltk.download('punkt')
from pymongo import MongoClient
import numpy as np
import json
import pandas as pd
from nltk.tokenize import word_tokenize


client = MongoClient('localhost', port=27017)
db = client['news_classification']
articles_coll = db['GameSpotArticles']
tags_coll = db['Tags']

with open("./Developers.json", 'r') as f:
    Developers = json.load(f)
with open("./games.json", 'r') as f:
    games = json.load(f)
with open("./Publishers.json", 'r') as f:
    Publishers = json.load(f)

def prepare_tokens(v):
    v = v.lower()
    tokens = tuple(word_tokenize(v))
    return {"value": v, "tokens": tokens, "l": len(tokens)}

games = [{f"type": "game", **prepare_tokens(v)} for v in games]
developers = [{f"type": "company", **prepare_tokens(v)} for v in Developers]
Publishers = [{f"type": "company", **prepare_tokens(v)} for v in Publishers]
print(games)
tags = pd.DataFrame(games + developers + Publishers)
tags = tags.drop_duplicates(keep='first')
print(tags.head())
tags = tags.sort_values('l')

tags = tags.to_json(orient="records")
tags = json.loads(tags)

with open("./tags.json", 'w') as f:
    json.dump(tags, f)

tags_coll.insert_many(tags)