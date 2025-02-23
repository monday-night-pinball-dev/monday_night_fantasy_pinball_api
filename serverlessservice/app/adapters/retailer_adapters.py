from typing import Any
from models.retailer_model import (
    RetailerCreateModel,
    RetailerInboundCreateModel,
    RetailerInboundSearchModel,
    RetailerInboundUpdateModel,
    RetailerModel,
    RetailerOutboundModel,
    RetailerSearchModel,
    RetailerUpdateModel,
)
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm,
    LikeComparatorModes,
    LikeSearchTerm,
    SearchTerm,
)


class RetailerDataAdapter:

    def __init__(
        self,
        common_utilities: CommonUtilities = CommonUtilities()
    ) -> None:
        
        self.common_utilities = common_utilities

    def convert_from_inbound_create_model_to_create_model(
        self, 
        inbound_create_model: RetailerInboundCreateModel
    ) -> RetailerCreateModel:
       
        model = RetailerCreateModel(
            name=inbound_create_model.name,
            hq_state=inbound_create_model.hq_state,
            hq_city=inbound_create_model.hq_city,
            hq_country=inbound_create_model.hq_country,
            contact_email=inbound_create_model.contact_email,
            account_status=inbound_create_model.account_status,
        )

        return model

    def convert_from_inbound_update_model_to_update_model(
        self, 
        inbound_update_model: RetailerInboundUpdateModel
    ) -> RetailerUpdateModel:
        
        model = RetailerUpdateModel(
            name=inbound_update_model.name,
            hq_state=inbound_update_model.hq_state,
            hq_city=inbound_update_model.hq_city,
            hq_country=inbound_update_model.hq_country,
            contact_email=inbound_update_model.contact_email,
            account_status=inbound_update_model.account_status,
        )

        return model

    def convert_from_inbound_search_model_to_search_model(
        self, 
        inbound_search_model: RetailerInboundSearchModel
    ) -> RetailerSearchModel:
        
        model = RetailerSearchModel(
            ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.ids)
                if inbound_search_model.ids is not None
                else 
                    None
            ),
            name=inbound_search_model.name,
            name_like=inbound_search_model.name_like,
            account_status = inbound_search_model.account_status,
            hq_state=inbound_search_model.hq_state,
            hq_city=inbound_search_model.hq_city,
            hq_country=inbound_search_model.hq_country,
        )

        return model

    def convert_from_search_model_to_search_terms(
        self, 
        model: RetailerSearchModel
    ) -> list[SearchTerm]:
        
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(InListSearchTerm('id', self.common_utilities.convert_uuid_list_to_string_list(model.ids)))
            
        if model.name is not None:
            search_terms.append(ExactMatchSearchTerm('name', model.name, True))
            
        if model.name_like is not None:
            search_terms.append(LikeSearchTerm('name', model.name_like, LikeComparatorModes.Like, True))
            
        if model.account_status is not None:
            search_terms.append(ExactMatchSearchTerm('account_status', model.account_status.value, True))
            
        if model.hq_state is not None:
            search_terms.append(ExactMatchSearchTerm('hq_state', model.hq_state, True))
            
        if model.hq_city is not None:
            search_terms.append(ExactMatchSearchTerm('hq_city', model.hq_city, True))
            
        if model.hq_country is not None:
            search_terms.append(ExactMatchSearchTerm('hq_country', model.hq_country, True))

        return search_terms

    def convert_from_create_model_to_database_model(
        self, 
        model: RetailerCreateModel
    ) -> dict[str, Any]:
        
        database_model: dict[str, Any] = {
            'name': model.name,
            'hq_state': model.hq_state,
            'hq_city': model.hq_city,
            'hq_country': model.hq_country,
            'contact_email': model.contact_email,
            'account_status': model.account_status.value if model.account_status is not None else None,
        }

        return database_model

    def convert_from_update_model_to_database_model(
        self, 
        model: RetailerUpdateModel
    ) -> dict[str, Any]:
        
        database_model: dict[str, Any] = {
            'name': model.name,
            'hq_state': model.hq_state,
            'hq_city': model.hq_city,
            'hq_country': model.hq_country,
            'contact_email': model.contact_email,
            'account_status': model.account_status.value if model.account_status is not None else None,
        }

        return database_model

    def convert_from_database_model_to_model(
        self,
        database_model: dict[str, Any]
    ) -> RetailerModel:
        
        model = RetailerModel(
            id=database_model['id'],
            name=database_model['name'],
            hq_state=database_model['hq_state'],
            hq_city=database_model['hq_city'],
            hq_country=database_model['hq_country'],
            contact_email=database_model['contact_email'],
            account_status=database_model['account_status'],
            created_at=database_model['created_at'],
            updated_at=database_model['updated_at'],
        )

        return model

    def convert_from_model_to_outbound_model(
        self, 
        model: RetailerModel
    ) -> RetailerOutboundModel:
        
        outbound_model = RetailerOutboundModel(
            id=model.id,
            name=model.name,
            hq_state=model.hq_state,
            hq_city=model.hq_city,
            hq_country=model.hq_country,
            contact_email=model.contact_email,
            account_status=model.account_status,
            created_at=model.created_at.isoformat(timespec='milliseconds').replace('+00:00','Z'),
            updated_at=model.updated_at.isoformat(timespec='milliseconds').replace('+00:00','Z') if model.updated_at is not None else None,
        )

        return outbound_model
