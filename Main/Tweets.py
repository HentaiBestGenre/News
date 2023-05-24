import re


class Tweet:
    def __init__(self, pos, tweet, **kwargs):
        self.pos = pos
        self.tweet_src = tweet['data-src']
        self.author = re.findall(r'(\(@.+?\))', tweet.text)[-1][1:-1]
        self.date = tweet.select('a')[-1].text
        for i in tweet.select('a'):
            i.extract()
        for br in tweet.p.find_all("br"):
            br.replace_with("\n")
        self.text = tweet.p.text

    def json(self):
        return {
            'position': self.pos,
            'author': self.author,
            'tweet_src': self.tweet_src,
            'text': self.text,
            'date': self.date,
        }

    def __str__(self):
        return f"""author - {self.author} tweet_src - {self.tweet_src}"""

    def __repr__(self):
        return f"""author = {self.author}
tweet_src = {self.tweet_src}
text = \"{self.text}\"
date = {self.date}"""
