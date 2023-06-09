import re
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Tweet:
    tweet_src: str
    author: str
    date: datetime
    pos: int | None = None

    def __init__(self, tweet):
        self.tweet_src: str = tweet['data-src']
        self.author: str = re.findall(r'(\(@.+?\))', tweet.text)[-1][1:-1]
        self.date: datetime = tweet.select('a')[-1].text
        
        for i in tweet.select('a'):
            i.extract()
        for br in tweet.p.find_all("br"):
            br.replace_with("\n")
        self.text: str = tweet.p.text
