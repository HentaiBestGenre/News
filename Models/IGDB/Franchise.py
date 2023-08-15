from pydantic import BaseModel


class AlternativeName(BaseModel):
    aggregated_rating: int
    aggregated_rating_count: int


class Game(BaseModel):
    name: str
    alternative_names: list[AlternativeName]
    aggregated_rating: int
    aggregated_rating_count: int


class Franchise(BaseModel):

    checksum: int
    created_at: int
    games: list[Game]
    name: str
    slug: str
    updated_at: str
    url: str
