from typing import Any
from adapters.inventory_intake_job_adapters import RangeSearchTerm
from adapters.retailer_adapters import RetailerDataAdapter
from adapters.retailer_location_adapters import RetailerLocationDataAdapter
from adapters.sales_intake_job_adapters import SalesIntakeJobDataAdapter
from models.historical_sale_model import (
    HistoricalSaleCreateModel,
    HistoricalSaleInboundCreateModel,
    HistoricalSaleInboundSearchModel, 
    HistoricalSaleModel,
    HistoricalSaleOutboundModel,
    HistoricalSaleSearchModel, 
)
from util.common import CommonUtilities
from util.database import ( 
    InListSearchTerm, 
    SearchTerm,
)


class HistoricalSaleDataAdapter:
    
    def __init__(
        self,
        retailer_adapter: RetailerDataAdapter = RetailerDataAdapter(),
        retailer_location_adapter: RetailerLocationDataAdapter = RetailerLocationDataAdapter(),
        sales_intake_job_adapter: SalesIntakeJobDataAdapter = SalesIntakeJobDataAdapter(),
        common_utilities: CommonUtilities = CommonUtilities(),
    ) -> None:

        self.retailer_adapter = retailer_adapter
        self.retailer_location_adapter = retailer_location_adapter
        self.sales_intake_job_adapter = sales_intake_job_adapter
        
        self.common_utilities = common_utilities
        
    def convert_from_inbound_create_model_to_create_model(
        self, 
        inbound_create_model: HistoricalSaleInboundCreateModel
    ) -> HistoricalSaleCreateModel:
        
        model = HistoricalSaleCreateModel(
            retailer_location_id=inbound_create_model.retailer_location_id,
            sale_timestamp=inbound_create_model.sale_timestamp,
            pos_sale_id=inbound_create_model.pos_sale_id,
            total=inbound_create_model.total,
            sub_total=inbound_create_model.sub_total,
            discount=inbound_create_model.discount,
            tax=inbound_create_model.tax,
            cost=inbound_create_model.cost, 
            sales_intake_job_id=inbound_create_model.sales_intake_job_id, 
        )

        return model
  
    def convert_from_inbound_search_model_to_search_model(
        self, 
        inbound_search_model: HistoricalSaleInboundSearchModel
    ) -> HistoricalSaleSearchModel:
        
        model = HistoricalSaleSearchModel(
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
            sale_timestamp_min=inbound_search_model.sale_timestamp_min,
            sale_timestamp_max=inbound_search_model.sale_timestamp_max, 
        )

        return model

    def convert_from_search_model_to_search_terms(
        self, 
        model: HistoricalSaleSearchModel
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
         
        if model.sale_timestamp_min is not None or model.sale_timestamp_max is not None:
            search_terms.append(RangeSearchTerm('sale_timestamp', model.sale_timestamp_min, model.sale_timestamp_max))
            
        return search_terms

    def convert_from_create_model_to_database_model(
        self, 
        model: HistoricalSaleCreateModel
    ) -> dict[str, Any]:
    
        database_model: dict[str, Any] = {  
            'retailer_id': str(model.retailer_id) if model.retailer_id is not None else None ,
            'retailer_location_id': str(model.retailer_location_id) if model.retailer_location_id is not None else None ,
            'pos_sale_id': model.pos_sale_id,
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
    ) -> HistoricalSaleModel:
        
        model = HistoricalSaleModel(
            id=database_model['id'], 
            retailer_id=database_model['retailer_id'],
            retailer_location_id=database_model['retailer_location_id'],
            sales_intake_job_id=database_model['sales_intake_job_id'],
            created_at=database_model['created_at'],
            pos_sale_id=database_model['pos_sale_id'],
            sale_timestamp=database_model['sale_timestamp'],
            total=database_model['total'],
            sub_total=database_model['sub_total'],
            discount=database_model['discount'],
            tax=database_model['tax'],
            cost=database_model['cost'],
        )

        return model

    def convert_from_model_to_outbound_model(
        self, 
        model: HistoricalSaleModel
    ) -> HistoricalSaleOutboundModel:
        
        outbound_model = HistoricalSaleOutboundModel(
            id=model.id,
            retailer_id=model.retailer_id,
            retailer = self.retailer_adapter.convert_from_model_to_outbound_model(model.retailer) if model.retailer is not None else None,
            retailer_location_id=model.retailer_location_id,
            retailer_location = self.retailer_location_adapter.convert_from_model_to_outbound_model(model.retailer_location) if model.retailer_location is not None else None,
            pos_sale_id=model.pos_sale_id,
             
            sale_timestamp=model.sale_timestamp.isoformat(timespec='milliseconds').replace('+00:00','Z'),
            total=model.total,
            sub_total=model.sub_total,
            discount=model.discount,
            tax=model.tax,
            cost=model.cost,
            sales_intake_job_id=model.sales_intake_job_id,
            sales_intake_job = self.sales_intake_job_adapter.convert_from_model_to_outbound_model(model.sales_intake_job) if model.sales_intake_job is not None else None,
           
            created_at=model.created_at.isoformat(timespec='milliseconds').replace('+00:00','Z'),
            updated_at=model.updated_at.isoformat(timespec='milliseconds').replace('+00:00','Z') if model.updated_at is not None else None,
        )

        return outbound_model
