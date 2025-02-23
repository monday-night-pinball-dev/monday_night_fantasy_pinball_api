import json
from typing import Any
from adapters.retailer_adapters import RetailerDataAdapter
from adapters.retailer_location_adapters import RetailerLocationDataAdapter
from adapters.sales_intake_batch_job_adapters import SalesIntakeBatchJobDataAdapter
from models.sales_intake_job_model import (
    SalesIntakeJobCreateModel,
    SalesIntakeJobInboundCreateModel,
    SalesIntakeJobInboundSearchModel,
    SalesIntakeJobInboundUpdateModel,
    SalesIntakeJobModel,
    SalesIntakeJobOutboundModel,
    SalesIntakeJobSearchModel,
    SalesIntakeJobUpdateModel,
)
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm,
    LikeComparatorModes,
    LikeSearchTerm,
    RangeSearchTerm,
    SearchTerm,
)
 
class SalesIntakeJobDataAdapter:

    def __init__(
        self,
        retailer_adapter : RetailerDataAdapter = RetailerDataAdapter(),
        retailer_location_adapter : RetailerLocationDataAdapter = RetailerLocationDataAdapter(),
        sales_intake_batch_job_adapter : SalesIntakeBatchJobDataAdapter = SalesIntakeBatchJobDataAdapter(),
        common_utilities: CommonUtilities = CommonUtilities()
    ) -> None:
        
        self.retailer_adapter = retailer_adapter
        self.retailer_location_adapter = retailer_location_adapter
        self.sales_intake_batch_job_adapter = sales_intake_batch_job_adapter
        self.common_utilities = common_utilities
        
    def convert_from_inbound_create_model_to_create_model(
        self, 
        inbound_create_model: SalesIntakeJobInboundCreateModel
    ) -> SalesIntakeJobCreateModel:
        
        model = SalesIntakeJobCreateModel( 
            retailer_id=None,
            retailer_location_id=inbound_create_model.retailer_location_id,
            parent_batch_job_id=inbound_create_model.parent_batch_job_id,
            start_time=inbound_create_model.start_time,
            end_time=inbound_create_model.end_time,
            status=inbound_create_model.status,
            status_details=inbound_create_model.status_details,
        )

        return model

    def convert_from_inbound_update_model_to_update_model(
        self, 
        inbound_update_model: SalesIntakeJobInboundUpdateModel
    ) -> SalesIntakeJobUpdateModel:
       
        model = SalesIntakeJobUpdateModel(
            status=inbound_update_model.status,
            status_details=inbound_update_model.status_details,
        )

        return model

    def convert_from_inbound_search_model_to_search_model(
        self, 
        inbound_search_model: SalesIntakeJobInboundSearchModel
    ) -> SalesIntakeJobSearchModel:
        
        model = SalesIntakeJobSearchModel(
            ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.ids)
                if inbound_search_model.ids is not None 
                else 
                    None
            ),
            retailer_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.retailer_ids)
                if inbound_search_model.retailer_ids is not None 
                else 
                    None
            ),
            retailer_location_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.retailer_location_ids)
                if inbound_search_model.retailer_location_ids is not None 
                else 
                    None
            ), 
            parent_batch_job_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.parent_batch_job_ids)
                if inbound_search_model.parent_batch_job_ids is not None 
                else 
                    None
            ),        
            status=inbound_search_model.status,
        )

        return model

    def convert_from_search_model_to_search_terms(
        self, 
        model: SalesIntakeJobSearchModel
    ) -> list[SearchTerm]:
        
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(InListSearchTerm('id', self.common_utilities.convert_uuid_list_to_string_list(model.ids)))
                    
        if model.retailer_ids is not None:
            search_terms.append(InListSearchTerm('retailer_id', self.common_utilities.convert_uuid_list_to_string_list(model.retailer_ids)))
                    
        if model.retailer_location_ids is not None:
            search_terms.append(InListSearchTerm('retailer_location_id', self.common_utilities.convert_uuid_list_to_string_list(model.retailer_location_ids)))
            
        if model.parent_batch_job_ids is not None:
            search_terms.append(InListSearchTerm('parent_batch_job_id', self.common_utilities.convert_uuid_list_to_string_list(model.parent_batch_job_ids)))
            
        if model.status is not None:
            search_terms.append(ExactMatchSearchTerm('status', model.status.value, True))
 

        return search_terms

    def convert_from_create_model_to_database_model(
        self, 
        model: SalesIntakeJobCreateModel
    ) -> dict[str, Any]:
       
        database_model: dict[str, Any] = {
            'retailer_id': str(model.retailer_id) if model.retailer_id is not None else None ,
            'retailer_location_id': str(model.retailer_location_id) if model.retailer_location_id is not None else None ,
            'parent_batch_job_id': str(model.parent_batch_job_id) if model.parent_batch_job_id is not None else None ,
            'start_time': model.start_time,
            'end_time': model.end_time,
            'status': model.status.value if model.status is not None else None, 
            'status_details': json.dumps(model.status_details) if model.status_details is not None else None,
        }

        return database_model

    def convert_from_update_model_to_database_model(
        self, 
        model: SalesIntakeJobUpdateModel
    ) -> dict[str, Any]:
        
        database_model: dict[str, Any] = {
            'status': model.status.value if model.status is not None else None,
            'status_details': json.dumps(model.status_details) if model.status_details is not None else None, 
        }

        return database_model

    def convert_from_database_model_to_model(
        self, 
        database_model: dict[str, Any]
    ) -> SalesIntakeJobModel:
        
        model = SalesIntakeJobModel(
            id=database_model['id'],
            retailer_id=database_model['retailer_id'],
            retailer_location_id=database_model['retailer_location_id'],
            parent_batch_job_id=database_model['parent_batch_job_id'],
            start_time=database_model['start_time'],    
            end_time=database_model['end_time'],
            status=database_model['status'],
            status_details=database_model['status_details'],
            created_at=database_model['created_at'],
            updated_at=database_model['updated_at'],
        )

        return model

    def convert_from_model_to_outbound_model(
        self, 
        model: SalesIntakeJobModel
    ) -> SalesIntakeJobOutboundModel:
        
        outbound_model = SalesIntakeJobOutboundModel(
            id=model.id,
            retailer_id=model.retailer_id, 
            retailer = self.retailer_adapter.convert_from_model_to_outbound_model(model.retailer) if model.retailer is not None else None,
            retailer_location_id=model.retailer_location_id, 
            retailer_location = self.retailer_location_adapter.convert_from_model_to_outbound_model(model.retailer_location) if model.retailer_location is not None else None,
            parent_batch_job_id=model.parent_batch_job_id,
            parent_batch_job=self.sales_intake_batch_job_adapter.convert_from_model_to_outbound_model(model.parent_batch_job) if model.parent_batch_job is not None else None,
            start_time=model.start_time.isoformat(timespec='milliseconds').replace('+00:00','Z'),
            end_time=model.end_time.isoformat(timespec='milliseconds').replace('+00:00','Z'),
            status=model.status,
            status_details=model.status_details,
            created_at=model.created_at.isoformat(timespec='milliseconds').replace('+00:00','Z'),
            updated_at=model.updated_at.isoformat(timespec='milliseconds').replace('+00:00','Z') if model.updated_at is not None else None,
        )

        return outbound_model
