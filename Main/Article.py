from Main.Image import Image  # , ImageGallery
from Main.Text import Text, Tag, Ul
from Main.Tweets import Tweet
from Main.Videos import YoutubeVideo, GamespotVideo
from bs4 import BeautifulSoup as bs


class Article:
    def __init__(self, article_id, url, page):
        self.article_id = article_id
        self.url = url
        self.json_data = {
            "_id": article_id,
            "url": url,
            "title": None,
            "len": 0,
            "text": [],
            "image": [],
            "tweet": [],
            "youtube": [],
            "gamespot_video": [],
            # "gallery": [],
            "ul": [],
            "tag": [],
        }
        self.deconstruct_page(page)

    def json(self):
        return self.json_data

    def deconstruct_page(self, soup: bs):
        article = soup.find('article')

        #  get article title, tags, body
        if (title := article.find("section", {'class': ['news-hdr']}).h1) is not None:
            self.json_data['title'] = title.text
        elif (title := soup.find("h1", {'class': ['kubrick-info__title']})) is not None:
            self.json_data['title'] = title.text
        else:
            raise Exception("Title did not found")
        
        tags = article.findAll("div", class_='horizontal-list__item-gap')
        self.json_data['tag'] = [Tag(tag).json() for tag in tags]
        article = article.find("section", {'class': ['article-body']}).find('div')

        # delete ad
        for i in article.select('div.js-mapped-ad'):
            i.extract()

        article = article.findAll(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'figure', 'div'], recursive=False)

        counter = 0
        article_length = len(article)
        for i in article:
            name = i.name
            type_ = i['data-embed-type'] if i.has_attr("data-embed-type") else None
            element = None

            match name:
                case "p" | "h1" | "h2" | "h3" | "h4" | "h5" | "h6":
                    if i.text.strip() == '':
                        continue
                    element = (Text, 'text')
                case "ul":
                    element = (Ul, 'ul')
                case "figure":
                    element = (Image, 'image')
                case "div":
                    match type_:
                        case 'tweet':
                            element = (Tweet, 'tweet')
                        case 'video':
                            element = self._get_video(i)
                        # case 'imageGallery':
                        #     element = (ImageGallery, 'gallery')
                        case None:
                            if i.has_attr('class') and 'article-related-video' in i['class']:
                                element = (GamespotVideo, 'gamespot_video')
            if element is None:
                continue

            self._add_element(element, counter, i)
            counter += 1
        self.json_data["len"] = counter

    @staticmethod
    def _get_video(video):
        if video.find("iframe"):
            return (YoutubeVideo, 'youtube')
        return (GamespotVideo, 'gamespot_video')


    def _add_element(self, element: tuple[object, str], index, value):
        element_type, element_name = element
        self.json_data[element_name].append(element_type(index, value, article_id=str(self.article_id)).json())

    def __repr__(self):
        return self.json_data
