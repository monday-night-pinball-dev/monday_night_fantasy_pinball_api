from datetime import datetime, timedelta
 
import json
from typing import Any
from uuid import UUID

import requests
 
from integrations.common import ServiceCaller
from integrations.types import GenericHistoricalSaleItemObject, GenericHistoricalSaleObject, GenericInventoryObject 
 
from models.product_model import ProductCreateModel, ProductModel, ProductVendorConfirmationStatuses
from models.retailer_location_model import RetailerLocationModel 

class PosabitSalesHistoryDiscountObject:
    def __init__(
        self,
        coupon_id: int | None = None,
        coupon_name: str | None = None
    ) -> None:
            
        self.coupon_id = coupon_id
        self.coupon_name = coupon_name

class PosabitSalesHistorySalesTenderObject:
    def __init__(
        self,
        sales_tender_id: int | None = None,
        subtotal: int | None = None,
        tax: int | None = None,
        total: int | None = None,
        payment_method_name: str | None = None
    ) -> None:

        self.sales_tender_id = sales_tender_id

        self.subtotal = subtotal
        self.tax = tax
        self.total = total
        
        self.payment_method_name = payment_method_name

class PosabitSalesHistoryItemObject:
    def __init__(
        self, 
        item_id: int | None = None,
        sales_history_id: int | None = None,
        product_id: int | None = None,
        inventory_id: int | None = None,
        lot_id: int | None = None,
        lot_number: str | None = None,
        is_marijuana: bool | None = None,
        quantity: int | None = None,
        weight: float | None = None,
        unit_weight: float | None = None,
        unit_of_weight: str | None = None,
        weight_in_grams: float | None = None,
        cost: int  | None = None,
        sub_total: int  | None = None,
        tax: int  | None = None,
        discount: int  | None = None,
        sku: str | None = None,
        category: str | None = None,
        brand: str | None = None,
        product_name: str | None = None,
        family_name: str | None = None,
        tier_name: str | None = None,
        total: int | None = None,
        discount_list: list[PosabitSalesHistoryDiscountObject] | None = None,
    ) -> None:  
        self.item_id= item_id
        self.sales_history_id= sales_history_id
        self.product_id= product_id
        self.inventory_id= inventory_id
        self.lot_id= lot_id
        self.lot_number= lot_number
        self.is_marijuana= is_marijuana
        self.quantity= quantity
        self.weight= weight
        self.unit_weight= unit_weight
        self.unit_of_weight= unit_of_weight
        self.weight_in_grams= weight_in_grams
        self.cost= cost
        self.sub_total= sub_total
        self.tax= tax
        self.discount= discount
        self.sku= sku
        self.category= category
        self.brand= brand
        self.product_name= product_name
        self.family_name= family_name
        self.tier_name= tier_name
        self.total= total
        self.discount_list= discount_list or []
        
class PosabitSalesHistoryObject:
    def __init__(
        self,
        id: int | None = None,
        is_medical: bool | None = None,
        ordered_at: datetime | None = None,
        ordered_at_local: datetime | None = None,
        sale_type: str | None = None,
        order_source: str | None = None,
        terminal_till_id: int | None = None,
        terminal_id: int | None = None,
        local_order_id: str | None = None,
        customer_id: int | None = None,
        user_id: int | None = None,
        sub_total: int | None = None,
        discount: int | None = None,
        tax: int | None = None,
        total: int | None = None,
        cost: int | None = None,
        status: str | None = None,
        items: list[dict[str, Any]] | None = None,
        sales_tenders: list[dict[str, Any]]  | None = None, 
        created_at: datetime | None = None,
        updated_at:  datetime | None= None
    ) -> None:

        self.id = id
        
        self.is_medical = is_medical
        self.ordered_at = ordered_at
        self.ordered_at_local = ordered_at_local
        self.sale_type = sale_type
        self.order_source = order_source
        self.terminal_till_id = terminal_till_id
        self.terminal_id = terminal_id
        self.local_order_id = local_order_id
        self.customer_id = customer_id
        self.user_id = user_id
        self.sub_total = sub_total
        self.discount = discount
        self.tax = tax
        self.total = total
        self.cost = cost
        self.status = status
        self.items = [PosabitSalesHistoryItemObject(**item) for item in items] if items is not None else []
        self.sales_tenders = [PosabitSalesHistorySalesTenderObject(**tender) for tender in sales_tenders] if sales_tenders is not None else []
        self.created_at = created_at
        self.updated_at = updated_at

 

