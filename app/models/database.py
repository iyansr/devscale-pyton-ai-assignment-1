from cuid2 import cuid_wrapper
from sqlmodel import Field, Relationship, SQLModel

cuid = cuid_wrapper()


class PlayerFavouriteHero(SQLModel, table=True):
    player_id: str = Field(foreign_key="players.id", primary_key=True)
    hero_id: str = Field(foreign_key="heroes.id", primary_key=True)


class Heroes(SQLModel, table=True):
    id: str = Field(default_factory=cuid, primary_key=True)
    name: str
    type: str
    difficulty: str


class Players(SQLModel, table=True):
    id: str = Field(default_factory=cuid, primary_key=True)
    username: str
    rank: str
    favourite_heroes: list["Heroes"] = Relationship(
        link_model=PlayerFavouriteHero
    )
