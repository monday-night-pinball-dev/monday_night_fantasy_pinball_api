from fastapi import Depends, FastAPI, Request
from pydantic import UUID4

from models.league_player_model import (
    LeaguePlayerInboundCreateModel,
    LeaguePlayerInboundSearchModel,
    LeaguePlayerInboundUpdateModel,
    LeaguePlayerOutboundModel,
)
from controllers.league_player_controller import LeaguePlayerController
from models.common_model import (
    OutboundItemListResponse,
)

controller: LeaguePlayerController = LeaguePlayerController()


def set_league_player_routes(app: FastAPI):
    @app.post(
        "/league_players", response_model=LeaguePlayerOutboundModel, status_code=201
    )
    def post_league_player(
        inbound_create_model: LeaguePlayerInboundCreateModel, request: Request
    ):
        result = controller.create(inbound_create_model, request.headers)

        return result

    @app.get(
        "/league_players",
        response_model=OutboundItemListResponse[LeaguePlayerOutboundModel],
    )
    def get_league_players(
        request: Request,
        inbound_search_model: LeaguePlayerInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[LeaguePlayerOutboundModel]:
        result = controller.search(inbound_search_model, request.headers)

        return result

    @app.get("/league_players/{id}", response_model=LeaguePlayerOutboundModel)
    def get_league_player_by_id(id: UUID4, request: Request):
        result = controller.get_by_id(id, request.headers)

        return result

    @app.patch("/league_players/{id}", response_model=LeaguePlayerOutboundModel)
    def patch_league_player(
        id: UUID4,
        inbound_update_model: LeaguePlayerInboundUpdateModel,
        request: Request,
    ) -> LeaguePlayerOutboundModel | None:
        result = controller.update(id, inbound_update_model, request.headers)

        return result

    @app.delete("/league_players/{id}", response_model=LeaguePlayerOutboundModel)
    def delete_league_player(id: UUID4, request: Request):
        result = controller.delete(id, request.headers)

        return result
