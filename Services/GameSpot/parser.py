from bs4 import BeautifulSoup as bs


from Models.GameSpot import Article, Text, Ul, Image, Tweet, YoutubeVideo, GamespotVideo, Tag, ArticleHeader


class Parser:    
    def pars_news_page(self, page) -> list:
        soup = bs(page, features="html.parser")
        articles = soup.findAll('div', class_='card-item')
        res = []  # founded news article headers
        for image, body in articles:
            header = ArticleHeader(body, image)
            res.append(header)
        return res
    
    def pars_article(self, url, page) -> Article:
        soup = bs(page, features="html.parser")
        body = soup.find('article')

        #  get article title
        if (title := body.find("section", {'class': ['news-hdr']}).h1) is not None:
            title = title.text
        elif (title := soup.find("h1", {'class': ['kubrick-info__title']})) is not None:
            title = title.text
        else:
            raise Exception("Title did not found")
        
        article = Article(url, title)
        self.__fill_up_articles(article, body)
        return article

    def __fill_up_articles(self, article: Article, body) -> None:
        # get body tags
        tags = body.findAll("div", class_='horizontal-list__item-gap')
        article.set_tags([Tag(tag) for tag in tags])
        
        # get article body
        body = body.find("section", {'class': ['article-body']}).find('div')
        # delete ad
        for i in body.select('div.js-mapped-ad'):
            i.extract()

        body = body.findAll(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'figure', 'div'], recursive=False)
        for i in body:
            name = i.name
            type_ = i['data-embed-type'] if i.has_attr("data-embed-type") else None

            match name:
                case "p" | "h1" | "h2" | "h3" | "h4" | "h5" | "h6":
                    if i.text.strip() == '':
                        continue
                    article("text", Text(i))
                case "ul" | 'ol':
                    article('ul', Ul(i))
                case "figure":
                    article('image', Image(i))
                case "div":
                    match type_:
                        case 'tweet':
                            article('tweet', Tweet(i))
                        case 'video':
                            if i.find("iframe"):
                                article('youtube', YoutubeVideo(i))
                            else:
                                article('gamespot_video', GamespotVideo(i))
                        case None:
                            if i.has_attr('class') and 'article-related-video' in i['class']:
                                article('gamespot_video', GamespotVideo(i))
                            else:
                                continue
                        case _: 
                            continue
                case _: 
                    continue
                