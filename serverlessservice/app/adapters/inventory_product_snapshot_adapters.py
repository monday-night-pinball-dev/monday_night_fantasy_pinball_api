from typing import Any
from adapters.inventory_intake_job_adapters import InventoryIntakeJobDataAdapter, RangeSearchTerm
from adapters.product_adapters import ProductDataAdapter
from adapters.retailer_adapters import RetailerDataAdapter
from adapters.retailer_location_adapters import RetailerLocationDataAdapter
from adapters.vendor_adapters import VendorDataAdapter
from models.inventory_product_snapshot_model import (
    InventoryProductSnapshotCreateModel,
    InventoryProductSnapshotInboundCreateModel,
    InventoryProductSnapshotInboundSearchModel, 
    InventoryProductSnapshotModel,
    InventoryProductSnapshotOutboundModel,
    InventoryProductSnapshotSearchModel, 
)
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm, 
    SearchTerm,
)


class InventoryProductSnapshotDataAdapter:
    def __init__(
        self,
        retailer_adapter : RetailerDataAdapter = RetailerDataAdapter(),
        retailer_location_adapter : RetailerLocationDataAdapter = RetailerLocationDataAdapter(),
        product_adapter : ProductDataAdapter = ProductDataAdapter(),
        inventory_intake_job_adapter : InventoryIntakeJobDataAdapter = InventoryIntakeJobDataAdapter(),
        vendor_adapter : VendorDataAdapter = VendorDataAdapter(),
        common_utilities: CommonUtilities = CommonUtilities()
    ) -> None:
        
        self.retailer_adapter = retailer_adapter
        self.retailer_location_adapter = retailer_location_adapter
        self.product_adapter = product_adapter
        self.inventory_intake_job_adapter = inventory_intake_job_adapter
        self.vendor_adapter = vendor_adapter    
        self.common_utilities = common_utilities

    def convert_from_inbound_create_model_to_create_model(
        self, 
        inbound_create_model: InventoryProductSnapshotInboundCreateModel
    ) -> InventoryProductSnapshotCreateModel:
        
        model = InventoryProductSnapshotCreateModel(
            retailer_id=None,
            vendor_id=None,
            product_id=inbound_create_model.product_id, 
            retailer_location_id=inbound_create_model.retailer_location_id, 
            snapshot_hour=inbound_create_model.snapshot_hour,
            sku=inbound_create_model.sku,
            stock_on_hand=inbound_create_model.stock_on_hand,
            price=inbound_create_model.price, 
            inventory_intake_job_id=inbound_create_model.inventory_intake_job_id,
        )

        return model
  
    def convert_from_inbound_search_model_to_search_model(
        self, 
        inbound_search_model: InventoryProductSnapshotInboundSearchModel
    ) -> InventoryProductSnapshotSearchModel:
        
        model = InventoryProductSnapshotSearchModel(
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
            product_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.product_ids)
                if inbound_search_model.product_ids is not None 
                else    
                    None
            ),
            vendor_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.vendor_ids)
                if inbound_search_model.vendor_ids is not None 
                else    
                    None
            ),
            inventory_intake_job_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.inventory_intake_job_ids)
                if inbound_search_model.inventory_intake_job_ids is not None 
                else    
                    None
            ),
            sku=inbound_search_model.sku, 
            snapshot_hour_min=inbound_search_model.snapshot_hour_min,
            snapshot_hour_max=inbound_search_model.snapshot_hour_max,
            
        )

        return model

    def convert_from_search_model_to_search_terms(
        self, 
        model: InventoryProductSnapshotSearchModel
    ) -> list[SearchTerm]:
        
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(InListSearchTerm('id', self.common_utilities.convert_uuid_list_to_string_list(model.ids)))
                    
        if model.retailer_ids is not None:
            search_terms.append(InListSearchTerm('retailer_id', self.common_utilities.convert_uuid_list_to_string_list(model.retailer_ids)))
                    
        if model.retailer_location_ids is not None:
            search_terms.append(InListSearchTerm('retailer_location_id', self.common_utilities.convert_uuid_list_to_string_list(model.retailer_location_ids)))
            
        if model.product_ids is not None:
            search_terms.append(InListSearchTerm('product_id', self.common_utilities.convert_uuid_list_to_string_list(model.product_ids)))
            
        if model.vendor_ids is not None:
            search_terms.append(InListSearchTerm('vendor_id', self.common_utilities.convert_uuid_list_to_string_list(model.vendor_ids)))
        
        if model.inventory_intake_job_ids is not None:
            search_terms.append(InListSearchTerm('inventory_intake_job_id', self.common_utilities.convert_uuid_list_to_string_list(model.inventory_intake_job_ids)))
            
        if model.sku is not None:    
            search_terms.append(ExactMatchSearchTerm('sku', model.sku, True))
 
        if model.snapshot_hour_min is not None or model.snapshot_hour_max is not None:
            search_terms.append(RangeSearchTerm('snapshot_hour', model.snapshot_hour_min, model.snapshot_hour_max))
            
        return search_terms

    def convert_from_create_model_to_database_model(
        self, 
        model: InventoryProductSnapshotCreateModel
    ) -> dict[str, Any]:
       
        database_model: dict[str, Any] = {  
            'retailer_id': str(model.retailer_id) if model.retailer_id is not None else None ,
            'retailer_location_id': str(model.retailer_location_id) if model.retailer_location_id is not None else None ,
            'product_id': str(model.product_id) if model.product_id is not None else None ,
            'inventory_intake_job_id': str(model.inventory_intake_job_id) if model.inventory_intake_job_id is not None else None ,
            'vendor_id': str(model.vendor_id) if model.vendor_id is not None else None,
            'snapshot_hour': model.snapshot_hour,
            'sku': model.sku,
            'stock_on_hand': model.stock_on_hand,
            'price': model.price, 
        }

        return database_model

    def convert_from_database_model_to_model(
        self, 
        database_model: dict[str, Any]
    ) -> InventoryProductSnapshotModel:
        
        model = InventoryProductSnapshotModel(
            id=database_model['id'],
            product_id=database_model['product_id'],
            retailer_id=database_model['retailer_id'],
            retailer_location_id=database_model['retailer_location_id'],
            inventory_intake_job_id=database_model['inventory_intake_job_id'],
            snapshot_hour=database_model['snapshot_hour'],
            sku=database_model['sku'],
            stock_on_hand=database_model['stock_on_hand'],
            price=database_model['price'], 
            vendor_id=database_model['vendor_id'],
            created_at=database_model['created_at'],
            updated_at=database_model['updated_at'],
        )

        return model

    def convert_from_model_to_outbound_model(
        self, 
        model: InventoryProductSnapshotModel
    ) -> InventoryProductSnapshotOutboundModel:
        
        outbound_model = InventoryProductSnapshotOutboundModel(
            id=model.id,
            retailer_id=model.retailer_id,
            retailer=self.retailer_adapter.convert_from_model_to_outbound_model(model.retailer) if model.retailer is not None else None,
            retailer_location_id=model.retailer_location_id,
            retailer_location = self.retailer_location_adapter.convert_from_model_to_outbound_model(model.retailer_location) if model.retailer_location is not None else None,
            product_id=model.product_id,
            product=self.product_adapter.convert_from_model_to_outbound_model(model.product) if model.product is not None else None,
            inventory_intake_job_id=model.inventory_intake_job_id,
            inventory_intake_job=self.inventory_intake_job_adapter.convert_from_model_to_outbound_model(model.inventory_intake_job) if model.inventory_intake_job is not None else None,
            snapshot_hour=model.snapshot_hour.isoformat(timespec='milliseconds').replace('+00:00','Z'),
            sku=model.sku,
            stock_on_hand=model.stock_on_hand,
            price=model.price, 
            vendor_id=model.vendor_id,
            vendor=self.vendor_adapter.convert_from_model_to_outbound_model(model.vendor) if model.vendor is not None else None,
            created_at=model.created_at.isoformat(timespec='milliseconds').replace('+00:00','Z'),
            updated_at=model.updated_at.isoformat(timespec='milliseconds').replace('+00:00','Z') if model.updated_at is not None else None,
        )

        return outbound_model
