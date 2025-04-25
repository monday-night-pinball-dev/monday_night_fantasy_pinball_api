from fastapi import Depends, FastAPI, Request
from pydantic import UUID4

from models.fantasy_team_season_link_model import (
    FantasyTeamSeasonLinkInboundCreateModel,
    FantasyTeamSeasonLinkInboundSearchModel,
    FantasyTeamSeasonLinkOutboundModel,
)
from controllers.fantasy_team_season_link_controller import (
    FantasyTeamSeasonLinkController,
)
from models.common_model import (
    OutboundItemListResponse,
)

controller: FantasyTeamSeasonLinkController = FantasyTeamSeasonLinkController()


def set_fantasy_team_season_link_routes(app: FastAPI):
    @app.post(
        "/fantasy_team_season_links",
        response_model=FantasyTeamSeasonLinkOutboundModel,
        status_code=201,
    )
    def post_fantasy_team_season_link(
        inbound_create_model: FantasyTeamSeasonLinkInboundCreateModel, request: Request
    ):
        result = controller.create(inbound_create_model, request.headers)

        return result

    @app.get(
        "/fantasy_team_season_links",
        response_model=OutboundItemListResponse[FantasyTeamSeasonLinkOutboundModel],
    )
    def get_fantasy_team_season_links(
        request: Request,
        inbound_search_model: FantasyTeamSeasonLinkInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[FantasyTeamSeasonLinkOutboundModel]:
        result = controller.search(inbound_search_model, request.headers)

        return result

    @app.get(
        "/fantasy_team_season_links/{id}",
        response_model=FantasyTeamSeasonLinkOutboundModel,
    )
    def get_fantasy_team_season_link_by_id(id: UUID4, request: Request):
        result = controller.get_by_id(id, request.headers)

        return result

    @app.delete(
        "/fantasy_team_season_links/{id}",
        response_model=FantasyTeamSeasonLinkOutboundModel,
    )
    def delete_fantasy_team_season_link(id: UUID4, request: Request):
        result = controller.delete(id, request.headers)

        return result
