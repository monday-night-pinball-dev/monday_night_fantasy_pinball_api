from fastapi import Depends, FastAPI, Request
from pydantic import UUID4

from models.league_player_fantasy_team_season_link_model import (
    LeaguePlayerFantasyTeamSeasonLinkInboundCreateModel,
    LeaguePlayerFantasyTeamSeasonLinkInboundSearchModel,
    LeaguePlayerFantasyTeamSeasonLinkOutboundModel,
)
from controllers.league_player_fantasy_team_season_link_controller import (
    LeaguePlayerFantasyTeamSeasonLinkController,
)
from models.common_model import (
    OutboundItemListResponse,
)

controller: LeaguePlayerFantasyTeamSeasonLinkController = (
    LeaguePlayerFantasyTeamSeasonLinkController()
)


def set_league_player_fantasy_team_season_link_routes(app: FastAPI):
    @app.post(
        "/league_player_fantasy_team_season_links",
        response_model=LeaguePlayerFantasyTeamSeasonLinkOutboundModel,
        status_code=201,
    )
    def post_league_player_fantasy_team_season_link(
        inbound_create_model: LeaguePlayerFantasyTeamSeasonLinkInboundCreateModel,
        request: Request,
    ):
        result = controller.create(inbound_create_model, request.headers)

        return result

    @app.get(
        "/league_player_fantasy_team_season_links",
        response_model=OutboundItemListResponse[
            LeaguePlayerFantasyTeamSeasonLinkOutboundModel
        ],
    )
    def get_league_player_fantasy_team_season_links(
        request: Request,
        inbound_search_model: LeaguePlayerFantasyTeamSeasonLinkInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[LeaguePlayerFantasyTeamSeasonLinkOutboundModel]:
        result = controller.search(inbound_search_model, request.headers)

        return result

    @app.get(
        "/league_player_fantasy_team_season_links/{id}",
        response_model=LeaguePlayerFantasyTeamSeasonLinkOutboundModel,
    )
    def get_league_player_fantasy_team_season_link_by_id(id: UUID4, request: Request):
        result = controller.get_by_id(id, request.headers)

        return result

    @app.delete(
        "/league_player_fantasy_team_season_links/{id}",
        response_model=LeaguePlayerFantasyTeamSeasonLinkOutboundModel,
    )
    def delete_league_player_fantasy_team_season_link(id: UUID4, request: Request):
        result = controller.delete(id, request.headers)

        return result
