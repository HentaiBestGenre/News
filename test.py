# from pymongo import MongoClient
# import json
# import pandas as pd


# from pymongo import MongoClient, DESCENDING
# import json
# import pandas as pd
# import requests

# HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"}
# mongo_client = MongoClient("mongodb://localhost:27017")
# db = mongo_client["news_classification"]

# page, res = 1, []
# end = db['GameSpotHeaders'].find({}).sort('_id', DESCENDING)[0]

# while page < 6:
#     headers = requests.get(f"http://localhost:8000/parse/gamespot/get/headers/page/{page}", headers=HEADERS)
#     if headers.status_code != 200:
#         raise Exception("request Error: ", json.loads(headers.content))
#     headers: list = json.loads(headers.content)

#     coincidences = list(filter(lambda x: x['title'] == end['title'] or x['url'] == end['url'], headers))
#     if len(coincidences):
#         res = list(reversed(headers[:headers.index(coincidences[0])])) + res
#         break
#     else:
#         res = list(reversed(headers)) + res
#     page += 1

# res = [{"_id": end['_id']+i+1, **v}for i, v in enumerate(res)]
# with open('/tmp/new_headers.json', 'w') as f:
#     json.dump(res, f)


from pymongo import MongoClient
import json
import pandas as pd
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

from pymongo import MongoClient, DESCENDING
import json
import pandas as pd
import numpy as np
import requests


client = MongoClient("localhost", 27017)
games = list(client['news_classification']['Games'].find({}))
platforms = list(client['news_classification']['Platforms'].find({}))
companies = list(client['news_classification']['Companies'].find({}))
tags = client['news_classification']['Tags']


def prepare_tokens(v):
    v = v.lower()
    tokens = word_tokenize(v)
    if len(list(filter(lambda x: x['value'] == v, games))):
        t = "game"
    elif len(list(filter(lambda x: x['value'] == v, platforms))):
        t = "platform"
    elif len(list(filter(lambda x: x['value'] == v, companies))):
        t = 'company'
    else:
        return None
    return {"type": t, "value": v, "tokens": tokens, "l": len(tokens)}

articles = client['news_classification']['GameSpotArticles']
article_tags = []
for i in articles.find({}):
    article_tags += [k['value'] for k in i['tags']]
article_tags = np.unique(article_tags)

tokens = [token for i in article_tags if (token := prepare_tokens(i)) is not None]
tags.insert_many(tokens)


# client = MongoClient("localhost", 27017)
# texts = client['news_classification']['Tags']

# with open("/home/vadim/Projects/news_classifire/Data/Tags.json", 'r') as f:
#     data = json.load(f)
# tokens = list(map(lambda x: {
#     "title": x['title'],
#     "value": x['value'],
#     "tokens": x['tokens'],
#     "l": x['l']
# }, data))

# a = [{"_id": i[0]+1, **i[1]} for i in enumerate(list({v['title']:v for v in tokens}.values()))]
# print('')