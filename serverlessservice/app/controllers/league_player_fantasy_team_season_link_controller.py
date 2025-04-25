from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models.league_player_fantasy_team_season_link_model import (
    LeaguePlayerFantasyTeamSeasonLinkInboundCreateModel,
    LeaguePlayerFantasyTeamSeasonLinkInboundSearchModel,
    LeaguePlayerFantasyTeamSeasonLinkOutboundModel,
)
from adapters.league_player_fantasy_team_season_link_adapters import (
    LeaguePlayerFantasyTeamSeasonLinkAdapter,
)
from services.league_player_fantasy_team_season_link_service import (
    LeaguePlayerFantasyTeamSeasonLinkService,
)

router = APIRouter(
    prefix="/league-player-fantasy-team-season-links",
    tags=["League Player Fantasy Team Season Links"],
)


@router.post(
    "/",
    response_model=LeaguePlayerFantasyTeamSeasonLinkOutboundModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_link(
    inbound_create_model: LeaguePlayerFantasyTeamSeasonLinkInboundCreateModel,
    service: LeaguePlayerFantasyTeamSeasonLinkService = Depends(),
    adapter: LeaguePlayerFantasyTeamSeasonLinkAdapter = Depends(),
):
    create_model = adapter.convert_from_inbound_create_model_to_create_model(
        inbound_create_model
    )
    database_model = await service.create_link(create_model)
    return adapter.convert_from_database_model_to_outbound_model(database_model)


@router.get("/", response_model=List[LeaguePlayerFantasyTeamSeasonLinkOutboundModel])
async def search_links(
    inbound_search_model: LeaguePlayerFantasyTeamSeasonLinkInboundSearchModel = Depends(),
    service: LeaguePlayerFantasyTeamSeasonLinkService = Depends(),
    adapter: LeaguePlayerFantasyTeamSeasonLinkAdapter = Depends(),
):
    search_model = adapter.convert_from_inbound_search_model_to_search_model(
        inbound_search_model
    )
    database_models = await service.search_links(search_model)
    return [
        adapter.convert_from_database_model_to_outbound_model(model)
        for model in database_models
    ]


@router.get("/{link_id}", response_model=LeaguePlayerFantasyTeamSeasonLinkOutboundModel)
async def get_link_by_id(
    link_id: str,
    service: LeaguePlayerFantasyTeamSeasonLinkService = Depends(),
    adapter: LeaguePlayerFantasyTeamSeasonLinkAdapter = Depends(),
):
    database_model = await service.get_link_by_id(link_id)
    if not database_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Link not found"
        )
    return adapter.convert_from_database_model_to_outbound_model(database_model)


@router.delete("/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_link(
    link_id: str,
    service: LeaguePlayerFantasyTeamSeasonLinkService = Depends(),
):
    success = await service.delete_link(link_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Link not found"
        )
