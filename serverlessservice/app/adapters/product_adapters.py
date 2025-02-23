from typing import Any
from adapters.retailer_adapters import RetailerDataAdapter
from adapters.retailer_location_adapters import RetailerLocationDataAdapter
from adapters.vendor_adapters import VendorDataAdapter
from models.product_model import (
    ProductCreateModel,
    ProductInboundCreateModel,
    ProductInboundSearchModel,
    ProductInboundUpdateModel,
    ProductModel,
    ProductOutboundModel,
    ProductSearchModel,
    ProductUpdateModel,
)
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm,
    LikeComparatorModes,
    LikeSearchTerm,
    SearchTerm,
)


class ProductDataAdapter: 
    
    def __init__(
        self,
        common_utilities: CommonUtilities = CommonUtilities(), 
        retailer_adapter: RetailerDataAdapter = RetailerDataAdapter(),
        retailer_location_adapter: RetailerLocationDataAdapter = RetailerLocationDataAdapter(),
        vendor_adapter: VendorDataAdapter = VendorDataAdapter(),
    ) -> None:
        
        self.common_utilities = common_utilities
        self.retailer_adapter = retailer_adapter
        self.retailer_location_adapter = retailer_location_adapter
        self.vendor_adapter = vendor_adapter

        
    def convert_from_inbound_create_model_to_create_model(
        self,
        inbound_create_model: ProductInboundCreateModel
    ) -> ProductCreateModel:
        
        model = ProductCreateModel(
            name = inbound_create_model.name,
            vendor_sku = inbound_create_model.vendor_sku,
            referring_retailer_location_id = inbound_create_model.referring_retailer_location_id,
            vendor_id = inbound_create_model.vendor_id,
            confirmed_core_product_id = inbound_create_model.confirmed_core_product_id, 
            vendor_confirmation_status=inbound_create_model.vendor_confirmation_status,
        )

        return model

    def convert_from_inbound_update_model_to_update_model(
        self, 
        inbound_update_model: ProductInboundUpdateModel
    ) -> ProductUpdateModel:
        
        model = ProductUpdateModel(
            name = inbound_update_model.name,
            vendor_sku = inbound_update_model.vendor_sku, 
            vendor_id = inbound_update_model.vendor_id,
            confirmed_core_product_id = inbound_update_model.confirmed_core_product_id, 
            vendor_confirmation_status = inbound_update_model.vendor_confirmation_status,
        )

        return model

    def convert_from_inbound_search_model_to_search_model(
        self, 
        inbound_search_model: ProductInboundSearchModel
    ) -> ProductSearchModel:
        
        model = ProductSearchModel(
            ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.ids)
                if inbound_search_model.ids is not None 
                else 
                    None
            ),
            referring_retailer_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.referring_retailer_ids)
                if inbound_search_model.referring_retailer_ids is not None 
                else 
                    None
            ), 
            referring_retailer_location_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.referring_retailer_location_ids)
                if inbound_search_model.referring_retailer_location_ids is not None 
                else 
                    None
            ), 
            vendor_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.vendor_ids)
                if inbound_search_model.vendor_ids is not None 
                else 
                    None
            ), 
            confirmed_core_product_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.confirmed_core_product_ids)
                if inbound_search_model.confirmed_core_product_ids is not None 
                else 
                    None
            ), 
            vendor_confirmation_status=inbound_search_model.vendor_confirmation_status,
               
            name=inbound_search_model.name,
            name_like=inbound_search_model.name_like,
            vendor_sku=inbound_search_model.vendor_sku
 
        )

        return model

    def convert_from_search_model_to_search_terms(
        self, 
        model: ProductSearchModel
    ) -> list[SearchTerm]:
        
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(InListSearchTerm('id', self.common_utilities.convert_uuid_list_to_string_list(model.ids)))
            
        if model.referring_retailer_ids is not None:
            search_terms.append(InListSearchTerm('referring_retailer_id', self.common_utilities.convert_uuid_list_to_string_list(model.referring_retailer_ids)))
  
        if model.referring_retailer_location_ids is not None:
            search_terms.append(InListSearchTerm('referring_retailer_location_id', self.common_utilities.convert_uuid_list_to_string_list(model.referring_retailer_location_ids)))
            
        if model.vendor_ids is not None:
            search_terms.append(InListSearchTerm('vendor_id', self.common_utilities.convert_uuid_list_to_string_list(model.vendor_ids)))
  
        if model.confirmed_core_product_ids is not None:
            search_terms.append(InListSearchTerm('confirmed_core_product_id', self.common_utilities.convert_uuid_list_to_string_list(model.confirmed_core_product_ids)))
            
        if model.vendor_confirmation_status is not None:
            search_terms.append(ExactMatchSearchTerm('vendor_confirmation_status', model.vendor_confirmation_status.value, True))
            
        if model.name is not None:
            search_terms.append(ExactMatchSearchTerm('name', model.name, True))
            
        if model.name_like is not None:
            search_terms.append(LikeSearchTerm('name', model.name_like, LikeComparatorModes.Like, True))
            
        if model.vendor_sku is not None:    
            search_terms.append(ExactMatchSearchTerm('vendor_sku', model.vendor_sku, True))

        return search_terms

    def convert_from_create_model_to_database_model(
        self, 
        model: ProductCreateModel
    ) -> dict[str, Any]:
        
        database_model: dict[str, Any] = {
            'name': model.name,
            'referring_retailer_id': str(model.referring_retailer_id) if model.referring_retailer_id is not None else None,  
            'referring_retailer_location_id': str(model.referring_retailer_location_id) if model.referring_retailer_location_id is not None else None, 
            'vendor_id': str(model.vendor_id) if model.vendor_id is not None else None, 
            'confirmed_core_product_id': str(model.confirmed_core_product_id) if model.confirmed_core_product_id is not None else None, 
            'vendor_confirmation_status': model.vendor_confirmation_status.value  if model.vendor_confirmation_status is not None else None, 
            'vendor_sku': model.vendor_sku,
        }

        return database_model

    def convert_from_update_model_to_database_model(
        self, 
        model: ProductUpdateModel
    ) -> dict[str, Any]:
        
        database_model: dict[str, Any] = {
            'name': model.name, 
            'vendor_id': str(model.vendor_id) if model.vendor_id is not None else None, 
            'confirmed_core_product_id': str(model.confirmed_core_product_id) if model.confirmed_core_product_id is not None else None, 
            'vendor_confirmation_status': model.vendor_confirmation_status.value  if model.vendor_confirmation_status is not None else None, 
            'vendor_sku': model.vendor_sku,
        }

        return database_model

    def convert_from_database_model_to_model(
        self, 
        database_model: dict[str, Any]
    ) -> ProductModel:
            
        model = ProductModel(
            id=database_model['id'],
            name=database_model['name'],    
            
            referring_retailer_id=database_model['referring_retailer_id'], 
            referring_retailer_location_id=database_model['referring_retailer_location_id'],
            vendor_id=database_model['vendor_id'], 
            confirmed_core_product_id=database_model['confirmed_core_product_id'],
            vendor_confirmation_status=database_model['vendor_confirmation_status'],
            vendor_sku=database_model['vendor_sku'],
            
            created_at=database_model['created_at'],
            updated_at=database_model['updated_at'],
        )

        return model

    def convert_from_model_to_outbound_model(
        self,
        model: ProductModel
    ) -> ProductOutboundModel:
    
        outbound_model = ProductOutboundModel(
            id=model.id,
            name=model.name, 
            
            referring_retailer_id=model.referring_retailer_id,  
            referring_retailer = self.retailer_adapter.convert_from_model_to_outbound_model(model.referring_retailer) if model.referring_retailer is not None else None,
            referring_retailer_location_id=model.referring_retailer_location_id,
            referring_retailer_location = self.retailer_location_adapter.convert_from_model_to_outbound_model(model.referring_retailer_location) if model.referring_retailer_location is not None else None,
            vendor_id=model.vendor_id, 
            vendor = self.vendor_adapter.convert_from_model_to_outbound_model(model.vendor) if model.vendor is not None else None,
            confirmed_core_product_id=model.confirmed_core_product_id,
            confirmed_core_product = self.convert_from_model_to_outbound_model(model.confirmed_core_product) if model.confirmed_core_product is not None else None,
            vendor_confirmation_status=model.vendor_confirmation_status,
            vendor_sku=model.vendor_sku,
            created_at=model.created_at.isoformat(timespec='milliseconds').replace('+00:00','Z'),
            updated_at=model.updated_at.isoformat(timespec='milliseconds').replace('+00:00','Z') if model.updated_at is not None else None,
        )

        return outbound_model
