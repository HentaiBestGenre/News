from dataclasses import dataclass


@dataclass
class Image:
    image_url: str
    image_path: str
    pos: int | None = None

    def __init__(self, image):
        if image.name == "figure":
            self.image_url = image['data-img-src']
        elif image.name == "div":
            self.image_url = image.find('img')['src']
        else:
            raise Exception("Image URL did not found")
        self.image_path: str = self.image_url.split('/')[-1]


    # def wright_image(self, article_id=None):
    #     image_bytes = requests.get(self.image_url, headers=HEADERS).content
    #     if article_id is None:
    #         article_id = "unrecognized"

    #     if not os.path.exists(IMAGES_DIR / article_id):
    #         os.makedirs(IMAGES_DIR / article_id)
    #     with open(IMAGES_DIR / article_id / self.image_path, 'wb') as f:
    #         f.write(image_bytes)


# class ImageGallery:
#     def __init__(self, gallery, pos=None):
#         self.pos = pos
#         self.images = [Image(None, i) for i in gallery.findAll('div', class_='image-gallery__item')[:-1]]
#         self.gallery_length = len(self.images)

#     def json(self):
#         return {
#             'positions': self.pos,
#             'images': self.get_images_json(),
#             'len': self.gallery_length
#         }

#     def get_images_json(self):
#         return [i.json() for i in self.images]

#     def __str__(self):
#         return f"""images: {self.images}, len: {self.gallery_length}"""

#     def __repr__(self):
#         return f"""images = {self.images}; len = {self.gallery_length};"""
