from fastapi import Depends, FastAPI, Request
from pydantic import UUID4

from models.fantasy_team_model import (
    FantasyTeamInboundCreateModel,
    FantasyTeamInboundSearchModel,
    FantasyTeamInboundUpdateModel,
    FantasyTeamOutboundModel,
)
from controllers.fantasy_team_controller import FantasyTeamController
from models.common_model import (
    OutboundItemListResponse,
)

controller: FantasyTeamController = FantasyTeamController()


def set_fantasy_team_routes(app: FastAPI):
    @app.post(
        "/fantasy_teams", response_model=FantasyTeamOutboundModel, status_code=201
    )
    def post_fantasy_team(
        inbound_create_model: FantasyTeamInboundCreateModel, request: Request
    ):
        result = controller.create(inbound_create_model, request.headers)

        return result

    @app.get(
        "/fantasy_teams",
        response_model=OutboundItemListResponse[FantasyTeamOutboundModel],
    )
    def get_fantasy_teams(
        request: Request,
        inbound_search_model: FantasyTeamInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[FantasyTeamOutboundModel]:
        result = controller.search(inbound_search_model, request.headers)

        return result

    @app.get("/fantasy_teams/{id}", response_model=FantasyTeamOutboundModel)
    def get_fantasy_team_by_id(id: UUID4, request: Request):
        result = controller.get_by_id(id, request.headers)

        return result

    @app.patch("/fantasy_teams/{id}", response_model=FantasyTeamOutboundModel)
    def patch_fantasy_team(
        id: UUID4,
        inbound_update_model: FantasyTeamInboundUpdateModel,
        request: Request,
    ) -> FantasyTeamOutboundModel | None:
        result = controller.update(id, inbound_update_model, request.headers)

        return result

    @app.delete("/fantasy_teams/{id}", response_model=FantasyTeamOutboundModel)
    def delete_fantasy_team(id: UUID4, request: Request):
        result = controller.delete(id, request.headers)

        return result
