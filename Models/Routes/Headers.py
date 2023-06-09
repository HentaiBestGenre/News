from pydantic import BaseModel, Field
from datetime import datetime


class LastArticle(BaseModel):
    title: str = Field(...)
    url: str = Field(...)
    date: datetime = Field(...)
