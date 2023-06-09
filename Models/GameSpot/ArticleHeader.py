from dataclasses import dataclass 
from datetime import datetime


@dataclass
class ArticleHeader:
    title: str
    url: str
    image_url: str
    date: datetime

    def __init__(self, body, image) -> None:
        self.title = body.a.h4.text
        self.url = body.a['href']
        self.image_url = image.img['src']
        self.date = datetime.strptime(body.div.time['datetime'], '%A, %b %d, %Y %I:%M%p')

        self.__post_init__()

    def __post_init__(self):
        if not isinstance(self.title, str):
            raise TypeError('Title should be of type str')
        if not isinstance(self.url, str):
            raise TypeError('URL should be of type str')
        if not isinstance(self.image_url, str):
            raise TypeError('image_url should be of type str')
        if not isinstance(self.date, datetime):
            raise TypeError('date should be of type datetime')
