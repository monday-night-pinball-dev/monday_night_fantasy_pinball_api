from fastapi import Depends, FastAPI, HTTPException, Request, Response
from pydantic import UUID4
import uvicorn

from models.pos_integration_model import (
    PosIntegrationInboundCreateModel,
    PosIntegrationInboundSearchModel,
    PosIntegrationInboundUpdateModel,
    PosIntegrationOutboundModel,
)
from controllers.pos_integration_controller import PosIntegrationController
from models.common_model import (
    OutboundItemListResponse, )
from util.environment import Environment

controller: PosIntegrationController = PosIntegrationController()


def set_pos_integration_routes(app: FastAPI):

    @app.post(
        '/pos_integrations',
        response_model=PosIntegrationOutboundModel,
        status_code=201,
    )
    def post_pos_integration(
        inbound_create_model: PosIntegrationInboundCreateModel,
        request: Request
    ):
        result = controller.create(inbound_create_model, request.headers)

        return result

    @app.get(
        '/pos_integrations',
        response_model=OutboundItemListResponse[PosIntegrationOutboundModel],
    )
    def get_retailer_locations(request: Request,
        inbound_search_model: PosIntegrationInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[PosIntegrationOutboundModel]:

        result = controller.search(inbound_search_model, request.headers)

        return result

    @app.get('/pos_integrations/{id}',
             response_model=PosIntegrationOutboundModel)
    def get_pos_integration_by_id(id: UUID4, request: Request):

        result = controller.get_by_id(id, request.headers)

        return result

    @app.patch('/pos_integrations/{id}',
               response_model=PosIntegrationOutboundModel)
    def patch_pos_integration(
            id: UUID4, inbound_update_model: PosIntegrationInboundUpdateModel, request: Request
    ):  
        result = controller.update(id, inbound_update_model, request.headers)

        return result

    @app.delete('/pos_integrations/{id}',
                response_model=PosIntegrationOutboundModel)
    def delete_pos_integration(id: UUID4, request: Request):

        result = controller.delete(id, request.headers)

        return result

    