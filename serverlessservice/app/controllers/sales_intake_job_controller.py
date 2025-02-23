from copy import copy
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from adapters.sales_intake_job_adapters import SalesIntakeJobDataAdapter
from adapters.common_adapters import CommonAdapters 
from managers.managers import Manager
from managers.process_managers import ProcessManager
from models.sales_intake_job_model import (
    SalesIntakeJobCreateModel,
    SalesIntakeJobDatabaseModel,
    SalesIntakeJobInboundCreateModel,
    SalesIntakeJobInboundSearchModel,
    SalesIntakeJobInboundUpdateModel,
    SalesIntakeJobModel,
    SalesIntakeJobOutboundModel,
    SalesIntakeJobSearchModel,
    SalesIntakeJobUpdateModel,
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)
from util.database import PagingModel

class SalesIntakeJobController:
    
    def __init__(
        self, 
        adapter: SalesIntakeJobDataAdapter = SalesIntakeJobDataAdapter(),
        common_adapter: CommonAdapters = CommonAdapters(),
        manager: Manager = Manager(),
        process_manager: ProcessManager = ProcessManager()
    ) -> None:
        
        self.adapter = adapter
        self.common_adapter = common_adapter
        self.manager = manager
        self.process_manager = process_manager
        
    def create( 
        self, 
        inbound_model: SalesIntakeJobInboundCreateModel, 
        headers: dict[str,str]
    ) -> SalesIntakeJobOutboundModel | None:
        
        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        model: SalesIntakeJobCreateModel =self.adapter.convert_from_inbound_create_model_to_create_model(inbound_model)

        result = self.manager.create_sales_intake_job(model, request_operators)

        if result is None:
            raise Exception('Received no model from create operation.')

        response_model: SalesIntakeJobOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model

    def get_by_id(
        self, 
        id: UUID, 
        headers: dict[str,str]
    ) -> SalesIntakeJobOutboundModel | None:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        result = self.manager.get_sales_intake_job_by_id(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'SalesIntakeJob with id {id} not found.',
            )

        response_model: SalesIntakeJobOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model
    
    def run (
        self, 
        id: UUID,
        headers: dict[str,str]
    ) -> SalesIntakeJobOutboundModel | None:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        result = self.process_manager.run_sales_intake_job(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'SalesIntakeJob with id {id} not found.',
            )

        response_model: SalesIntakeJobOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model

    def search(
        self, 
        inbound_model: SalesIntakeJobInboundSearchModel, 
        headers: dict[str,str]
    ) -> OutboundItemListResponse[SalesIntakeJobOutboundModel]:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        paging_model: PagingModel = self.common_adapter.convert_from_paged_inbound_model_to_paging_model(inbound_model)

        search_model: SalesIntakeJobSearchModel =self.adapter.convert_from_inbound_search_model_to_search_model(inbound_model)

        results: ItemList[SalesIntakeJobModel] = self.manager.search_sales_intake_jobs(
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
        inbound_model: SalesIntakeJobInboundUpdateModel,
        headers: dict[str,str] | None = None
    ):
        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)

        model: SalesIntakeJobUpdateModel = (
           self.adapter.convert_from_inbound_update_model_to_update_model(
                inbound_model))

        result: None | SalesIntakeJobModel = self.manager.update_sales_intake_job(id, model, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'SalesIntakeJob with id {id} not found.',
            )

        response_model: SalesIntakeJobOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model

    def delete(
        self, 
        id: UUID, 
        headers: dict[str,str]
    ) -> SalesIntakeJobOutboundModel | None:

        request_operators = self.common_adapter.convert_from_headers_to_operators(headers)
        
        result = self.manager.delete_sales_intake_job(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'SalesIntakeJob with id {id} not found.',
            )

        response_model: SalesIntakeJobOutboundModel =self.adapter.convert_from_model_to_outbound_model(result)

        return response_model
