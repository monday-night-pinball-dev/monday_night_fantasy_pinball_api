from copy import copy
from datetime import datetime
from typing import Any
from uuid import UUID

from fastapi import HTTPException
from adapters.pos_simulator_response_adapters import PosSimulatorResponseDataAdapter
from adapters.common_adapters import CommonAdapters 
from managers.managers import Manager
from models.pos_simulator_response_model import (
    PosSimulatorResponseCreateModel, 
    PosSimulatorResponseInboundCreateModel,
    PosSimulatorResponseInboundSearchModel, 
    PosSimulatorResponseModel,
    PosSimulatorResponseOutboundModel,
    PosSimulatorResponseSearchModel, 
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)
from util.database import PagingModel 

class PosSimulatorResponseController:
    
    def __init__(
        self, 
        adapter: PosSimulatorResponseDataAdapter = PosSimulatorResponseDataAdapter(),
        common_adapter: CommonAdapters = CommonAdapters(),
        manager: Manager = Manager()
    ) -> None:
        
        self.adapter = adapter
        self.common_adapter = common_adapter
        self.manager = manager
    
    def create(
        self, 
        inbound_model: PosSimulatorResponseInboundCreateModel, 
        headers: dict[str,str]
    ) -> PosSimulatorResponseOutboundModel | None:
        
        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        model: PosSimulatorResponseCreateModel =self.adapter.convert_from_inbound_create_model_to_create_model(inbound_model)

        result = self.manager.create_pos_simulator_response(model, request_operators)

        if result is None:
            raise Exception('Received no model from create operation.')

        response_model: PosSimulatorResponseOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model

    def get_by_id(
        self, 
        id: UUID, 
        headers: dict[str,str]
    ) -> PosSimulatorResponseOutboundModel | None:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        result = self.manager.get_pos_simulator_response_by_id(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'PosSimulatorResponse with id {id} not found.',
            )

        response_model: PosSimulatorResponseOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model

    def call(
        self, 
        id: UUID,
        headers: dict[str,str]
    ) -> dict[str, Any | None]:
        
        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        result = self.manager.call_pos_simulator_response(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'Product with id {id} not found.',
            )
        
        response_model: dict[str, Any | None] = result
        
        return response_model
    def search(
        self, 
        inbound_model: PosSimulatorResponseInboundSearchModel, 
        headers: dict[str,str]
    ) -> OutboundItemListResponse[PosSimulatorResponseOutboundModel]:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        paging_model: PagingModel = self.common_adapter.convert_from_paged_inbound_model_to_paging_model(inbound_model)

        search_model: PosSimulatorResponseSearchModel =self.adapter.convert_from_inbound_search_model_to_search_model(inbound_model)

        results: ItemList[PosSimulatorResponseModel] = self.manager.search_pos_simulator_responses(
            search_model, 
            paging_model, 
            request_operators
        )

        return_result_list = list(
            map(
                lambda x:self.adapter.convert_from_model_to_outbound_model(x),
                results.items,
            )
        )

        outbound_paging: OutboundResultantPagingModel = self.common_adapter.convert_from_paging_model_to_outbound_paging_model(results.paging)

        return_result = OutboundItemListResponse(items=return_result_list, paging=outbound_paging)

        return return_result
 
    def delete(
        self, 
        id: UUID, 
        headers: dict[str,str]
    ) -> PosSimulatorResponseOutboundModel | None:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        result = self.manager.delete_pos_simulator_response(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'PosSimulatorResponse with id {id} not found.',
            )

        response_model: PosSimulatorResponseOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model
