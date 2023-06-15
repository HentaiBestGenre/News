from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

from Services import Gamespot


router = APIRouter()
gamespot_client = Gamespot()


@router.get("")
def index():
    return "Hello world!"

@router.get("/get/headers/page/{page}", description="Parse an headers form a gamespot news page")
def get_article(page: int):
    try:
        headers = gamespot_client.get_news_page(page=page)
        return JSONResponse(status_code=200, content=jsonable_encoder(headers))
    except Exception as e:
        return HTTPException(status_code=500, detail=e)

@router.get("/get/article", description="Parse a new article by article url")
def get_article_queue(url):
    try:
        new_article = gamespot_client.get_article_page(url)
        return JSONResponse(status_code=200, content=jsonable_encoder(new_article))
    except Exception as e:
        return HTTPException(status_code=500, detail=e)