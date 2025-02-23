from uuid import UUID
from fastapi import HTTPException
from adapters.vendor_adapters import VendorDataAdapter
from adapters.common_adapters import CommonAdapters
from managers.managers import Manager 
from models.vendor_model import (
    VendorCreateModel,
    VendorDatabaseModel,
    VendorInboundCreateModel,
    VendorInboundSearchModel,
    VendorInboundUpdateModel,
    VendorModel,
    VendorOutboundModel,
    VendorSearchModel,
    VendorUpdateModel,
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)
from util.database import PagingModel

class VendorController:
    
    def __init__(
        self, 
        adapter: VendorDataAdapter = VendorDataAdapter(),
        common_adapter: CommonAdapters = CommonAdapters(),
        manager: Manager = Manager()
    ) -> None:
        
        self.adapter = adapter
        self.common_adapter = common_adapter
        self.manager = manager
    
    def create(
            self, 
            inbound_model: VendorInboundCreateModel, 
            headers: dict[str,str]
    ) -> VendorOutboundModel | None:
        
        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        model: VendorCreateModel =self.adapter.convert_from_inbound_create_model_to_create_model(inbound_model)

        result = self.manager.create_vendor(model, request_operators)

        if result is None:
            raise Exception('Received no model from create operation.')

        response_model: VendorOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model

    def get_by_id(
        self, 
        id: UUID, 
        headers: dict[str,str]
    ) -> VendorOutboundModel | None:
        
        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        result = self.manager.get_vendor_by_id(id, request_operators)

        if result is None:
            raise HTTPException(status_code=404,
                                detail=f'Vendor with id {id} not found.')

        response_model: VendorOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model

    def search(
        self, 
        inbound_model: VendorInboundSearchModel, 
        headers: dict[str,str]
    ) -> OutboundItemListResponse[VendorOutboundModel]:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        paging_model: PagingModel = self.common_adapter.convert_from_paged_inbound_model_to_paging_model(inbound_model)

        search_model: VendorSearchModel =self.adapter.convert_from_inbound_search_model_to_search_model(inbound_model)

        results: ItemList[VendorModel] = self.manager.search_vendors(
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
        inbound_model: VendorInboundUpdateModel, 
        headers: dict[str,str] | None = None
    ):
        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)

        model: VendorUpdateModel = (
           self.adapter.convert_from_inbound_update_model_to_update_model(
                inbound_model))

        result: None | VendorModel = self.manager.update_vendor(id, model, request_operators)

        if result is None:
            raise HTTPException(status_code=404,
                                detail=f'Vendor with id {id} not found.')

        response_model: VendorOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model

    def delete(
        self, 
        id: UUID, 
        headers: dict[str,str]
    ) -> VendorOutboundModel | None:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        result = self.manager.delete_vendor(id, request_operators)

        if result is None:
            raise HTTPException(status_code=404,
                                detail=f'Vendor with id {id} not found.')

        response_model: VendorOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model
