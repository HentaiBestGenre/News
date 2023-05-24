class Text:
    def __init__(self, pos, text, **kwargs):
        self.pos = pos
        self.isTitle = False if text.name == "p" else True
        self.text = text.text.strip()

    def json(self):
        return {
            'position': self.pos,
            'isTitle': self.isTitle,
            'text': self.text,
        }

    def __repr__(self):
        return f"isTitle = {self.isTitle}\ntext = {self.text}"

    def __str__(self):
        return f"{self.text}"


class Tag:
    def __init__(self, tag, **kwargs):
        self.value = tag.text.strip()

    def json(self):
        return {
            'value': self.value,
        }

    def __repr__(self):
        return f'vale = {self.value}'

    def __str__(self):
        return f'{self.value}'


class Ul:
    def __init__(self, pos, ul, **kwargs):
        self.pos = pos
        self.lis = [i.text for i in ul.findAll('li')]
        self.len = len(self.lis)

    def json(self):
        return {
            'position': self.pos,
            'lis': self.lis,
            'len': self.len,
        }

    def __str__(self):
        return f"""lis: {self.lis}, len: {self.len}"""

    def __repr__(self):
        return f"""position = {self.pos}; lis = {self.lis}; len = {self.len}"""
