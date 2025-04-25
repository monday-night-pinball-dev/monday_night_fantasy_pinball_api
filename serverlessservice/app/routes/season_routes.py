from fastapi import Depends, FastAPI, Request
from pydantic import UUID4

from models.season_model import (
    SeasonInboundCreateModel,
    SeasonInboundSearchModel,
    SeasonInboundUpdateModel,
    SeasonOutboundModel,
)
from controllers.season_controller import SeasonController
from models.common_model import (
    OutboundItemListResponse,
)

controller: SeasonController = SeasonController()


def set_season_routes(app: FastAPI):
    @app.post("/seasons", response_model=SeasonOutboundModel, status_code=201)
    def post_season(inbound_create_model: SeasonInboundCreateModel, request: Request):
        result = controller.create(inbound_create_model, request.headers)

        return result

    @app.get(
        "/seasons",
        response_model=OutboundItemListResponse[SeasonOutboundModel],
    )
    def get_seasons(
        request: Request,
        inbound_search_model: SeasonInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[SeasonOutboundModel]:
        result = controller.search(inbound_search_model, request.headers)

        return result

    @app.get("/seasons/{id}", response_model=SeasonOutboundModel)
    def get_season_by_id(id: UUID4, request: Request):
        result = controller.get_by_id(id, request.headers)

        return result

    @app.patch(
        "/seasons/{id}",
        response_model=SeasonOutboundModel,
    )
    def patch_season(
        id: UUID4,
        inbound_update_model: SeasonInboundUpdateModel,
        request: Request,
    ):
        result = controller.update(id, inbound_update_model, request.headers)

        return result

    @app.delete("/seasons/{id}", response_model=SeasonOutboundModel)
    def delete_season(id: UUID4, request: Request):
        result = controller.delete(id, request.headers)

        return result
