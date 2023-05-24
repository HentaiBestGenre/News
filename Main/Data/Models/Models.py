from sqlalchemy import String, DateTime, Column, Integer
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

from .DBClient import get_engine


Base = declarative_base()


class ArticleHeader(Base):
    __tablename__ = "GamesSpotArticles"

    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    url = Column(String(256))
    image_url = Column(String(256))
    date = Column(DateTime)

    def __init__(self, title, url, image_url, date):
        super().__init__()
        self.title = title
        self.url = url
        self.image_url = image_url
        self.date = datetime.strptime(date, '%A, %b %d, %Y %I:%M%p')

    def to_json(self) -> dict:
        return {
            "_id": self.id,
            "title": self.title,
            "url": self.url,
            "image_url": self.image_url,
            "date": self.date
        }

    def __repr__(self) -> str:
        return f"GamesSpotArticle(\n\t{self.title}\n\t{self.url}\n\t{self.image_url}\n\t{self.date}\n)"


def init_db():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
