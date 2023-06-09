from dataclasses import dataclass, field


from .Image import Image  # , ImageGallery
from .Text import Text, Tag, Ul
from .Tweets import Tweet
from .Videos import YoutubeVideo, GamespotVideo


class Article:

    def __init__(self, url: str, title: str):
        self.url: str = url
        self.title: str = title
        self.length: int = 0
        self.text: list[Text] = []
        self.ul: list[Ul] = []
        self.image: list[Image] = []
        self.tweet: list[Tweet] = []
        self.youtube: list[YoutubeVideo] = []
        self.gamespot_video: list[GamespotVideo] = []
        self.tags: list[Tag] = []

        self.__post_init__()

    def __post_init__(self):
        if not isinstance(self.url, str):
            raise TypeError(f'URL should be of type str, not {type(self.url)}')
        if not isinstance(self.title, str):
            raise TypeError(f'Title should be of type str, not {type(self.title)}')
        
    def set_tags(self, tag: list | Tag):
        if type(tag) == Tag:
            tag = [tag]
        self.tags = list(set(self.tags + tag))

    def __call__(self, prop:str, value):
        value.pos = self.length
        self.length += 1
        self.__dict__[prop].append(value)
