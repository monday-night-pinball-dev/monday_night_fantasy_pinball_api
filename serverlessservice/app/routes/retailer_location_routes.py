from fastapi import Depends, FastAPI, HTTPException, Request, Response
from pydantic import UUID4
import uvicorn

from models.retailer_location_model import (
    RetailerLocationInboundCreateModel,
    RetailerLocationInboundSearchModel,
    RetailerLocationInboundUpdateModel,
    RetailerLocationOutboundModel,
)
from controllers.retailer_location_controller import RetailerLocationController
from models.common_model import (
    CommonOutboundResponseModel,
    OutboundItemListResponse,
)
from util.environment import Environment

controller: RetailerLocationController = RetailerLocationController()


def set_retailer_location_routes(app: FastAPI):

    @app.post(
        '/retailer_locations',
        response_model=RetailerLocationOutboundModel,
        status_code=201,
    )
    def post_retailer_location( 
        inbound_create_model: RetailerLocationInboundCreateModel, 
        request: Request
    ) -> RetailerLocationOutboundModel | None:
         
        result = controller.create(inbound_create_model, request.headers)

        return result

    @app.get(
        '/retailer_locations',
        response_model=OutboundItemListResponse[RetailerLocationOutboundModel],
    )
    def get_retailer_locations(  
        request: Request,
        inbound_search_model: RetailerLocationInboundSearchModel = Depends(), 
    ) -> OutboundItemListResponse[RetailerLocationOutboundModel]:
       
        result = controller.search(inbound_search_model, request.headers)

        return result

    @app.get(
        '/retailer_locations/{id}',
        response_model=RetailerLocationOutboundModel,
    )
    def get_retailer_location_by_id(request: Request, id: UUID4) -> RetailerLocationOutboundModel | None:

        result = controller.get_by_id(id, request.headers)

        return result

    @app.patch(
        '/retailer_locations/{id}',
        response_model=RetailerLocationOutboundModel,
    )
    def patch_retailer_location(
            id: UUID4,
            inbound_update_model: RetailerLocationInboundUpdateModel,
            request: Request
    ) -> RetailerLocationOutboundModel | None:
        result = controller.update(id, inbound_update_model, request.headers)

        return result

    @app.delete(
        '/retailer_locations/{id}',
        response_model=RetailerLocationOutboundModel,
    ) 
    def delete_retailer_location(
        id: UUID4, 
        request: Request
    ) -> RetailerLocationOutboundModel | None:

        result = controller.delete(id, request.headers)

        return result
