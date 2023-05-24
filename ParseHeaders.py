from bs4 import BeautifulSoup as bs
import requests

from Main.Data.Models.DBClient import get_session
from Main.Data.Models.Models import ArticleHeader

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"}
session, _ = get_session()


def parse_urls(page):
    host = "https://www.gamespot.com/news/"
    url = host + f"?page={page}"
    r = requests.get(url, headers=headers)
    soup = bs(r.content, features="html.parser")
    return soup


def pars_headers():
    for i in range(1, 21):
        articles = parse_urls(i)
        articles = articles.findAll('div', class_='card-item')

        for image, body in articles:
            article = {
                'title': body.a.h4.text,
                'url': body.a['href'],
                'image_url': image.img['src'],
                'date': body.div.time['datetime']
            }
            article = ArticleHeader(
                article["title"],
                article["url"],
                article["image_url"],
                article["date"]
            )
            try:
                session.add(article)
            except Exception as e:
                print(article.__repr__())
                print("\n==========================================================\n")
    session.commit()


if __name__ == "__main__":
    pars_headers()
