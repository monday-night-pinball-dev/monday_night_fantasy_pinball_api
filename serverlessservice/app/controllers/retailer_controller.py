from uuid import UUID
from fastapi import HTTPException
from adapters.retailer_adapters import RetailerDataAdapter
from adapters.common_adapters import CommonAdapters
from managers.managers import Manager 
from models.retailer_model import (
    RetailerCreateModel, 
    RetailerInboundCreateModel,
    RetailerInboundSearchModel,
    RetailerInboundUpdateModel,
    RetailerModel,
    RetailerOutboundModel,
    RetailerSearchModel,
    RetailerUpdateModel,
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)
from util.database import PagingModel

class RetailerController:
    
    def __init__(
        self, 
        adapter: RetailerDataAdapter = RetailerDataAdapter(),
        common_adapter: CommonAdapters = CommonAdapters(),
        manager: Manager = Manager()
    ) -> None:
        
        self.adapter = adapter
        self.common_adapter = common_adapter
        self.manager = manager
    
    def create(
        self, 
        inbound_model: RetailerInboundCreateModel, 
        headers: dict[str,str]
        
    ) -> RetailerOutboundModel | None:
        
        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        model: RetailerCreateModel =self.adapter.convert_from_inbound_create_model_to_create_model(inbound_model)

        result = self.manager.create_retailer(model, request_operators)

        if result is None:
            raise Exception('Received no model from create operation.')

        response_model: RetailerOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model

    def get_by_id(
        self, 
        id: UUID, 
        headers: dict[str,str]
    ) -> RetailerOutboundModel | None:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        result = self.manager.get_retailer_by_id(id, request_operators)

        if result is None:
            raise HTTPException(status_code=404,
                                detail=f'Retailer with id {id} not found.')

        response_model: RetailerOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model

    def search(
        self, 
        inbound_model: RetailerInboundSearchModel, 
        headers: dict[str,str]
    ) -> OutboundItemListResponse[RetailerOutboundModel]:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        paging_model: PagingModel = self.common_adapter.convert_from_paged_inbound_model_to_paging_model(inbound_model)

        search_model: RetailerSearchModel =self.adapter.convert_from_inbound_search_model_to_search_model(inbound_model)

        results: ItemList[RetailerModel] = self.manager.search_retailers(
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

    def update(
        self,
        id: UUID,
        inbound_model: RetailerInboundUpdateModel, 
        headers: dict[str,str] | None = None
    ):
        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)

        model: RetailerUpdateModel = (
           self.adapter.convert_from_inbound_update_model_to_update_model(
                inbound_model))

        result: None | RetailerModel = self.manager.update_retailer(
            id, 
            model, 
            request_operators
        )

        if result is None:
            raise HTTPException(status_code=404,
                                detail=f'Retailer with id {id} not found.')

        response_model: RetailerOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model

    def delete(
        self, 
        id: UUID, 
        headers: dict[str,str]
    ) -> RetailerOutboundModel | None:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        result = self.manager.delete_retailer(id, request_operators)

        if result is None:
            raise HTTPException(status_code=404,
                                detail=f'Retailer with id {id} not found.')

        response_model: RetailerOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model
