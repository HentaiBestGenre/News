import requests
import pymongo
import json
import time


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"}
mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
db = mongo_client["news_classification"]


pages = 200
article_id = 1
while pages != 0:

    article_headers = requests.get(f"http://localhost:8000/parse/gamespot/get/headers/page/{pages}", headers=headers)
    if article_headers.status_code != 200:
        print("Error:\n", article.content)
        pages -= 1
        continue
    article_headers = json.loads(article_headers.content)[-1::-1]
    for i in article_headers:
        try:
            i["_id"] = article_id
            db['GameSpotHeaders'].insert_one(i)

            article = requests.get(f"http://localhost:8000/parse/gamespot/get/article?url={i['url']}")
            if article.status_code != 200:
                print("Error:\n", article.content)
                continue
            article = json.loads(article.content)
            article['_id'] = article_id
            db['GameSpotArticles'].insert_one(article)

            article_id += 1
        except Exception as e:
            print(f"==========================\n{e}\n==========================")
    pages -= 1
    time.sleep(2*60)
