from typing import Any
from fastapi import Depends, FastAPI, Request
from pydantic import UUID4 

from models.pos_simulator_response_model import (
    PosSimulatorResponseInboundCreateModel,
    PosSimulatorResponseInboundSearchModel, 
    PosSimulatorResponseOutboundModel,
)
from controllers.pos_simulator_response_controller import PosSimulatorResponseController
from models.common_model import (
    OutboundItemListResponse
) 

controller: PosSimulatorResponseController = PosSimulatorResponseController()


def set_pos_simulator_response_routes(app: FastAPI):

    @app.post(
        '/pos_simulator_responses',
        response_model=PosSimulatorResponseOutboundModel,
        status_code=201,
    )
    def post_pos_simulator_response(
        inbound_create_model: PosSimulatorResponseInboundCreateModel,
        request: Request
    ):
        result = controller.create(inbound_create_model , request.headers)

        return result

    @app.get(
        '/pos_simulator_responses',
        response_model=OutboundItemListResponse[PosSimulatorResponseOutboundModel],
    )
    def get_retailer_locations(
        request: Request,
        inbound_search_model: PosSimulatorResponseInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[PosSimulatorResponseOutboundModel]:

        result = controller.search(inbound_search_model , request.headers)

        return result

    @app.get('/pos_simulator_responses/{id}',
             response_model=PosSimulatorResponseOutboundModel)
    def get_pos_simulator_response_by_id(id: UUID4, request: Request):

        result = controller.get_by_id(id, request.headers)

        return result
    
    
    @app.get('/pos_simulator_responses/{id}/call',
             response_model=dict[str, Any | None])
    def call_pos_simulator_response(id: UUID4, request: Request):

        result = controller.call(id, request.headers)

        return result
  
    @app.delete('/pos_simulator_responses/{id}',
                response_model=PosSimulatorResponseOutboundModel)
    def delete_pos_simulator_response(id: UUID4, request: Request):

        result = controller.delete(id, request.headers)

        return result
