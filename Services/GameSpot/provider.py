from fastapi.exceptions import HTTPException
import requests


class Provider:
    host = "https://www.gamespot.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"
        }

    def get_news_page(self, page: int):
        url = self.host + f"/news?page={page}"
        r = requests.get(url, headers=self.headers)
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=r.reason)
        return r

    def get_article_page(self, article_url):
        url = self.host + article_url
        r = requests.get(url, headers=self.headers)
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=r.reason)
        return r