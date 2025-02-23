from copy import copy
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from adapters.pos_integration_call_adapters import PosIntegrationCallDataAdapter
from adapters.common_adapters import CommonAdapters 
from managers.managers import Manager
from models.pos_integration_call_model import (
    PosIntegrationCallCreateModel,
    PosIntegrationCallDatabaseModel,
    PosIntegrationCallInboundCreateModel,
    PosIntegrationCallInboundSearchModel, 
    PosIntegrationCallModel,
    PosIntegrationCallOutboundModel,
    PosIntegrationCallSearchModel, 
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)
from util.database import PagingModel 

class PosIntegrationCallController:
    
    def __init__(
        self, 
        adapter: PosIntegrationCallDataAdapter = PosIntegrationCallDataAdapter(),
        common_adapter: CommonAdapters = CommonAdapters(),
        manager: Manager = Manager()
    ) -> None:
        
        self.adapter = adapter
        self.common_adapter = common_adapter
        self.manager = manager
    
    def create(
        self, 
        inbound_model: PosIntegrationCallInboundCreateModel, 
        headers: dict[str,str]
    ) -> PosIntegrationCallOutboundModel | None:
        
        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        model: PosIntegrationCallCreateModel =self.adapter.convert_from_inbound_create_model_to_create_model(inbound_model)

        result = self.manager.create_pos_integration_call(model, request_operators)

        if result is None:
            raise Exception('Received no model from create operation.')

        response_model: PosIntegrationCallOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model

    def get_by_id(
        self, 
        id: UUID, 
        headers: dict[str,str]
    ) -> PosIntegrationCallOutboundModel | None:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        result = self.manager.get_pos_integration_call_by_id(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'PosIntegrationCall with id {id} not found.',
            )

        response_model: PosIntegrationCallOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model

    def search(
        self, 
        inbound_model: PosIntegrationCallInboundSearchModel, 
        headers: dict[str,str]
    ) -> OutboundItemListResponse[PosIntegrationCallOutboundModel]:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        paging_model: PagingModel = self.common_adapter.convert_from_paged_inbound_model_to_paging_model(inbound_model)

        search_model: PosIntegrationCallSearchModel =self.adapter.convert_from_inbound_search_model_to_search_model(inbound_model)

        results: ItemList[PosIntegrationCallModel] = self.manager.search_pos_integration_calls(
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
    ) -> PosIntegrationCallOutboundModel | None:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        result = self.manager.delete_pos_integration_call(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'PosIntegrationCall with id {id} not found.',
            )

        response_model: PosIntegrationCallOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model
