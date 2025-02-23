import json
from typing import Any

from pydantic import ValidationError
from adapters.pos_integration_adapters import PosIntegrationDataAdapter
from adapters.retailer_adapters import RetailerDataAdapter
from adapters.retailer_location_adapters import RetailerLocationDataAdapter
from models.pos_simulator_response_model import (
    PosSimulatorResponseCreateModel,
    PosSimulatorResponseInboundCreateModel,
    PosSimulatorResponseInboundSearchModel, 
    PosSimulatorResponseModel,
    PosSimulatorResponseOutboundModel,
    PosSimulatorResponseSearchModel, 
)
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm, 
    SearchTerm,
)


class PosSimulatorResponseDataAdapter: 
    
    def __init__(
        self,
        common_utilities: CommonUtilities = CommonUtilities()
    ) -> None:
        
        self.common_utilities = common_utilities

    def convert_from_inbound_create_model_to_create_model(
        self, 
        inbound_create_model: PosSimulatorResponseInboundCreateModel
    ) -> PosSimulatorResponseCreateModel:
        
        model = PosSimulatorResponseCreateModel(
            action_type=inbound_create_model.action_type,
            response_status_code=inbound_create_model.response_status_code,
            response_body=inbound_create_model.response_body,
            description=inbound_create_model.description
        )

        return model
 
    def convert_from_inbound_search_model_to_search_model(
        self, 
        inbound_search_model: PosSimulatorResponseInboundSearchModel
    ) -> PosSimulatorResponseSearchModel:
        
        model = PosSimulatorResponseSearchModel(
            ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.ids)
                if inbound_search_model.ids is not None 
                else 
                    None
            ) 
        )

        return model

    def convert_from_search_model_to_search_terms(
        self, 
        model: PosSimulatorResponseSearchModel
    ) -> list[SearchTerm]:
        
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(InListSearchTerm('id', self.common_utilities.convert_uuid_list_to_string_list(model.ids)))
                     
        return search_terms

    def convert_from_create_model_to_database_model(
        self, 
        model: PosSimulatorResponseCreateModel
    ) -> dict[str, Any]:
       
        database_model: dict[str, Any] = { 
            'action_type': model.action_type.value if model.action_type is not None else None,
            'response_status_code': model.response_status_code,
            'response_body': json.dumps(model.response_body) if model.response_body is not None else None,
            'description': model.description,
        }

        return database_model
 
    def convert_from_database_model_to_model(
        self,
        database_model: dict[str, Any]
    ) -> PosSimulatorResponseModel:
        
        model = PosSimulatorResponseModel(
            id=database_model['id'],
            response_status_code=database_model['response_status_code'],
            action_type=database_model['action_type'],
            description=database_model['description'],
            response_body=database_model['response_body'],
            created_at=database_model['created_at'],
            updated_at=database_model['updated_at'],
        )

        return model

    def convert_from_model_to_outbound_model(
        self, 
        model: PosSimulatorResponseModel
    ) -> PosSimulatorResponseOutboundModel:
         
        outbound_model = PosSimulatorResponseOutboundModel(
            id=model.id,
            response_status_code=model.response_status_code, 
            action_type=model.action_type,
            response_body=model.response_body,
            description=model.description,
            created_at=model.created_at.isoformat(timespec='milliseconds').replace('+00:00','Z'),
            updated_at=model.updated_at.isoformat(timespec='milliseconds').replace('+00:00','Z') if model.updated_at is not None else None,
        )

        
        return outbound_model
