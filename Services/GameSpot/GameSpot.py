from .parser import Parser
from .provider import Provider


class Gamespot:    
    def __init__(self) -> None:
        self.parser = Parser()
        self.provider = Provider()

    def get_news_page(self, page: int):
        r = self.provider.get_news_page(page)
        return self.parser.pars_news_page(r.content)

    def get_article_page(self, article_url):
        r = self.provider.get_article_page(article_url)
        return self.parser.pars_article(article_url, r.content)
