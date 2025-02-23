import json
from typing import Any
from adapters.pos_simulator_response_adapters import PosSimulatorResponseDataAdapter
from adapters.retailer_adapters import RetailerDataAdapter
from adapters.retailer_location_adapters import RetailerLocationDataAdapter
from adapters.sales_intake_batch_job_adapters import SalesIntakeBatchJobDataAdapter
from models.inventory_intake_job_model import (
    InventoryIntakeJobCreateModel,
    InventoryIntakeJobInboundCreateModel,
    InventoryIntakeJobInboundSearchModel,
    InventoryIntakeJobInboundUpdateModel,
    InventoryIntakeJobModel,
    InventoryIntakeJobOutboundModel,
    InventoryIntakeJobSearchModel,
    InventoryIntakeJobUpdateModel,
)
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm, 
    RangeSearchTerm,
    SearchTerm,
)


class InventoryIntakeJobDataAdapter:
    def __init__(
        self,
        retailer_adapter : RetailerDataAdapter = RetailerDataAdapter(),
        retailer_location_adapter : RetailerLocationDataAdapter = RetailerLocationDataAdapter(),
        sales_intake_batch_job_adapter : SalesIntakeBatchJobDataAdapter = SalesIntakeBatchJobDataAdapter(),
        pos_simulator_response_adapter : PosSimulatorResponseDataAdapter = PosSimulatorResponseDataAdapter(),
        common_utilities: CommonUtilities = CommonUtilities()
    ) -> None:
        
        self.retailer_adapter = retailer_adapter
        self.retailer_location_adapter = retailer_location_adapter
        self.pos_simulator_response_adapter = pos_simulator_response_adapter
        self.sales_intake_batch_job_adapter = sales_intake_batch_job_adapter
        self.common_utilities = common_utilities
        
    def convert_from_inbound_create_model_to_create_model(
        self, 
        inbound_create_model: InventoryIntakeJobInboundCreateModel
    ) -> InventoryIntakeJobCreateModel:
        
        model = InventoryIntakeJobCreateModel( 
            retailer_id=None,
            retailer_location_id=inbound_create_model.retailer_location_id,
            simulator_response_id=inbound_create_model.simulator_response_id,
            parent_batch_job_id=inbound_create_model.parent_batch_job_id,
            snapshot_hour=inbound_create_model.snapshot_hour,
            status=inbound_create_model.status,
            status_details=inbound_create_model.status_details,
        )

        return model

    def convert_from_inbound_update_model_to_update_model(
        self, 
        inbound_update_model: InventoryIntakeJobInboundUpdateModel
    ) -> InventoryIntakeJobUpdateModel:
       
        model = InventoryIntakeJobUpdateModel(
            status=inbound_update_model.status,
            status_details=inbound_update_model.status_details,
        )

        return model

    def convert_from_inbound_search_model_to_search_model(
        self, 
        inbound_search_model: InventoryIntakeJobInboundSearchModel
    ) -> InventoryIntakeJobSearchModel:
        
        model = InventoryIntakeJobSearchModel(
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
            snapshot_hour_min=inbound_search_model.snapshot_hour_min,
            snapshot_hour_max=inbound_search_model.snapshot_hour_max, 
            status=inbound_search_model.status,
        )

        return model

    def convert_from_search_model_to_search_terms(
        self, 
        model: InventoryIntakeJobSearchModel
    ) -> list[SearchTerm]:
        
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(InListSearchTerm('id', self.common_utilities.convert_uuid_list_to_string_list(model.ids)))
                    
        if model.retailer_ids is not None:
            search_terms.append(InListSearchTerm('retailer_id', self.common_utilities.convert_uuid_list_to_string_list(model.retailer_ids)))
                    
        if model.retailer_location_ids is not None:
            search_terms.append(InListSearchTerm('retailer_location_id', self.common_utilities.convert_uuid_list_to_string_list(model.retailer_location_ids)))
             
        if model.parent_batch_job_ids  is not None:
            search_terms.append(InListSearchTerm('parent_batch_job_id', self.common_utilities.convert_uuid_list_to_string_list(model.parent_batch_job_ids)))
            
        if model.status is not None:
            search_terms.append(ExactMatchSearchTerm('status', model.status.value, True))
        
        if model.snapshot_hour_min is not None or model.snapshot_hour_max is not None:
            search_terms.append(RangeSearchTerm('snapshot_hour', model.snapshot_hour_min, model.snapshot_hour_max))

        return search_terms

    def convert_from_create_model_to_database_model(
        self, 
        model: InventoryIntakeJobCreateModel
    ) -> dict[str, Any]:
       
        database_model: dict[str, Any] = {
            'retailer_id': str(model.retailer_id) if model.retailer_id is not None else None ,
            'retailer_location_id': str(model.retailer_location_id) if model.retailer_location_id is not None else None ,
            'parent_batch_job_id': str(model.parent_batch_job_id) if model.parent_batch_job_id is not None else None ,
            'simulator_response_id': str(model.simulator_response_id) if model.simulator_response_id is not None else None ,
            'snapshot_hour': model.snapshot_hour,
            'status': model.status.value if model.status is not None else None, 
            'status_details': json.dumps(model.status_details) if model.status_details is not None else None,
        }

        return database_model

    def convert_from_update_model_to_database_model(
        self, 
        model: InventoryIntakeJobUpdateModel
    ) -> dict[str, Any]:
        
        database_model: dict[str, Any] = {
            'status': model.status.value if model.status is not None else None,
            'status_details': json.dumps(model.status_details) if model.status_details is not None else None,
            
        }

        return database_model

    def convert_from_database_model_to_model(
        self, 
        database_model: dict[str, Any]
    ) -> InventoryIntakeJobModel:
        
        model = InventoryIntakeJobModel(
            id=database_model['id'],
            retailer_id=database_model['retailer_id'],
            retailer_location_id=database_model['retailer_location_id'],
            parent_batch_job_id=database_model['parent_batch_job_id'],
            simulator_response_id=database_model['simulator_response_id'],
            snapshot_hour=database_model['snapshot_hour'],
            status=database_model['status'],
            status_details=database_model['status_details'],
            created_at=database_model['created_at'],
            updated_at=database_model['updated_at'],
        )

        return model

    def convert_from_model_to_outbound_model(
        self, 
        model: InventoryIntakeJobModel
    ) -> InventoryIntakeJobOutboundModel:
        
        outbound_model = InventoryIntakeJobOutboundModel(
            id=model.id,
            retailer_id=model.retailer_id,
            retailer=self.retailer_adapter.convert_from_model_to_outbound_model(model.retailer) if model.retailer is not None else None,
            retailer_location_id=model.retailer_location_id,
            retailer_location=self.retailer_location_adapter.convert_from_model_to_outbound_model(model.retailer_location) if model.retailer_location is not None else None,
            parent_batch_job_id=model.parent_batch_job_id,
            parent_batch_job=self.sales_intake_batch_job_adapter.convert_from_model_to_outbound_model(model.parent_batch_job) if model.parent_batch_job is not None else None,
            simulator_response_id=model.simulator_response_id,
            simulator_response=self.pos_simulator_response_adapter.convert_from_model_to_outbound_model(model.simulator_response) if model.simulator_response is not None else None,
            snapshot_hour=model.snapshot_hour.isoformat(timespec='milliseconds').replace('+00:00','Z'),
            status=model.status,
            status_details=model.status_details,
            created_at=model.created_at.isoformat(timespec='milliseconds').replace('+00:00','Z'),
            updated_at=model.updated_at.isoformat(timespec='milliseconds').replace('+00:00','Z') if model.updated_at is not None else None,
        )

        return outbound_model
