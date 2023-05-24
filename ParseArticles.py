import json

from bs4 import BeautifulSoup as bs
import requests
from pymongo import MongoClient, ASCENDING
import time

from Main.Data.Models.DBClient import get_session
from Main.Data.Models.Models import ArticleHeader
from Main import Article

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"}
session, _ = get_session()
repo = session.query(ArticleHeader)
errors = {}


def get_article(_id, url, page, commit=False):
    soup = bs(page, features="html.parser")
    try:
        article = Article(_id, url, soup).json()
        if commit:
            client = MongoClient("mongodb://root:password@localhost:27017")
            db = client["news_classification"]
            db["GameSpotArticles"].insert_one(article)
        print(f"=========================\n{_id}:\t{True}\n=========================")
        return article
    except Exception as e:
        print(f"=========================\n{_id}\n{e}\n=========================")
        errors[str(_id)] = e.__repr__()


def parse_from_web(_id, url, commit=False, write=False):
    page = requests.get("https://www.gamespot.com" + url, headers=headers).content
    if write:
        with open(f"{_id}.html", 'wb') as f:
            f.write(page)
        return
    get_article(_id, url, page, commit=commit)


def parse_from_file(fn, commit=False):
    with open(fn, 'r') as f:
        get_article(_id=0, url='', page=f, commit=commit)


def parse_all():
    article_headers = repo.all()
    for article_header in article_headers:
        parse_from_web(article_header.id, article_header.url, commit=True)
        if article_header.id % 100 == 0:
            time.sleep(300)


def parse_one(_id, write=False, commit=False):
    article_header = repo.get(_id)
    parse_from_web(article_header.id, article_header.url, write=write, commit=commit)


def parse_many(ids, commit=False):
    for i in ids:
        parse_one(i, commit=commit)


def parse_by_url(url, write=False):
    parse_from_web(_id=0, url=url, write=write)


def write_log():
    with open("errors.json", 'w') as f:
        json.dump(errors, f)


if __name__ == "__main__":
    pass
    # _ids = [40, 69, 74, 143, 280, 297, 298, 361, 380, 426, 512, 665, 721]
    # parse_many(_ids, commit=True)
    # _id = 721
    # parse_one(_id, write=True)
    # parse_from_file(f"{_id}.html")
    # parse_all()
    # write_log()

