from copy import copy
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from adapters.inventory_intake_batch_job_adapters import InventoryIntakeBatchJobDataAdapter
from adapters.common_adapters import CommonAdapters 
from managers.managers import Manager
from models.inventory_intake_batch_job_model import (
    InventoryIntakeBatchJobCreateModel,
    InventoryIntakeBatchJobDatabaseModel,
    InventoryIntakeBatchJobInboundCreateModel,
    InventoryIntakeBatchJobInboundSearchModel,
    InventoryIntakeBatchJobInboundUpdateModel,
    InventoryIntakeBatchJobModel,
    InventoryIntakeBatchJobOutboundModel,
    InventoryIntakeBatchJobSearchModel,
    InventoryIntakeBatchJobUpdateModel,
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)
from util.database import PagingModel

class InventoryIntakeBatchJobController:

    def __init__(
        self, 
        adapter: InventoryIntakeBatchJobDataAdapter = InventoryIntakeBatchJobDataAdapter(),
        common_adapter: CommonAdapters = CommonAdapters(),
        manager: Manager = Manager()
    ) -> None:
        
        self.adapter = adapter
        self.common_adapter = common_adapter
        self.manager = manager
        
    def create(
        self, 
        inbound_model: InventoryIntakeBatchJobInboundCreateModel, 
        headers: dict[str,str]
    ) -> InventoryIntakeBatchJobOutboundModel | None:
        
        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        model: InventoryIntakeBatchJobCreateModel =self.adapter.convert_from_inbound_create_model_to_create_model(inbound_model)

        result = self.manager.create_inventory_intake_batch_job(model, request_operators)

        if result is None:
            raise Exception('Received no model from create operation.')

        response_model: InventoryIntakeBatchJobOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model

    def get_by_id(
        self, 
        id: UUID, 
        headers: dict[str,str]
    ) -> InventoryIntakeBatchJobOutboundModel | None:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        result = self.manager.get_inventory_intake_batch_job_by_id(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'InventoryIntakeBatchJob with id {id} not found.',
            )

        response_model: InventoryIntakeBatchJobOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model
    
    def run(
        self, 
        id: UUID, 
        headers: dict[str,str]
    ) -> InventoryIntakeBatchJobOutboundModel | None:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        result = self.manager.run_inventory_intake_batch_job(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'InventoryIntakeBatchJob with id {id} not found.',
            )

        response_model: InventoryIntakeBatchJobOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model

    def search(
        self, 
        inbound_model: InventoryIntakeBatchJobInboundSearchModel, 
        headers: dict[str,str]
    ) -> OutboundItemListResponse[InventoryIntakeBatchJobOutboundModel]:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        paging_model: PagingModel = self.common_adapter.convert_from_paged_inbound_model_to_paging_model(inbound_model)

        search_model: InventoryIntakeBatchJobSearchModel =self.adapter.convert_from_inbound_search_model_to_search_model(inbound_model)

        results: ItemList[InventoryIntakeBatchJobModel] = self.manager.search_inventory_intake_batch_jobs(search_model, paging_model, request_operators)

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
        inbound_model: InventoryIntakeBatchJobInboundUpdateModel, 
        headers: dict[str,str] | None = None
    ) -> InventoryIntakeBatchJobOutboundModel | None:
        
        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
  
        model: InventoryIntakeBatchJobUpdateModel =self.adapter.convert_from_inbound_update_model_to_update_model(inbound_model)

        result: None | InventoryIntakeBatchJobModel = self.manager.update_inventory_intake_batch_job(id, model, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'InventoryIntakeBatchJob with id {id} not found.',
            )

        response_model: InventoryIntakeBatchJobOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)
        

        return response_model

    def delete(
        self, 
        id: UUID,
        headers: dict[str,str]
    ) -> InventoryIntakeBatchJobOutboundModel | None:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        result = self.manager.delete_inventory_intake_batch_job(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'InventoryIntakeBatchJob with id {id} not found.',
            )

        response_model: InventoryIntakeBatchJobOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model
