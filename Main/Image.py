import requests
from Main.Config import HEADERS, IMAGES_DIR
import os


class Image:
    def __init__(self, pos, image, **kwargs):
        self.pos = pos
        if image.name == "figure":
            self.image_url = image['data-img-src']
        elif image.name == "div":
            self.image_url = image.find('img')['src']
        else:
            raise Exception("Wrong tag")

        image_bytes = requests.get(self.image_url, headers=HEADERS).content
        folder = kwargs.get("article_id")
        if folder is None:
            folder = 'unrecognized'

        self.image_path = self.image_url.split('/')[-1]

        if not os.path.exists(IMAGES_DIR / folder):
            os.makedirs(IMAGES_DIR / folder)
        with open(IMAGES_DIR / folder / self.image_path, 'wb') as f:
            f.write(image_bytes)

    def json(self):
        return {
            'position': self.pos,
            'image_url': self.image_url,
        }

    def __str__(self):
        return f"""image_url: {self.image_url}"""

    def __repr__(self):
        return f"""image_url = {self.image_url}"""


class ImageGallery:
    def __init__(self, pos, gallery):
        self.pos = pos
        self.images = [Image(None, i) for i in gallery.findAll('div', class_='image-gallery__item')[:-1]]
        self.gallery_length = len(self.images)

    def json(self):
        return {
            'positions': self.pos,
            'images': self.get_images_json(),
            'len': self.gallery_length
        }

    def get_images_json(self):
        return [i.json() for i in self.images]

    def __str__(self):
        return f"""images: {self.images}, len: {self.gallery_length}"""

    def __repr__(self):
        return f"""images = {self.images}; len = {self.gallery_length};"""
