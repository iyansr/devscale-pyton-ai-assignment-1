from pydantic import BaseModel, Field

from app.modules.heroes.serializer import HeroResponse


class PlayerResponse(BaseModel):
    id: str
    username: str
    rank: str
    favourite_heroes: list[HeroResponse] = []


class PlayerCreateRequest(BaseModel):
    username: str = Field(min_length=1)
    rank: str = Field(min_length=1)


class PlayerUpdateRequest(BaseModel):
    username: str | None = Field(None, min_length=1)
    rank: str | None = Field(None, min_length=1)


class AddFavouriteHeroRequest(BaseModel):
    hero_id: str = Field(min_length=1)
