import json
from typing import Any
from models.sales_intake_batch_job_model import (
    SalesIntakeBatchJobCreateModel,
    SalesIntakeBatchJobInboundCreateModel,
    SalesIntakeBatchJobInboundSearchModel,
    SalesIntakeBatchJobInboundUpdateModel,
    SalesIntakeBatchJobModel,
    SalesIntakeBatchJobOutboundModel,
    SalesIntakeBatchJobSearchModel,
    SalesIntakeBatchJobUpdateModel,
)
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm, 
    RangeSearchTerm,
    SearchTerm,
)


class SalesIntakeBatchJobDataAdapter:

    def __init__(
        self, 
        common_utilities: CommonUtilities = CommonUtilities()
    ) -> None: 
        self.common_utilities = common_utilities
        
        
    def convert_from_inbound_create_model_to_create_model(
        self, 
        inbound_create_model: SalesIntakeBatchJobInboundCreateModel
    ) -> SalesIntakeBatchJobCreateModel:
        
        model = SalesIntakeBatchJobCreateModel(   
            restricted_retailer_location_ids = self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_create_model.restricted_retailer_location_ids),
            status=inbound_create_model.status,
            status_details=inbound_create_model.status_details,
        )

        return model

    def convert_from_inbound_update_model_to_update_model(
        self, 
        inbound_update_model: SalesIntakeBatchJobInboundUpdateModel
    ) -> SalesIntakeBatchJobUpdateModel:
       
        model = SalesIntakeBatchJobUpdateModel(
            status=inbound_update_model.status,
            status_details=inbound_update_model.status_details,
        )

        return model

    def convert_from_inbound_search_model_to_search_model(
        self, 
        inbound_search_model: SalesIntakeBatchJobInboundSearchModel
    ) -> SalesIntakeBatchJobSearchModel:
        
        model = SalesIntakeBatchJobSearchModel(
            ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.ids)
                if inbound_search_model.ids is not None 
                else 
                    None
            ), 
            status=inbound_search_model.status,
        )

        return model

    def convert_from_search_model_to_search_terms(
        self, 
        model: SalesIntakeBatchJobSearchModel
    ) -> list[SearchTerm]:
        
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(InListSearchTerm('id', self.common_utilities.convert_uuid_list_to_string_list(model.ids)))
 
        if model.status is not None:
            search_terms.append(ExactMatchSearchTerm('status', model.status.value, True))
  
        return search_terms

    def convert_from_create_model_to_database_model(
        self, 
        model: SalesIntakeBatchJobCreateModel
    ) -> dict[str, Any]:
       
        database_model: dict[str, Any] = {  
            'restricted_retailer_location_ids': ",".join(str(x) for x in model.restricted_retailer_location_ids) if model.restricted_retailer_location_ids is not None else None,
            'status': model.status.value if model.status is not None else None, 
            'status_details': json.dumps(model.status_details) if model.status_details is not None else None,
        }

        return database_model

    def convert_from_update_model_to_database_model(
        self, 
        model: SalesIntakeBatchJobUpdateModel
    ) -> dict[str, Any]:
    
        database_model: dict[str, Any] = {
            'status': model.status.value if model.status is not None else None,
            'status_details': json.dumps(model.status_details) if model.status_details is not None else None,
            
        }

        return database_model

    def convert_from_database_model_to_model(
        self, 
        database_model: dict[str, Any]
    ) -> SalesIntakeBatchJobModel:
        
        model = SalesIntakeBatchJobModel(
            id=database_model['id'],   
            status=database_model['status'],
            status_details=database_model['status_details'],
            
            restricted_retailer_location_ids = database_model['restricted_retailer_location_ids'].split(',') if database_model['restricted_retailer_location_ids'] is not None else None,
            created_at=database_model['created_at'],
            updated_at=database_model['updated_at'],
        )

        return model

    def convert_from_model_to_outbound_model(
        self, 
        model: SalesIntakeBatchJobModel
    ) -> SalesIntakeBatchJobOutboundModel:
        
        outbound_model = SalesIntakeBatchJobOutboundModel(
            id=model.id, 
            status=model.status,
            status_details=model.status_details,
            restricted_retailer_location_ids =  model.restricted_retailer_location_ids,
            created_at=model.created_at.isoformat(timespec='milliseconds').replace('+00:00','Z'),
            updated_at=model.updated_at.isoformat(timespec='milliseconds').replace('+00:00','Z') if model.updated_at is not None else None,
        )

        return outbound_model
