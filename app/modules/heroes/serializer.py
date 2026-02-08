from pydantic import BaseModel, Field


class HeroResponse(BaseModel):
    id: str
    name: str
    type: str
    difficulty: str


class HeroCreateRequest(BaseModel):
    name: str = Field(min_length=1)
    type: str = Field(min_length=1)
    difficulty: str = Field(min_length=1)


class HeroUpdateRequest(BaseModel):
    name: str | None = Field(None, min_length=1)
    type: str | None = Field(None, min_length=1)
    difficulty: str | None = Field(None, min_length=1)
