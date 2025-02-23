from fastapi import Depends, FastAPI, Request
from pydantic import UUID4

from models.league_team_model import (
    LeagueTeamInboundCreateModel,
    LeagueTeamInboundSearchModel,
    LeagueTeamInboundUpdateModel,
    LeagueTeamOutboundModel,
)
from controllers.league_team_controller import LeagueTeamController
from models.common_model import (
    OutboundItemListResponse,
)

controller: LeagueTeamController = LeagueTeamController()


def set_league_team_routes(app: FastAPI):
    @app.post("/league_teams", response_model=LeagueTeamOutboundModel, status_code=201)
    def post_league_team(
        inbound_create_model: LeagueTeamInboundCreateModel, request: Request
    ):
        result = controller.create(inbound_create_model, request.headers)

        return result

    @app.get(
        "/league_teams",
        response_model=OutboundItemListResponse[LeagueTeamOutboundModel],
    )
    def get_league_teams(
        request: Request,
        inbound_search_model: LeagueTeamInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[LeagueTeamOutboundModel]:
        result = controller.search(inbound_search_model, request.headers)

        return result

    @app.get("/league_teams/{id}", response_model=LeagueTeamOutboundModel)
    def get_league_team_by_id(id: UUID4, request: Request):
        result = controller.get_by_id(id, request.headers)

        return result

    @app.patch("/league_teams/{id}", response_model=LeagueTeamOutboundModel)
    def patch_league_team(
        id: UUID4, inbound_update_model: LeagueTeamInboundUpdateModel, request: Request
    ) -> LeagueTeamOutboundModel | None:
        result = controller.update(id, inbound_update_model, request.headers)

        return result

    @app.delete("/league_teams/{id}", response_model=LeagueTeamOutboundModel)
    def delete_league_team(id: UUID4, request: Request):
        result = controller.delete(id, request.headers)

        return result
