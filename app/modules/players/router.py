from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, func, select

from app.core.schema import PaginatedResponse, Pagination, Response
from app.models.database import Heroes, PlayerFavouriteHero, Players
from app.models.engine import get_db
from app.modules.heroes.serializer import HeroResponse
from app.modules.players.serializer import (
    AddFavouriteHeroRequest,
    PlayerCreateRequest,
    PlayerResponse,
    PlayerUpdateRequest,
)
from app.utils.query_params import list_query_params

player_router = APIRouter(
    prefix="/players",
    tags=["Players"],
)


@player_router.get("/", response_model=PaginatedResponse[PlayerResponse])
def get_players(params=Depends(list_query_params), db: Session = Depends(get_db)):
    stmt = select(Players).limit(params["limit"]).offset(params["offset"])
    results = db.exec(stmt)
    players = results.all()

    total_count = db.exec(select(func.count()).select_from(Players)).one()

    current_page = (
        (params["offset"] // params["limit"]) + 1 if params["limit"] > 0 else 1
    )

    total_pages = (
        (total_count + params["limit"] - 1) // params["limit"]
        if params["limit"] > 0
        else 1
    )

    return PaginatedResponse[PlayerResponse](
        message="Players retrieved successfully",
        data=[
            PlayerResponse(
                id=player.id,
                username=player.username,
                rank=player.rank,
                favourite_heroes=[
                    HeroResponse(
                        id=hero.id,
                        name=hero.name,
                        type=hero.type,
                        difficulty=hero.difficulty,
                    )
                    for hero in player.favourite_heroes
                ],
            )
            for player in players
        ],
        pagination=Pagination(
            current_page=current_page,
            total_records=total_count,
            total_pages=total_pages,
        ),
    )


@player_router.get(
    "/{player_id}",
    responses={404: {"description": "Player not found"}},
    response_model=Response[PlayerResponse],
)
def get_player(player_id: str, db: Session = Depends(get_db)):
    stmt = select(Players).where(Players.id == player_id)
    results = db.exec(stmt)
    player = results.one_or_none()

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player not found"
        )
    return Response[PlayerResponse](
        data=PlayerResponse(
            id=player.id,
            username=player.username,
            rank=player.rank,
            favourite_heroes=[
                HeroResponse(
                    id=hero.id,
                    name=hero.name,
                    type=hero.type,
                    difficulty=hero.difficulty,
                )
                for hero in player.favourite_heroes
            ],
        ),
    )


@player_router.post("/", status_code=status.HTTP_201_CREATED)
def create_player(
    body: PlayerCreateRequest,
    db: Session = Depends(get_db),
):
    new_player = Players(username=body.username, rank=body.rank)
    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    return Response[PlayerResponse](
        data=PlayerResponse(
            id=new_player.id,
            username=new_player.username,
            rank=new_player.rank,
            favourite_heroes=[],
        ),
    )


@player_router.patch(
    "/{player_id}", responses={404: {"description": "Player not found"}}
)
def update_player(
    player_id: str, body: PlayerUpdateRequest, db: Session = Depends(get_db)
):
    stmt = select(Players).where(Players.id == player_id)
    results = db.exec(stmt)
    player = results.one_or_none()

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player not found"
        )

    player.username = body.username or player.username
    player.rank = body.rank or player.rank

    db.add(player)
    db.commit()
    db.refresh(player)

    return Response[PlayerResponse](
        data=PlayerResponse(
            id=player.id,
            username=player.username,
            rank=player.rank,
            favourite_heroes=[
                HeroResponse(
                    id=hero.id,
                    name=hero.name,
                    type=hero.type,
                    difficulty=hero.difficulty,
                )
                for hero in player.favourite_heroes
            ],
        ),
    )


@player_router.delete(
    "/{player_id}", responses={404: {"description": "Player not found"}}
)
def delete_player(player_id: str, db: Session = Depends(get_db)):
    stmt = select(Players).where(Players.id == player_id)
    results = db.exec(stmt)
    player = results.one_or_none()

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player not found"
        )

    # Delete player's favourite heroes associations first
    stmt_favourites = select(PlayerFavouriteHero).where(
        PlayerFavouriteHero.player_id == player_id
    )
    favourite_results = db.exec(stmt_favourites)
    for favourite in favourite_results:
        db.delete(favourite)

    db.delete(player)
    db.commit()

    return True


@player_router.post(
    "/{player_id}/favourite-heroes",
    responses={
        404: {"description": "Player or Hero not found"},
        409: {"description": "Hero is already in player's favourites"},
    },
    response_model=Response[PlayerResponse],
)
def add_favourite_hero(
    player_id: str, body: AddFavouriteHeroRequest, db: Session = Depends(get_db)
):
    stmt = select(Players).where(Players.id == player_id)
    results = db.exec(stmt)
    player = results.one_or_none()

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player not found"
        )

    stmt = select(Heroes).where(Heroes.id == body.hero_id)
    results = db.exec(stmt)
    hero = results.one_or_none()

    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found"
        )

    stmt = select(PlayerFavouriteHero).where(
        (PlayerFavouriteHero.player_id == player_id)
        & (PlayerFavouriteHero.hero_id == body.hero_id)
    )
    results = db.exec(stmt)
    existing = results.one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Hero is already in player's favourites",
        )

    favourite = PlayerFavouriteHero(player_id=player_id, hero_id=body.hero_id)
    db.add(favourite)
    db.commit()

    db.refresh(player)

    return Response[PlayerResponse](
        data=PlayerResponse(
            id=player.id,
            username=player.username,
            rank=player.rank,
            favourite_heroes=[
                HeroResponse(
                    id=h.id,
                    name=h.name,
                    type=h.type,
                    difficulty=h.difficulty,
                )
                for h in player.favourite_heroes
            ],
        ),
    )
