from urllib.parse import urlparse
from dataclasses import dataclass


@dataclass
class Text:
    isTitle: bool
    text: str
    pos: int | None = None

    def __init__(self, text):
        self.text: str = text.text.strip()
        self.isTitle: bool = False if text.name == "p" else True

        self.__post_init__()

    def __post_init__(self):
        if self.text == '':
            raise ValueError('Text should not be empty string')


class Tag:
    def __init__(self, tag):
        self.value: str = tag.text.strip()


@dataclass
class Ul:
    lis: list[str]
    len: int
    pos: int | None = None

    def __init__(self, ul):
        self.lis: list[str] = [Li(i) for i in ul.findAll('li')]
        self.len: int = len(self.lis)

        self.__post_init__()

    def __post_init__(self):
        if len(self.lis) == 0:
            raise ValueError('Lis len is 0')
        

@dataclass
class Li:
    value: str
    isLink: bool = False
    href: str | None = None

    def __init__(self, data):
        self.value = data.text
        if (link := data.find('a')) is not None:
            parsed = urlparse(link['href'])
            self.href = f"{parsed[0]}://{parsed[1]}{parsed[2]}"
            self.isLink = True