class PosabitInventoryObject:
    def __init__(self, 
        id: int | None = None, 
        product_id: int | None = None,
        name: str | None = None,
        unit: str | None = None,
        price: int | None = None,
        med_price: int | None = None,
        last_price: int | None = None,
        quantity_on_hand: str | None = None,
        sellable_quantity: str | None = None,
        ecomm_quantity: str | None = None,
        vendor: str | None = None,
        vendor_license: str | None = None,
        brand: str | None = None,
        category: str | None = None,
        compliance_type: str | None = None,
        flower_type: str | None = None,
        concentrate_type: str | None = None,
        product_type: str | None = None,
        product_family: str | None = None,
        tags: list[str] | None = None, 
        description: str | None = None,
        description_html: str | None = None,
        image: list[str] | None = None,
        active: bool | None = None,
        bulk_item: bool | None = None,
        strain: str | None = None,
        thc_measure: str | None = None,
        cbd_measure: str | None = None,
        sku: str | None = None,
        discountable: bool | None = None,
        tier_name: str | None = None,
        doh_compliant: bool | None = None,
        created_at: datetime | None = None,
        updated_at:  datetime | None= None,
        rooms: list[tuple[str,str]] | None = None
    ) -> None:
        
        self.id = id
        self.product_id = product_id
        self.name = name
        self.unit = unit
        self.price = price
        self.med_price = med_price
        self.last_price = last_price
        self.quantity_on_hand = quantity_on_hand
        self.sellable_quantity = sellable_quantity
        self.ecomm_quantity = ecomm_quantity
        self.vendor = vendor
        self.vendor_license = vendor_license
        self.brand = brand
        self.category = category
        self.compliance_type = compliance_type
        self.flower_type = flower_type
        self.concentrate_type = concentrate_type
        self.product_type = product_type
        self.product_family = product_family
        self.tags = tags
        self.description = description
        self.description_html = description_html
        self.image = image
        self.active = active
        self.bulk_item = bulk_item
        self.strain = strain
        self.thc_measure = thc_measure
        self.cbd_measure = cbd_measure
        self.sku = sku
        self.discountable = discountable
        self.tier_name = tier_name
        self.doh_compliant = doh_compliant
        self.created_at = created_at
        self.updated_at = updated_at
        self.rooms = rooms or []
 
class PosabitInventoryResponse:
    def __init__(
        self,
        total_records: int,
        current_page: int,
        total_pages: int,
        per_page: int,
        inventory: list[PosabitInventoryObject] | None = None,
    ) -> None:
        self.total_records = total_records
        self.current_page = current_page
        self.total_pages = total_pages
        self.per_page = per_page
         
        self.inventory = inventory or []

class PosabitSalesHistoriesResponse:
    def __init__(
        self,
        total_records: int,
        current_page: int,
        total_pages: int,
        per_page: int,
        sales_histories: list[PosabitSalesHistoryObject] | None = None,
    ) -> None:
        self.total_records = total_records
        self.current_page = current_page
        self.total_pages = total_pages
        self.per_page = per_page
         
        self.sales_histories = sales_histories or []
        
