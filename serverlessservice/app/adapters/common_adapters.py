from typing import Any

from fastapi.datastructures import Headers 

from models.common_model import (
    CommonInboundPagedModel,
    OutboundResultantPagingModel,
)
from util.database import PagingModel, ResultantPagingModel
from util.common import RequestOperators
 
class CommonAdapters:
    
    def convert_from_headers_to_operators(
        self, 
        headers: Headers
    ) -> RequestOperators:
        
        requestOperators = RequestOperators()
        
        samson_hydration = headers.get("Samson-Hydration")
        
        if(samson_hydration is not None):
            requestOperators.hydration = samson_hydration.split(",")

        return requestOperators
        
    def convert_from_paged_inbound_model_to_paging_model(
        self, 
        inbound_model: CommonInboundPagedModel
    ) -> PagingModel:

        model = PagingModel(
            page=inbound_model.page,
            page_length=inbound_model.page_length,
            sort_by=inbound_model.sort_by,
            is_sort_descending=inbound_model.is_sort_descending,
        )

        return model

    def convert_from_paging_model_to_outbound_paging_model(
        self, 
        model: ResultantPagingModel
    ) -> OutboundResultantPagingModel:

        outbound_model = OutboundResultantPagingModel(
            page=model.page,
            page_length=model.page_length,
            sort_by=model.sort_by,
            is_sort_descending=model.is_sort_descending,
            total_record_count=model.total_record_count,
        )

        return outbound_model
