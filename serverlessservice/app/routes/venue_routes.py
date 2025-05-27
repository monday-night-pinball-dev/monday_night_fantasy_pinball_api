from fastapi import Depends, FastAPI, Request
from pydantic import UUID4

from models.venue_model import (
    VenueInboundCreateModel,
    VenueInboundSearchModel,
    VenueInboundUpdateModel,
    VenueOutboundModel,
)
from controllers.venue_controller import VenueController
from models.common_model import (
    OutboundItemListResponse,
)

controller: VenueController = VenueController()


def set_venue_routes(app: FastAPI):
    @app.post("/venues", response_model=VenueOutboundModel, status_code=201)
    def post_venue(inbound_create_model: VenueInboundCreateModel, request: Request):
        result = controller.create(inbound_create_model, request.headers)

        return result

    @app.get(
        "/venues",
        response_model=OutboundItemListResponse[VenueOutboundModel],
    )
    def get_venues(
        request: Request,
        inbound_search_model: VenueInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[VenueOutboundModel]:
        result = controller.search(inbound_search_model, request.headers)

        return result

    @app.get("/venues/{id}", response_model=VenueOutboundModel)
    def get_venue_by_id(id: UUID4, request: Request):
        result = controller.get_by_id(id, request.headers)

        return result

    @app.patch("/venues/{id}", response_model=VenueOutboundModel)
    def patch_user(
        id: UUID4, inbound_update_model: VenueInboundUpdateModel, request: Request
    ) -> VenueOutboundModel | None:
        result = controller.update(id, inbound_update_model, request.headers)

        return result

    @app.delete("/venues/{id}", response_model=VenueOutboundModel)
    def delete_venue(id: UUID4, request: Request):
        result = controller.delete(id, request.headers)

        return result
