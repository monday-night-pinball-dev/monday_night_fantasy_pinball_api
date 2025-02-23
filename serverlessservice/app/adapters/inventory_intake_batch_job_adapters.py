import json
from typing import Any
from models.inventory_intake_batch_job_model import (
    InventoryIntakeBatchJobCreateModel,
    InventoryIntakeBatchJobInboundCreateModel,
    InventoryIntakeBatchJobInboundSearchModel,
    InventoryIntakeBatchJobInboundUpdateModel,
    InventoryIntakeBatchJobModel,
    InventoryIntakeBatchJobOutboundModel,
    InventoryIntakeBatchJobSearchModel,
    InventoryIntakeBatchJobUpdateModel,
)
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm, 
    RangeSearchTerm,
    SearchTerm,
)


class InventoryIntakeBatchJobDataAdapter:
    

    def __init__(
        self,
        common_utilities: CommonUtilities = CommonUtilities()
    ) -> None:
        
        self.common_utilities = common_utilities

    def convert_from_inbound_create_model_to_create_model(
        self, 
        inbound_create_model: InventoryIntakeBatchJobInboundCreateModel
    ) -> InventoryIntakeBatchJobCreateModel:
        
        model = InventoryIntakeBatchJobCreateModel(   
            restricted_retailer_location_ids = self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_create_model.restricted_retailer_location_ids),
            status=inbound_create_model.status,
            status_details=inbound_create_model.status_details,
        )

        return model

    def convert_from_inbound_update_model_to_update_model(
        self, 
        inbound_update_model: InventoryIntakeBatchJobInboundUpdateModel
    ) -> InventoryIntakeBatchJobUpdateModel:
       
        model = InventoryIntakeBatchJobUpdateModel(
            status=inbound_update_model.status,
            status_details=inbound_update_model.status_details,
        )

        return model

    def convert_from_inbound_search_model_to_search_model(
        self, 
        inbound_search_model: InventoryIntakeBatchJobInboundSearchModel
    ) -> InventoryIntakeBatchJobSearchModel:
        
        model = InventoryIntakeBatchJobSearchModel(
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
        model: InventoryIntakeBatchJobSearchModel
    ) -> list[SearchTerm]:
    
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(InListSearchTerm('id', self.common_utilities.convert_uuid_list_to_string_list(model.ids)))
  
        if model.status is not None:
            search_terms.append(ExactMatchSearchTerm('status', model.status.value, True))
  
        return search_terms

    def convert_from_create_model_to_database_model(
        self, 
        model: InventoryIntakeBatchJobCreateModel
    ) -> dict[str, Any]:
    
        database_model: dict[str, Any] = {  
            'restricted_retailer_location_ids': ",".join(str(x) for x in model.restricted_retailer_location_ids) if model.restricted_retailer_location_ids is not None else None,
            'status': model.status.value if model.status is not None else None, 
            'status_details': json.dumps(model.status_details) if model.status_details is not None else None,
        }

        return database_model

    def convert_from_update_model_to_database_model(
        self, 
        model: InventoryIntakeBatchJobUpdateModel
    ) -> dict[str, Any]:
    
        database_model: dict[str, Any] = {
            'status': model.status.value if model.status is not None else None,
            'status_details': json.dumps(model.status_details) if model.status_details is not None else None,
            
        }

        return database_model

    def convert_from_database_model_to_model(
        self, 
        database_model: dict[str, Any]
    ) -> InventoryIntakeBatchJobModel:
        
        model = InventoryIntakeBatchJobModel(
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
        model: InventoryIntakeBatchJobModel
    ) -> InventoryIntakeBatchJobOutboundModel:
        
        outbound_model = InventoryIntakeBatchJobOutboundModel(
            id=model.id, 
            status=model.status,
            status_details=model.status_details,
            restricted_retailer_location_ids =  model.restricted_retailer_location_ids,
            created_at=model.created_at.isoformat(timespec='milliseconds').replace('+00:00','Z'),
            updated_at=model.updated_at.isoformat(timespec='milliseconds').replace('+00:00','Z') if model.updated_at is not None else None,
        )

        return outbound_model
