from typing import Any
from models.vendor_model import (
    VendorCreateModel,
    VendorInboundCreateModel,
    VendorInboundSearchModel,
    VendorInboundUpdateModel,
    VendorModel,
    VendorOutboundModel,
    VendorSearchModel,
    VendorUpdateModel,
)
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm,
    LikeComparatorModes,
    LikeSearchTerm,
    SearchTerm,
)
 
class VendorDataAdapter: 

    def __init__(
        self,
        common_utilities: CommonUtilities = CommonUtilities()
    ) -> None:
        
        self.common_utilities = common_utilities
        
    def convert_from_inbound_create_model_to_create_model(
        self,
        inbound_create_model: VendorInboundCreateModel,
    ) -> VendorCreateModel:
        
        model = VendorCreateModel(
            name=inbound_create_model.name,
            unregistered_vendor_referring_retailer_location_id=inbound_create_model.unregistered_vendor_referring_retailer_location_id, 
            is_registered=inbound_create_model.is_registered,
            account_status=inbound_create_model.account_status,
            hq_state=inbound_create_model.hq_state,
            hq_city=inbound_create_model.hq_city,
            hq_country=inbound_create_model.hq_country,
            contact_email=inbound_create_model.contact_email,
            contact_phone=inbound_create_model.contact_phone,
        )

        return model

    def convert_from_inbound_update_model_to_update_model(
        self,
        inbound_update_model: VendorInboundUpdateModel,
    ) -> VendorUpdateModel:
        
        model = VendorUpdateModel(
            name=inbound_update_model.name,
            is_registered=inbound_update_model.is_registered,
            account_status=inbound_update_model.account_status,
            hq_state=inbound_update_model.hq_state,
            hq_city=inbound_update_model.hq_city,
            hq_country=inbound_update_model.hq_country,
            contact_email=inbound_update_model.contact_email,
            contact_phone=inbound_update_model.contact_phone,
        )

        return model

    def convert_from_inbound_search_model_to_search_model(
        self, 
        inbound_search_model: VendorInboundSearchModel
    ) -> VendorSearchModel:
        
        model = VendorSearchModel(
            ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.ids)
                if inbound_search_model.ids is not None
                else 
                    None
            ),
            unregistered_vendor_referring_retailer_location_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.unregistered_vendor_referring_retailer_location_ids)
                if inbound_search_model.unregistered_vendor_referring_retailer_location_ids
                is not None 
                else 
                    None
            ),  
            account_status=inbound_search_model.account_status,
            name=inbound_search_model.name,
            name_like=inbound_search_model.name_like,
            hq_state=inbound_search_model.hq_state,
            hq_city=inbound_search_model.hq_city,
            hq_country=inbound_search_model.hq_country,
        )

        return model

    def convert_from_search_model_to_search_terms(
        self, 
        model: VendorSearchModel
    ) -> list[SearchTerm]:
        
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(InListSearchTerm('id', self.common_utilities.convert_uuid_list_to_string_list(model.ids)))
  
        if model.unregistered_vendor_referring_retailer_location_ids is not None:
            search_terms.append(
                InListSearchTerm(
                    'unregistered_vendor_referring_retailer_location_id',
                    self.common_utilities.convert_uuid_list_to_string_list(model.unregistered_vendor_referring_retailer_location_ids),
                )
            )

        if model.name is not None:
            search_terms.append(ExactMatchSearchTerm('name', model.name, True))

        if model.name_like is not None:
            search_terms.append(
                LikeSearchTerm('name', model.name_like,
                               LikeComparatorModes.Like, True))
             
        if model.account_status is not None:
            search_terms.append(ExactMatchSearchTerm('account_status', model.account_status))

        if model.hq_state is not None:
            search_terms.append(
                ExactMatchSearchTerm('hq_state', model.hq_state, True))

        if model.hq_city is not None:
            search_terms.append(
                ExactMatchSearchTerm('hq_city', model.hq_city, True))

        if model.hq_country is not None:
            search_terms.append(
                ExactMatchSearchTerm('hq_country', model.hq_country, True))

        return search_terms

    def convert_from_create_model_to_database_model(
        self, 
        model: VendorCreateModel
    ) -> dict[str, Any]:
        
        database_model: dict[str, Any] = {
            'name': model.name,
            'unregistered_vendor_referring_retailer_location_id': str(model.unregistered_vendor_referring_retailer_location_id) if model.unregistered_vendor_referring_retailer_location_id is not None else None,
            'is_registered': model.is_registered,
            'account_status': model.account_status.value if model.account_status is not None else None,
            'hq_state': model.hq_state,
            'hq_city': model.hq_city,
            'hq_country': model.hq_country,
            'contact_email': model.contact_email,
            'contact_phone': model.contact_phone,
        }

        return database_model

    def convert_from_update_model_to_database_model(
        self, 
        model: VendorUpdateModel
    ) -> dict[str, Any]:
        
        database_model: dict[str, Any] = {
            'name': model.name,
            'is_registered': model.is_registered,
            'account_status': model.account_status.value if model.account_status is not None else None,
            'hq_state': model.hq_state,
            'hq_city': model.hq_city,
            'hq_country': model.hq_country,
            'contact_email': model.contact_email,
            'contact_phone': model.contact_phone,
        }

        return database_model

    def convert_from_database_model_to_model(
        self, 
        database_model: dict[str, Any]
    ) -> VendorModel:
        
        model = VendorModel(
            id=database_model['id'],
            name=database_model['name'], 
            unregistered_vendor_referring_retailer_location_id=database_model['unregistered_vendor_referring_retailer_location_id'],
            is_registered=database_model['is_registered'],
            account_status=database_model['account_status'],
            hq_state=database_model['hq_state'],
            hq_city=database_model['hq_city'],
            hq_country=database_model['hq_country'],
            contact_email=database_model['contact_email'],
            contact_phone=database_model['contact_phone'],
            created_at=database_model['created_at'],
            updated_at=database_model['updated_at'],
        )

        return model

    def convert_from_model_to_outbound_model(
        self, 
        model: VendorModel
    ) -> VendorOutboundModel:
        
        outbound_model = VendorOutboundModel(
            id=model.id,
            name=model.name, 
            unregistered_vendor_referring_retailer_location_id=model. unregistered_vendor_referring_retailer_location_id,
            is_registered=model.is_registered,
            account_status=model.account_status,
            hq_state=model.hq_state,
            hq_city=model.hq_city,
            hq_country=model.hq_country,
            contact_email=model.contact_email,
            contact_phone=model.contact_phone,
            created_at=model.created_at.isoformat(timespec='milliseconds').replace('+00:00','Z'),
            updated_at=model.updated_at.isoformat(timespec='milliseconds').replace('+00:00','Z')    if model.updated_at is not None else None,
        )

        return outbound_model