class PosabitIntegration:
  
    def __init__(
        self,
        service_caller: ServiceCaller = ServiceCaller()
    ) -> None:
        self.service_caller = service_caller
            
            
    def get_all_pages_of_inventory_items(
        self,
        pos_integration_key: str,  
        simulator_response_id : UUID | None = None,
    ) -> list[PosabitInventoryObject]:
        
        running_list_of_inventory_items: list[PosabitInventoryObject] = []
    
        # note that if we want to restrict the date range, we need to add the following to the url:
        # q[updated_at_gt]={start_date.isoformat(timespec='milliseconds').replace('+00:00','Z')}&q[updated_at_lt]={end_date.isoformat(timespec='milliseconds').replace('+00:00','Z')}
         
        print("Posabit integration retrieving inventory data with key")
        
        results = self.service_caller.get(
            url = f"https://app.posabit.com/api/v2/venue/sales_histories", 
            headers = {"Authorization": f"Bearer {pos_integration_key}"},
            simulator_response_id = simulator_response_id
        ) 
       
        var = results.json()
        posabit_inventories =  PosabitInventoryResponse(**results.json())
        
        running_list_of_inventory_items += [PosabitInventoryObject(**item) for item in posabit_inventories.inventory]
        
        total_pages = posabit_inventories.total_pages or 1
        current_page = 2
        
        while current_page <= total_pages and simulator_response_id is None:
             
            next_page_of_results = self.service_caller.get(
                url = f"https://app.posabit.com/api/v2/venue/inventories", 
                headers = {"Authorization": f"Bearer {pos_integration_key}"},
                simulator_response_id = simulator_response_id
            ) 
                
            next_page_of_posabit_inventories =  PosabitInventoryResponse(**next_page_of_results.json())
            running_list_of_inventory_items += [PosabitInventoryObject(**item) for item in posabit_inventories.inventory]
            current_page = next_page_of_posabit_inventories.current_page + 1
            total_pages = next_page_of_posabit_inventories.total_pages
                
        return running_list_of_inventory_items
    
    def get_all_pages_of_sales(
        self,
        pos_integration_key: str,  
        start_time: datetime,
        end_time: datetime | None = None,
        simulator_response_id : UUID | None = None,
    ) -> list[PosabitSalesHistoryObject]:
        
        url = self.resolve_date_range_url(
            base_url = f"https://app.posabit.com/api/v2/venue/sales_histories",
            start_time = start_time,
            end_time = end_time,
            page = 1
        )
        
        running_list_of_sales_history_items: list[PosabitSalesHistoryObject] = []
 
        # note that if we want to restrict the date range, we need to add the following to the url:
        # q[updated_at_gt]={start_date.isoformat(timespec='milliseconds').replace('+00:00','Z')}&q[updated_at_lt]={end_date.isoformat(timespec='milliseconds').replace('+00:00','Z')}
         
        print("Posabit integration retrieving sales data")
        
        results = self.service_caller.get(
            url = f"{url}",
            headers = {"Authorization": f"Bearer {pos_integration_key}"},
            simulator_response_id = simulator_response_id
        ) 
       
        var = results.json()
        posabit_sales_histories =  PosabitSalesHistoriesResponse(**results.json())
        
        running_list_of_sales_history_items += [PosabitSalesHistoryObject(**item) for item in posabit_sales_histories.sales_histories]
        
        total_pages = posabit_sales_histories.total_pages or 1
        current_page = 2
        
        while current_page <= total_pages and simulator_response_id is None:
             
            url = self.resolve_date_range_url(
                base_url = f"https://app.posabit.com/api/v2/venue/sales_histories",
                start_time = start_time,
                end_time = end_time,
                page = current_page
            )
             
            next_page_of_results = self.service_caller.get(
                url = f"{url}",
                headers = {"Authorization": f"Bearer {pos_integration_key}"},
                simulator_response_id = simulator_response_id
            ) 
                
            next_page_of_posabit_inventories =  PosabitSalesHistoriesResponse(**next_page_of_results.json())
            running_list_of_sales_history_items += [PosabitSalesHistoryObject(**item) for item in posabit_sales_histories.sales_histories]
            current_page = next_page_of_posabit_inventories.current_page + 1
            total_pages = next_page_of_posabit_inventories.total_pages
                
        return running_list_of_sales_history_items
        
    def get_inventory_snapshots(
        self,  
        integration_key: str,
        simulator_response_id: UUID | None = None
    ) -> list[GenericInventoryObject] | None:
        return_list: list[GenericInventoryObject] = [] 
        
        inventory_items = self.get_all_pages_of_inventory_items(integration_key, simulator_response_id = simulator_response_id)
         
        for inventory_item in inventory_items:
              
            samson_inventory_snapshot_item = self.convert_from_posabit_inventory_object_to_generic_inventory_object( 
                posabit_inventory_object= inventory_item
            )
            
            return_list.append(samson_inventory_snapshot_item)
        
        return return_list 

    def get_historical_sales(
        self,  
        integration_key: str,
        start_time: datetime,
        end_time: datetime | None = None,
        simulator_response_id: UUID | None = None
    ) -> list[GenericInventoryObject] | None:
        return_list: list[GenericInventoryObject] = [] 
        
        sales = self.get_all_pages_of_sales(
            integration_key, 
            start_time=start_time, 
            end_time=end_time,
            simulator_response_id = simulator_response_id
        )
         
        for sale in sales:
              
            samson_inventory_snapshot_item = self.convert_from_posabit_sales_history_object_to_generic_historical_sale_object( 
                posabit_sales_history_object = sale
            )
            
            return_list.append(samson_inventory_snapshot_item)
        
        return return_list 

    def convert_from_posabit_inventory_object_to_generic_inventory_object(
        self,  
        posabit_inventory_object: PosabitInventoryObject, 
 
    ) -> GenericInventoryObject:
        return GenericInventoryObject( 
            sku = posabit_inventory_object.sku,
            stock_on_hand= posabit_inventory_object.quantity_on_hand,
            price = posabit_inventory_object.price,  
            product_name= posabit_inventory_object.name,
            listed_vendor = posabit_inventory_object.vendor,
            listed_brand = posabit_inventory_object.brand,
            listed_category = posabit_inventory_object.category,
        )  
    
    def convert_from_posabit_sales_history_object_to_generic_historical_sale_object(
        self,  
        posabit_sales_history_object: PosabitSalesHistoryObject,  
    ) -> GenericHistoricalSaleObject:
        
        sales_object = GenericHistoricalSaleObject( 
            pos_sale_id = posabit_sales_history_object.id,
            sale_timestamp = posabit_sales_history_object.ordered_at,
            total = posabit_sales_history_object.total,   
            
            sub_total = posabit_sales_history_object.sub_total,
            discount = posabit_sales_history_object.discount,
            tax = posabit_sales_history_object.tax,
            cost = posabit_sales_history_object.cost,  
        )  
         
        sales_object.items = [self.convert_from_posabit_sales_history_item_to_generic_historical_sale_item(item, posabit_sales_history_object) for item in posabit_sales_history_object.items]
        
        return sales_object
    
    
    def convert_from_posabit_sales_history_item_to_generic_historical_sale_item(
        self,  
        posabit_sale_item_object: PosabitSalesHistoryItemObject,  
        posabit_sales_history_object: PosabitSalesHistoryObject
    ) -> GenericHistoricalSaleItemObject:
        
        sales_object = GenericHistoricalSaleItemObject( 
            cost=posabit_sale_item_object.cost,
            discount=posabit_sale_item_object.discount, 
            quantity=posabit_sale_item_object.quantity,
            sku=posabit_sale_item_object.sku,
            sub_total=posabit_sale_item_object.sub_total,
            tax=posabit_sale_item_object.tax,
            total=posabit_sale_item_object.total,
            unit_of_weight=posabit_sale_item_object.unit_of_weight,
            weight_in_units=posabit_sale_item_object.weight,
            product_name=posabit_sale_item_object.product_name, 
            listed_brand=posabit_sale_item_object.brand,
            listed_category=posabit_sale_item_object.category,
            lot_identifier=posabit_sale_item_object.lot_number,
            pos_product_id=posabit_sale_item_object.product_id,
            pos_sale_id=posabit_sale_item_object.sales_history_id, 
            sale_product_name=posabit_sale_item_object.product_name,
            sale_timestamp=posabit_sales_history_object.ordered_at,
             
        )  
          
        return sales_object 
    
    def resolve_date_range_url(
        self,
        base_url: str,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        page: int = 1,
    ) -> str:
        
        does_a_param_already_exist = False
        result_str = base_url
 
        if(start_time is not None):
            if(not does_a_param_already_exist):
                result_str += "?"
            else:
                result_str += "&"
            result_str += f"q[updated_at_gt]={start_time.isoformat(timespec='milliseconds').replace('+00:00','Z')}"
            
            does_a_param_already_exist = True
            
        if(end_time is not None):
            if(not does_a_param_already_exist):
                result_str += "?"
            else:
                result_str += "&"
            result_str += f"q[updated_at_lt]={end_time.isoformat(timespec='milliseconds').replace('+00:00','Z')}"
            
            does_a_param_already_exist = True
            
        if(page is not None):
            if(not does_a_param_already_exist):
                result_str += "?"
            else:
                result_str += "&"
            result_str += f"page={page}"
            
        return result_str