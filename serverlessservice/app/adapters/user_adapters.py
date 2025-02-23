from typing import Any
from models.user_model import (
    UserCreateModel,
    UserInboundCreateModel,
    UserInboundSearchModel,
    UserInboundUpdateModel,
    UserModel,
    UserOutboundModel,
    UserSearchModel,
    UserUpdateModel,
)
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm,
    LikeComparatorModes,
    LikeSearchTerm,
    SearchTerm,
)
 
class UserDataAdapter: 
    
    def __init__(
        self,
        common_utilities: CommonUtilities = CommonUtilities()
    ) -> None:
        
        self.common_utilities = common_utilities

    def convert_from_inbound_create_model_to_create_model(
        self,
        inbound_create_model: UserInboundCreateModel,
    ) -> UserCreateModel:
        
        model = UserCreateModel(
            first_name=inbound_create_model.first_name,
            last_name=inbound_create_model.last_name, 
            username=inbound_create_model.username, 
            role=inbound_create_model.role,
            vendor_id=inbound_create_model.vendor_id, 
            retailer_location_id=inbound_create_model.retailer_location_id, 
        )

        return model

    def convert_from_inbound_update_model_to_update_model(
        self,
        inbound_update_model: UserInboundUpdateModel,
    ) -> UserUpdateModel:
        
        model = UserUpdateModel(
            first_name=inbound_update_model.first_name,
            last_name=inbound_update_model.last_name, 
            role=inbound_update_model.role,
        )

        return model

    def convert_from_inbound_search_model_to_search_model(
            self, 
            inbound_search_model: UserInboundSearchModel
    ) -> UserSearchModel:
        
        model = UserSearchModel(
            ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.ids)
                if inbound_search_model.ids is not None
                else 
                    None
            ),
            vendor_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.vendor_ids)
                if inbound_search_model.vendor_ids
                is not None 
                else 
                    None
            ),  
            retailer_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.retailer_ids)
                if inbound_search_model.retailer_ids
                is not None 
                else 
                    None
            ),  
            retailer_location_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.retailer_location_ids)
                if inbound_search_model.retailer_location_ids
                is not None 
                else 
                    None
            ),  
            role=inbound_search_model.role,
            name_like=inbound_search_model.name_like, 
            username_like=inbound_search_model.username_like, 
            username=inbound_search_model.username,
             
        )

        return model

    def convert_from_search_model_to_search_terms(
        self, 
        model: UserSearchModel
    ) -> list[SearchTerm]:
        
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(InListSearchTerm('id', self.common_utilities.convert_uuid_list_to_string_list(model.ids)))
  
        if model.retailer_ids is not None:
            search_terms.append(
                InListSearchTerm(
                    'retailer_id',
                    self.common_utilities.convert_uuid_list_to_string_list(model.retailer_ids),
                )
            )
            
        if model.retailer_location_ids is not None:
            search_terms.append(
                InListSearchTerm(
                    'retailer_location_id',
                    self.common_utilities.convert_uuid_list_to_string_list(model.retailer_location_ids),
                )
            )
             
        if model.vendor_ids is not None:
            search_terms.append(
                InListSearchTerm(
                    'vendor_id',
                    self.common_utilities.convert_uuid_list_to_string_list(model.vendor_ids),
                )
            )

        if model.role is not None:
            search_terms.append(ExactMatchSearchTerm('role', model.role.value, True))

        if model.name_like is not None:
            search_terms.append(
                LikeSearchTerm('full_name', model.name_like,
                               LikeComparatorModes.Like, True))
            
        if model.username is not None:
            search_terms.append(
                LikeSearchTerm('username', model.username,
                               LikeComparatorModes.Like, True))
            
        if model.username_like is not None:
            search_terms.append(
                LikeSearchTerm('username', model.username_like,
                               LikeComparatorModes.Like, True))
            
        return search_terms

    def convert_from_create_model_to_database_model(
        self, 
        model: UserCreateModel
    ) -> dict[str, Any]:
        
        database_model: dict[str, Any] = {
            'first_name': model.first_name,
            'last_name': model.last_name,
            'username': model.username,
            'role': model.role.value if model.role is not None else None,
            'vendor_id': str(model.vendor_id) if model.vendor_id is not None else None,
            'retailer_id': str(model.retailer_id) if model.retailer_id is not None else None,
            'retailer_location_id': str(model.retailer_location_id) if model.retailer_location_id is not None else None, 
        }

        return database_model

    def convert_from_update_model_to_database_model(
        self, 
        model: UserUpdateModel
    ) -> dict[str, Any]:
    
        database_model: dict[str, Any] = {
            'first_name': model.first_name,
            'last_name': model.last_name,
            'role': model.role.value if model.role is not None else None,
        }

        return database_model

    def convert_from_database_model_to_model(
        self, 
        database_model: dict[str, Any]
    ) -> UserModel:
        
        model = UserModel(
            id=database_model['id'],
            first_name=database_model['first_name'], 
            last_name=database_model['last_name'],
            full_name=database_model['full_name'],
            role=database_model['role'],
            username=database_model['username'],
            retailer_id=database_model['retailer_id'],
            retailer_location_id=database_model['retailer_location_id'],
            vendor_id=database_model['vendor_id'], 
            created_at=database_model['created_at'],
            updated_at=database_model['updated_at'],
        )

        return model

    def convert_from_model_to_outbound_model(
        self, 
        model: UserModel
    ) -> UserOutboundModel:
        
        outbound_model = UserOutboundModel(
            id=model.id,
            first_name=model.first_name, 
            last_name=model.last_name, 
            full_name=model.full_name, 
            username=model.username, 
            role=model.role,  
            vendor_id=model. vendor_id,
            retailer_id=model. retailer_id,
            retailer_location_id=model.retailer_location_id, 
            created_at=model.created_at.isoformat(timespec='milliseconds').replace('+00:00','Z'),
            updated_at=model.updated_at.isoformat(timespec='milliseconds').replace('+00:00','Z') if model.updated_at is not None else None,
        )

        return outbound_model
