from copy import copy
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from adapters.historical_sale_item_adapters import HistoricalSaleItemDataAdapter
from adapters.common_adapters import CommonAdapters 
from managers.managers import Manager
from models.historical_sale_item_model import (
    HistoricalSaleItemCreateModel,
    HistoricalSaleItemDatabaseModel,
    HistoricalSaleItemInboundCreateModel,
    HistoricalSaleItemInboundSearchModel, 
    HistoricalSaleItemModel,
    HistoricalSaleItemOutboundModel,
    HistoricalSaleItemSearchModel, 
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)
from util.common import RequestOperators
from util.database import PagingModel
 
class HistoricalSaleItemController:

    def __init__(
        self, 
        adapter: HistoricalSaleItemDataAdapter = HistoricalSaleItemDataAdapter(),
        common_adapter: CommonAdapters = CommonAdapters(),
        manager: Manager = Manager()
    ) -> None:
        
        self.adapter = adapter
        self.common_adapter = common_adapter
        self.manager = manager
        
    def create(
        self, 
        inbound_model: HistoricalSaleItemInboundCreateModel,
        headers: dict[str,str]
    ) -> HistoricalSaleItemOutboundModel | None:
        
        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        model: HistoricalSaleItemCreateModel =self.adapter.convert_from_inbound_create_model_to_create_model(inbound_model)

        result = self.manager.create_historical_sale_item(model, request_operators)

        if result is None:
            raise Exception('Received no model from create operation.')

        response_model: HistoricalSaleItemOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model

    def get_by_id(
        self, 
        id: UUID,
        headers: dict[str,str]
    ) -> HistoricalSaleItemOutboundModel | None:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        result = self.manager.get_historical_sale_item_by_id(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'HistoricalSaleItem with id {id} not found.',
            )

        response_model: HistoricalSaleItemOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model

    def search(
        self, 
        inbound_model: HistoricalSaleItemInboundSearchModel,
        headers: dict[str,str]
    ) -> OutboundItemListResponse[HistoricalSaleItemOutboundModel]:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        paging_model: PagingModel = self.common_adapter.convert_from_paged_inbound_model_to_paging_model(inbound_model)

        search_model: HistoricalSaleItemSearchModel =self.adapter.convert_from_inbound_search_model_to_search_model(inbound_model)

        results: ItemList[HistoricalSaleItemModel] = self.manager.search_historical_sale_items(search_model, paging_model, request_operators)

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
    ) -> HistoricalSaleItemOutboundModel | None:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        result = self.manager.delete_historical_sale_item(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'HistoricalSaleItem with id {id} not found.',
            )

        response_model: HistoricalSaleItemOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model 
