from fastapi import Depends, FastAPI, Request
from pydantic import UUID4

from models.fantasy_league_model import (
    FantasyLeagueInboundCreateModel,
    FantasyLeagueInboundSearchModel,
    FantasyLeagueInboundUpdateModel,
    FantasyLeagueOutboundModel,
)
from controllers.fantasy_league_controller import FantasyLeagueController
from models.common_model import (
    OutboundItemListResponse,
)

controller: FantasyLeagueController = FantasyLeagueController()


def set_fantasy_league_routes(app: FastAPI):
    @app.post(
        "/fantasy_leagues", response_model=FantasyLeagueOutboundModel, status_code=201
    )
    def post_fantasy_league(
        inbound_create_model: FantasyLeagueInboundCreateModel, request: Request
    ):
        result = controller.create(inbound_create_model, request.headers)

        return result

    @app.get(
        "/fantasy_leagues",
        response_model=OutboundItemListResponse[FantasyLeagueOutboundModel],
    )
    def get_fantasy_leagues(
        request: Request,
        inbound_search_model: FantasyLeagueInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[FantasyLeagueOutboundModel]:
        result = controller.search(inbound_search_model, request.headers)

        return result

    @app.get("/fantasy_leagues/{id}", response_model=FantasyLeagueOutboundModel)
    def get_fantasy_league_by_id(id: UUID4, request: Request):
        result = controller.get_by_id(id, request.headers)

        return result

    @app.patch("/fantasy_leagues/{id}", response_model=FantasyLeagueOutboundModel)
    def patch_fantasy_league(
        id: UUID4,
        inbound_update_model: FantasyLeagueInboundUpdateModel,
        request: Request,
    ) -> FantasyLeagueOutboundModel | None:
        result = controller.update(id, inbound_update_model, request.headers)

        return result

    @app.delete("/fantasy_leagues/{id}", response_model=FantasyLeagueOutboundModel)
    def delete_fantasy_league(id: UUID4, request: Request):
        result = controller.delete(id, request.headers)

        return result
