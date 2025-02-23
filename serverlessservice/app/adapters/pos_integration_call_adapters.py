import json
from typing import Any
from adapters.pos_integration_adapters import PosIntegrationDataAdapter
from adapters.retailer_adapters import RetailerDataAdapter
from adapters.retailer_location_adapters import RetailerLocationDataAdapter
from models.pos_integration_call_model import (
    PosIntegrationCallCreateModel,
    PosIntegrationCallInboundCreateModel,
    PosIntegrationCallInboundSearchModel, 
    PosIntegrationCallModel,
    PosIntegrationCallOutboundModel,
    PosIntegrationCallSearchModel, 
)
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm, 
    SearchTerm,
)


class PosIntegrationCallDataAdapter: 
    
    def __init__(
        self,
        common_utilities: CommonUtilities = CommonUtilities(),
        retailer_adapter: RetailerDataAdapter = RetailerDataAdapter(),
        retailer_location_adapter: RetailerLocationDataAdapter = RetailerLocationDataAdapter(),
        pos_integration_adapter: PosIntegrationDataAdapter = PosIntegrationDataAdapter(),
    ) -> None:
        
        self.common_utilities = common_utilities
        self.retailer_adapter = retailer_adapter
        self.retailer_location_adapter = retailer_location_adapter
        self.pos_integration_adapter = pos_integration_adapter

    def convert_from_inbound_create_model_to_create_model(
        self, 
        inbound_create_model: PosIntegrationCallInboundCreateModel
    ) -> PosIntegrationCallCreateModel:
        
        model = PosIntegrationCallCreateModel(
            pos_integration_id = inbound_create_model.pos_integration_id,
            request = inbound_create_model.request,
            response = inbound_create_model.response,
            response_status_code = inbound_create_model.response_status_code,
        )

        return model
 
    def convert_from_inbound_search_model_to_search_model(
        self, 
        inbound_search_model: PosIntegrationCallInboundSearchModel
    ) -> PosIntegrationCallSearchModel:
        
        model = PosIntegrationCallSearchModel(
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
            pos_integration_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.pos_integration_ids)
                if inbound_search_model.pos_integration_ids is not None 
                else 
                    None
            ), 
            response_status_code=inbound_search_model.response_status_code,
        )

        return model

    def convert_from_search_model_to_search_terms(
        self, 
        model: PosIntegrationCallSearchModel
    ) -> list[SearchTerm]:
        
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(InListSearchTerm('id', self.common_utilities.convert_uuid_list_to_string_list(model.ids)))
                    
        if model.retailer_ids is not None:
            search_terms.append(InListSearchTerm('retailer_id', self.common_utilities.convert_uuid_list_to_string_list(model.retailer_ids)))
                    
        if model.retailer_location_ids is not None:
            search_terms.append(InListSearchTerm('retailer_location_id', self.common_utilities.convert_uuid_list_to_string_list(model.retailer_location_ids)))
            
        if model.pos_integration_ids is not None:
            search_terms.append(InListSearchTerm('pos_integration_id', self.common_utilities.convert_uuid_list_to_string_list(model.pos_integration_ids)))
            
        if model.response_status_code is not None:
            search_terms.append(ExactMatchSearchTerm('response_status_code', model.response_status_code, True))
             
        return search_terms

    def convert_from_create_model_to_database_model(
        self, 
        model: PosIntegrationCallCreateModel
    ) -> dict[str, Any]:
       
        database_model: dict[str, Any] = { 
            'retailer_id': str(model.retailer_id) if model.retailer_id is not None else None,
            'retailer_location_id': str(model.retailer_location_id) if model.retailer_location_id is not None else None,
            'pos_integration_id': str(model.pos_integration_id) if model.pos_integration_id is not None else None,
            'request': json.dumps(model.request) if model.request is not None else None,
            'response': json.dumps(model.response) if model.response is not None else None,
            'response_status_code': model.response_status_code, 
        }

        return database_model
 
    def convert_from_database_model_to_model(
        self,
        database_model: dict[str, Any]
    ) -> PosIntegrationCallModel:
        
        model = PosIntegrationCallModel(
            id=database_model['id'],
            retailer_id=database_model['retailer_id'],
            retailer_location_id=database_model['retailer_location_id'],
            pos_integration_id=database_model['pos_integration_id'],
            request=database_model['request'],
            response=database_model['response'],
            response_status_code=database_model['response_status_code'],
            created_at=database_model['created_at'],
            updated_at=database_model['updated_at'],
        )

        return model

    def convert_from_model_to_outbound_model(
        self, 
        model: PosIntegrationCallModel
    ) -> PosIntegrationCallOutboundModel:
        
        outbound_model = PosIntegrationCallOutboundModel(
            id=model.id,
            retailer_id=model.retailer_id,
            retailer=self.retailer_adapter.convert_from_model_to_outbound_model(model.retailer) if model.retailer is not None else None,
            retailer_location_id=model.retailer_location_id,
            retailer_location=self.retailer_location_adapter.convert_from_model_to_outbound_model(model.retailer_location) if model.retailer_location is not None else None,
            pos_integration_id=model.pos_integration_id,
            pos_integration=self.pos_integration_adapter.convert_from_model_to_outbound_model(model.pos_integration) if model.pos_integration is not None else None,
            request=model.request,
            response=model.response,
            response_status_code=model.response_status_code,
            created_at=model.created_at.isoformat(timespec='milliseconds').replace('+00:00','Z'),
            updated_at=model.updated_at.isoformat(timespec='milliseconds').replace('+00:00','Z') if model.updated_at is not None else None,
        )

        return outbound_model
