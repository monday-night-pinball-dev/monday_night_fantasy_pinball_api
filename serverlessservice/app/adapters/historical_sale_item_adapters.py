from typing import Any
from adapters.historical_sale_adapters import HistoricalSaleDataAdapter
from adapters.inventory_intake_job_adapters import RangeSearchTerm
from adapters.product_adapters import ProductDataAdapter
from adapters.retailer_adapters import RetailerDataAdapter
from adapters.retailer_location_adapters import RetailerLocationDataAdapter
from adapters.sales_intake_job_adapters import SalesIntakeJobDataAdapter
from adapters.vendor_adapters import VendorDataAdapter
from models.historical_sale_item_model import (
    HistoricalSaleItemCreateModel,
    HistoricalSaleItemInboundCreateModel,
    HistoricalSaleItemInboundSearchModel, 
    HistoricalSaleItemModel,
    HistoricalSaleItemOutboundModel,
    HistoricalSaleItemSearchModel, 
)
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm, 
    SearchTerm,
)


class HistoricalSaleItemDataAdapter:
    def __init__(
        self,
        product_adapter : ProductDataAdapter = ProductDataAdapter(),
        historical_sale_adapter : HistoricalSaleDataAdapter = HistoricalSaleDataAdapter(),
        retailer_location_adapter : RetailerLocationDataAdapter = RetailerLocationDataAdapter(),
        retailer_adapter : RetailerDataAdapter = RetailerDataAdapter(),
        sales_intake_job_adapter : SalesIntakeJobDataAdapter = SalesIntakeJobDataAdapter(),
        vendor_adapter : VendorDataAdapter = VendorDataAdapter(), 
        common_utilities: CommonUtilities = CommonUtilities()
    ) -> None:
        
        self.product_adapter = product_adapter
        self.historical_sale_adapter = historical_sale_adapter
        self.retailer_location_adapter = retailer_location_adapter
        self.retailer_adapter = retailer_adapter
        self.sales_intake_job_adapter = sales_intake_job_adapter
        self.vendor_adapter = vendor_adapter
        self.common_utilities = common_utilities

    def convert_from_inbound_create_model_to_create_model(
        self, 
        inbound_create_model: HistoricalSaleItemInboundCreateModel
    ) -> HistoricalSaleItemCreateModel:
        
        model = HistoricalSaleItemCreateModel( 
            product_id=inbound_create_model.product_id,
            sale_timestamp=inbound_create_model.sale_timestamp,
            pos_sale_id=inbound_create_model.pos_sale_id,
            total=inbound_create_model.total,
            sub_total=inbound_create_model.sub_total,
            discount=inbound_create_model.discount,
            tax=inbound_create_model.tax,
            cost=inbound_create_model.cost,   
            historical_sale_id=inbound_create_model.historical_sale_id,
            pos_product_id=inbound_create_model.pos_product_id,
            lot_identifier=inbound_create_model.lot_identifier,
            unit_of_weight=inbound_create_model.unit_of_weight,
            weight_in_units=inbound_create_model.weight_in_units,
            sale_product_name=inbound_create_model.sale_product_name,
            sku=inbound_create_model.sku,
            sale_count=inbound_create_model.sale_count,
            
        )

        return model
  
    def convert_from_inbound_search_model_to_search_model(
        self, 
        inbound_search_model: HistoricalSaleItemInboundSearchModel
    ) -> HistoricalSaleItemSearchModel:
        
        model = HistoricalSaleItemSearchModel(
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
            
            sales_intake_job_ids=    (  
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.sales_intake_job_ids)
                if inbound_search_model.sales_intake_job_ids is not None 
                else 
                    None
            ),
            
            pos_sale_ids=(
                inbound_search_model.pos_sale_ids.split(',')  
                if inbound_search_model.pos_sale_ids is not None
                else    
                    None
            ), 
            
            pos_product_ids=(
                inbound_search_model.pos_product_ids.split(',')  
                if inbound_search_model.pos_product_ids is not None
                else    
                    None
            ),
            
            historical_sale_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.historical_sale_ids)
                if inbound_search_model.historical_sale_ids is not None 
                else    
                    None
            ),
            
            product_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.product_ids)
                if inbound_search_model.product_ids is not None 
                else    
                    None
            ),
            
            product_vendor_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(inbound_search_model.product_vendor_ids)
                if inbound_search_model.product_vendor_ids is not None 
                else    
                    None
            ),
            
            lot_identifiers=(
                inbound_search_model.lot_identifiers.split(',')  
                if inbound_search_model.lot_identifiers is not None
                else    
                    None
            ), 
            skus=(
                inbound_search_model.skus.split(',')  
                if inbound_search_model.skus is not None
                else    
                    None
            ),
            sale_product_name=inbound_search_model.sale_product_name,
            
            sale_timestamp_min=inbound_search_model.sale_timestamp_min,
            sale_timestamp_max=inbound_search_model.sale_timestamp_max,
            
        )

        return model

    def convert_from_search_model_to_search_terms(
        self, 
        model: HistoricalSaleItemSearchModel
    ) -> list[SearchTerm]:
        
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(InListSearchTerm('id', self.common_utilities.convert_uuid_list_to_string_list(model.ids)))
                    
        if model.retailer_ids is not None:
            search_terms.append(InListSearchTerm('retailer_id', self.common_utilities.convert_uuid_list_to_string_list(model.retailer_ids)))
                    
        if model.retailer_location_ids is not None:
            search_terms.append(InListSearchTerm('retailer_location_id', self.common_utilities.convert_uuid_list_to_string_list(model.retailer_location_ids)))
            
        if model.sales_intake_job_ids is not None:
            search_terms.append(InListSearchTerm('sales_intake_job_id', self.common_utilities.convert_uuid_list_to_string_list(model.sales_intake_job_ids)))
            
        if model.pos_sale_ids is not None:
            search_terms.append(InListSearchTerm('pos_sale_id', self.common_utilities.convert_uuid_list_to_string_list(model.pos_sale_ids)))
          
        if model.pos_product_ids is not None:
            search_terms.append(InListSearchTerm('pos_product_id', self.common_utilities.convert_uuid_list_to_string_list(model.pos_product_ids)))
         
        if model.sale_timestamp_min is not None or model.sale_timestamp_max is not None:
            search_terms.append(RangeSearchTerm('sale_timestamp', model.sale_timestamp_min, model.sale_timestamp_max))
            
        if model.historical_sale_ids is not None:
            search_terms.append(InListSearchTerm('historical_sale_id', self.common_utilities.convert_uuid_list_to_string_list(model.historical_sale_ids)))
            
        if model.product_ids is not None:
            search_terms.append(InListSearchTerm('product_id', self.common_utilities.convert_uuid_list_to_string_list(model.product_ids)))
            
        if model.product_vendor_ids is not None:
            search_terms.append(InListSearchTerm('product_vendor_id', self.common_utilities.convert_uuid_list_to_string_list(model.product_vendor_ids)))
            
        if model.lot_identifiers is not None:
            search_terms.append(InListSearchTerm('lot_identifier', model.lot_identifiers))
            
        if model.skus is not None:
            search_terms.append(InListSearchTerm('sku', model.skus))
            
        if model.sale_product_name is not None:
            search_terms.append(ExactMatchSearchTerm('sale_product_name', model.sale_product_name, True))
             
        return search_terms

    def convert_from_create_model_to_database_model(
        self, 
        model: HistoricalSaleItemCreateModel
    ) -> dict[str, Any]:
       
        database_model: dict[str, Any] = {  
            'retailer_id': str(model.retailer_id) if model.retailer_id is not None else None ,
            'retailer_location_id': str(model.retailer_location_id) if model.retailer_location_id is not None else None ,
            'historical_sale_id': str(model.historical_sale_id) if model.historical_sale_id is not None else None ,
            
            'product_id': str(model.product_id) if model.product_id is not None else None ,
            'product_vendor_id': str(model.product_vendor_id) if model.product_vendor_id is not None else None ,
            
            'sku': model.sku,
            'sale_count': model.sale_count,
            'pos_product_id': model.pos_product_id,
            'pos_sale_id': model.pos_sale_id,
            'lot_identifier': model.lot_identifier,
            'unit_of_weight': model.unit_of_weight,
            'weight_in_units': model.weight_in_units,
            'sale_product_name': model.sale_product_name,
            'sale_timestamp': model.sale_timestamp,
            'total': model.total,
            'sub_total': model.sub_total,
            'discount': model.discount,
            'tax': model.tax,
            'cost': model.cost, 
            'sales_intake_job_id': str(model.sales_intake_job_id) if model.sales_intake_job_id is not None else None ,
        }

        return database_model

    def convert_from_database_model_to_model(
            self, 
            database_model: dict[str, Any]
        ) -> HistoricalSaleItemModel:
        
        model = HistoricalSaleItemModel(
            id=database_model['id'], 
            product_id=database_model['product_id'],
            retailer_id=database_model['retailer_id'],
            retailer_location_id=database_model['retailer_location_id'],
            historical_sale_id=database_model['historical_sale_id'],
            sales_intake_job_id=database_model['sales_intake_job_id'],
            product_vendor_id=database_model['product_vendor_id'],
            pos_sale_id=database_model['pos_sale_id'],
            pos_product_id=database_model['pos_product_id'],
            lot_identifier=database_model['lot_identifier'],
            unit_of_weight=database_model['unit_of_weight'],
            weight_in_units=database_model['weight_in_units'],
            sale_product_name=database_model['sale_product_name'],
            sale_timestamp=database_model['sale_timestamp'],
            sku=database_model['sku'],
            sale_count=database_model['sale_count'],
            total=database_model['total'],
            sub_total=database_model['sub_total'],
            discount=database_model['discount'],
            tax=database_model['tax'],
            cost=database_model['cost'], 
            created_at=database_model['created_at'],
            updated_at=database_model['updated_at'],
        )

        return model

    def convert_from_model_to_outbound_model(
            self, 
            model: HistoricalSaleItemModel
        ) -> HistoricalSaleItemOutboundModel:
        
        outbound_model = HistoricalSaleItemOutboundModel(
            id=model.id,
            product_id=model.product_id,
            product=self.product_adapter.convert_from_model_to_outbound_model(model.product) if model.product is not None else None,
            retailer_id=model.retailer_id, 
            retailer = self.retailer_adapter.convert_from_model_to_outbound_model(model.retailer) if model.retailer is not None else None,
            retailer_location_id=model.retailer_location_id,
            retailer_location = self.retailer_location_adapter.convert_from_model_to_outbound_model(model.retailer_location) if model.retailer_location is not None else None,
            historical_sale_id=model.historical_sale_id,
            historical_sale = self.historical_sale_adapter.convert_from_model_to_outbound_model(model.historical_sale) if model.historical_sale is not None else None,
            sales_intake_job_id=model.sales_intake_job_id,
            sales_intake_job = self.sales_intake_job_adapter.convert_from_model_to_outbound_model(model.sales_intake_job) if model.sales_intake_job is not None else None,
            product_vendor_id=model.product_vendor_id,
            product_vendor = self.vendor_adapter.convert_from_model_to_outbound_model(model.product_vendor) if model.product_vendor is not None else None,
            pos_sale_id=model.pos_sale_id,
            pos_product_id=model.pos_product_id,
            lot_identifier=model.lot_identifier,
            unit_of_weight=model.unit_of_weight,
            weight_in_units=model.weight_in_units,
            sale_product_name=model.sale_product_name,
            sale_timestamp=model.sale_timestamp.isoformat(timespec='milliseconds').replace('+00:00','Z'),
            sku=model.sku,
            sale_count=model.sale_count,
            total=model.total,
            sub_total=model.sub_total,
            discount=model.discount,
            tax=model.tax,
            cost=model.cost,  
            created_at=model.created_at.isoformat(timespec='milliseconds').replace('+00:00','Z'),
            updated_at=model.updated_at.isoformat(timespec='milliseconds').replace('+00:00','Z') if model.updated_at is not None else None,
        )

        return outbound_model
