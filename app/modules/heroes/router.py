from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, func, select

from app.core.schema import PaginatedResponse, Pagination, Response
from app.models.database import Heroes
from app.models.engine import get_db
from app.modules.heroes.serializer import (
    HeroCreateRequest,
    HeroResponse,
    HeroUpdateRequest,
)
from app.utils.query_params import list_query_params

heroes_router = APIRouter(
    prefix="/heroes",
    tags=["Heroes"],
)


@heroes_router.get("/", response_model=PaginatedResponse[HeroResponse])
def get_heroes(params=Depends(list_query_params), db: Session = Depends(get_db)):
    stmt = select(Heroes).limit(params["limit"]).offset(params["offset"])
    results = db.exec(stmt)
    heroes = results.all()

    total_count = db.exec(select(func.count()).select_from(Heroes)).one()

    current_page = (
        (params["offset"] // params["limit"]) + 1 if params["limit"] > 0 else 1
    )

    total_pages = (
        (total_count + params["limit"] - 1) // params["limit"]
        if params["limit"] > 0
        else 1
    )

    return PaginatedResponse[HeroResponse](
        message="Heroes retrieved successfully",
        data=[
            HeroResponse(
                id=hero.id,
                name=hero.name,
                type=hero.type,
                difficulty=hero.difficulty,
            )
            for hero in heroes
        ],
        pagination=Pagination(
            current_page=current_page,
            total_records=total_count,
            total_pages=total_pages,
        ),
    )


@heroes_router.get(
    "/{hero_id}",
    responses={404: {"description": "Hero not found"}},
    response_model=Response[HeroResponse],
)
def get_hero(hero_id: str, db: Session = Depends(get_db)):
    stmt = select(Heroes).where(Heroes.id == hero_id)
    results = db.exec(stmt)
    hero = results.one()

    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found"
        )
    return Response[HeroResponse](
        data=HeroResponse(
            id=hero.id,
            name=hero.name,
            type=hero.type,
            difficulty=hero.difficulty,
        ),
    )


@heroes_router.post("/", status_code=status.HTTP_201_CREATED)
def create_hero(
    body: HeroCreateRequest,
    db: Session = Depends(get_db),
):
    new_hero = Heroes(name=body.name, type=body.type, difficulty=body.difficulty)
    db.add(new_hero)
    db.commit()
    db.refresh(new_hero)

    return Response[HeroResponse](
        data=HeroResponse(
            id=new_hero.id,
            name=new_hero.name,
            type=new_hero.type,
            difficulty=new_hero.difficulty,
        ),
    )


@heroes_router.patch("/{hero_id}", responses={404: {"description": "Hero not found"}})
def update_hero(hero_id: str, body: HeroUpdateRequest, db: Session = Depends(get_db)):
    stmt = select(Heroes).where(Heroes.id == hero_id)
    results = db.exec(stmt)
    updated_hero = results.one()

    if not updated_hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found"
        )

    updated_hero.name = body.name or updated_hero.name
    updated_hero.type = body.type or updated_hero.type
    updated_hero.difficulty = body.difficulty or updated_hero.difficulty

    db.add(updated_hero)
    db.commit()
    db.refresh(updated_hero)

    return Response[HeroResponse](
        data=HeroResponse(
            id=updated_hero.id,
            name=updated_hero.name,
            type=updated_hero.type,
            difficulty=updated_hero.difficulty,
        ),
    )


@heroes_router.delete("/{hero_id}", responses={404: {"description": "Hero not found"}})
def delete_hero(hero_id: str, body: HeroUpdateRequest, db: Session = Depends(get_db)):
    stmt = select(Heroes).where(Heroes.id == hero_id)
    results = db.exec(stmt)
    updated_hero = results.one()

    if not updated_hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found"
        )

    updated_hero.name = body.name or updated_hero.name
    updated_hero.type = body.type or updated_hero.type
    updated_hero.difficulty = body.difficulty or updated_hero.difficulty

    db.add(updated_hero)
    db.commit()
    db.refresh(updated_hero)

    return True
