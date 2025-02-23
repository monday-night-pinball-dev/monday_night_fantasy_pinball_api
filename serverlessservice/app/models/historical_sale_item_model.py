from datetime import datetime
from enum import Enum
from typing import Annotated, Optional
from uuid import UUID
from fastapi import Query
from pydantic import UUID4, BaseModel, BeforeValidator, Field, Strict 
from enum import Enum

from models.product_model import ProductModel, ProductOutboundModel
from models.retailer_location_model import RetailerLocationModel, RetailerLocationOutboundModel
from models.retailer_model import RetailerModel, RetailerOutboundModel
from models.sales_intake_job_model import SalesIntakeJobModel, SalesIntakeJobOutboundModel
from models.vendor_model import VendorModel, VendorOutboundModel 
from models.historical_sale_model import HistoricalSaleModel, HistoricalSaleOutboundModel

class ProductUnitOfMeasurements(str, Enum):
    Milligrams  = 'Milligrams'
    Grams = 'Grams'
    Kilograms = 'Kilograms'
    Pounds = 'Pounds'
    Ounces = 'Ounces'
    FluidOunces = 'FluidOunces'
    Pints = 'Pints'
    Quarts = 'Quarts'
    Gallons = 'Gallons'
    Liters = 'Liters'
    Milliliters = 'Milliliters'
    
from models.common_model import (
    CommonDatabaseModel,
    CommonInboundSearchModel,
    CommonModel,
    CommonOutboundResponseModel,
    CommonSearchModel,
    validate_ids,
) 
 
# Pydantic causes these class variables to safely be instance variables.
class HistoricalSaleItemInboundCreateModel(BaseModel):  
    historical_sale_id: Annotated[UUID4, Strict(False)] = Field(...)  
    product_id: Annotated[UUID4, Strict(False)] = Field(...) 
    
    pos_product_id: Optional[str] = Field(default=None, max_length=255)
    pos_sale_id: Optional[str] = Field(default=None, max_length=255)

    lot_identifier: Optional[str] = Field(default=None, max_length=255)
    sale_count: float = Field(...) 
    unit_of_weight: Optional[ProductUnitOfMeasurements] = Field(default=None, max_length=32)
    weight_in_units: Optional[float] = Field( default=None)
    sale_product_name: Optional[str] = Field(default=None, max_length=255)
    
    sale_timestamp: datetime = Field(...)   
    
    sku: str = Field(..., max_length=255) 
    sub_total: Optional[int] = Field( default=None)
    discount:  Optional[int] = Field( default=None)
    tax:  Optional[int] = Field( default=None)
    total: int = Field(...)
    cost:  Optional[int] = Field( default=None)
    
  

# Pydantic causes these class variables to safely be instance variables.
class HistoricalSaleItemInboundSearchModel(CommonInboundSearchModel): 
    pos_sale_ids: Optional[str] = Query(default=None)
    pos_product_ids: Optional[str] = Query(default=None)
    lot_identifiers: Optional[str] = Query(default=None)
    
    historical_sale_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None)
    sales_intake_job_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None)
    product_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None)
    product_vendor_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None)
    retailer_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    retailer_location_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    sale_timestamp_min:  Optional[datetime] = Query(default=None) 
    sale_timestamp_max: Optional[datetime] = Query(default=None) 
    skus: Optional[str] = Query(default=None)
    sale_product_name: Optional[str] = Query(default=None)
    

class HistoricalSaleItemCreateModel:

    
    def __init__(
        self,
        product_id: UUID,
        historical_sale_id: UUID,
        sku: str,
        sale_count: float,
        sale_timestamp: datetime, 
        total: int, 
        retailer_id: UUID | None = None, 
        sales_intake_job_id: UUID | None = None, 
        retailer_location_id: UUID | None = None,
        product_vendor_id: UUID | None = None, 
        sale_product_name: str | None = None,
        lot_identifier: str | None = None,
        pos_sale_id: str | None = None,
        pos_product_id: str | None = None,
        unit_of_weight: ProductUnitOfMeasurements | None = None,
        weight_in_units: float | None = None,
        sub_total: int | None = None,
        discount: int | None = None,
        tax: int | None = None,
        cost : int | None = None,
    ) -> None:
    
        self.retailer_location_id = retailer_location_id
        self.product_id = product_id
        self.sales_intake_job_id = sales_intake_job_id
        self.historical_sale_id = historical_sale_id
        self.pos_sale_id = pos_sale_id
        self.pos_product_id = pos_product_id
        self.total = total
        self.sub_total = sub_total
        self.discount = discount
        
        self.tax = tax
        self.cost = cost
        self.retailer_id = retailer_id
        self.product_vendor_id = product_vendor_id
        self.sale_product_name = sale_product_name
        self.lot_identifier = lot_identifier
        self.unit_of_weight = unit_of_weight
        self.weight_in_units = weight_in_units
        self.sale_count = sale_count
        self.sku = sku
        self.sale_timestamp = sale_timestamp 
    
  
class HistoricalSaleItemSearchModel(CommonSearchModel): 
 
    
    def __init__(
        self,
        ids: list[UUID] | None = None,
        retailer_ids: list[UUID] | None = None,
        retailer_location_ids: list[UUID] | None = None,
        product_ids: list[UUID] | None = None,
        product_vendor_ids: list[UUID] | None = None,
        sales_intake_job_ids: list[UUID] | None = None, 
        pos_sale_ids: list[str] | None = None,
        pos_product_ids: list[str] | None = None,
        lot_identifiers: list[str] | None = None,
        historical_sale_ids: list[UUID] | None = None,
        skus: list[str] | None = None,
        sale_product_name: str | None = None,
        sale_timestamp_min: datetime | None = None,
        sale_timestamp_max: datetime | None = None 
    ) -> None:

        super().__init__(ids)

        self.retailer_ids = retailer_ids
        self.retailer_location_ids = retailer_location_ids
        self.product_ids = product_ids
        self.product_vendor_ids = product_vendor_ids
        self.sales_intake_job_ids = sales_intake_job_ids
        self.pos_sale_ids = pos_sale_ids
        self.pos_product_ids = pos_product_ids
        self.lot_identifiers = lot_identifiers
        self.historical_sale_ids = historical_sale_ids
        self.skus = skus
        self.sale_product_name = sale_product_name
        self.sale_timestamp_min = sale_timestamp_min
        self.sale_timestamp_max = sale_timestamp_max 


class HistoricalSaleItemDatabaseModel(CommonDatabaseModel):

    def __init__(
        self,
        id: UUID,
        product_id: UUID,
        retailer_id: UUID,
        retailer_location_id: UUID,
        historical_sale_id: UUID,
        sale_timestamp: datetime,
        sku: str,
        sale_count: float,
        total: int,
        created_at: datetime, 
        sub_total: int | None = None,
        pos_sale_id: str | None = None,
        pos_product_id: str | None = None, 
        lot_identifier: str | None = None,
        unit_of_weight: ProductUnitOfMeasurements | None = None,
        weight_in_units: float | None = None,
        sale_product_name: str | None = None,
        discount: int | None = None,
        tax: int | None = None,
        cost : int | None = None,
        
        product_vendor_id: UUID | None = None,  
        sales_intake_job_id: UUID | None = None,  
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)
 
        self.product_id = product_id
        self.product_vendor_id = product_vendor_id
        self.retailer_id = retailer_id
        self.retailer_location_id = retailer_location_id
        self.sales_intake_job_id = sales_intake_job_id 
        self.historical_sale_id = historical_sale_id
        self.pos_sale_id = pos_sale_id
        self.pos_product_id = pos_product_id
        self.lot_identifier = lot_identifier
        self.unit_of_weight = unit_of_weight
        self.weight_in_units = weight_in_units
        self.sale_product_name = sale_product_name
        self.sale_timestamp = sale_timestamp
        self.sku = sku
        self.sale_count = sale_count
        self.total = total
        self.sub_total = sub_total
        self.discount = discount
        self.tax = tax
        self.cost = cost  
         
         
class HistoricalSaleItemModel(CommonModel):
  
    def __init__(
        self,
        id: UUID,
        product_id: UUID,
        retailer_id: UUID,
        retailer_location_id: UUID,
        historical_sale_id: UUID,
        sale_timestamp: datetime,
        sku: str,
        sale_count: float,
        total: int,
        created_at: datetime, 
        sub_total: int | None = None,
        pos_sale_id: str | None = None,
        pos_product_id: str | None = None, 
        lot_identifier: str | None = None,
        unit_of_weight: ProductUnitOfMeasurements | None = None,
        weight_in_units: float | None = None,
        sale_product_name: str | None = None,
        discount: int | None = None,
        tax: int | None = None,
        cost : int | None = None,
        
        product_vendor_id: UUID | None = None,  
        sales_intake_job_id: UUID | None = None,
        product: ProductModel | None = None,
        retailer: RetailerModel | None = None,
        retailer_location: RetailerLocationModel | None = None,
        historical_sale: HistoricalSaleModel | None = None,
        sales_intake_job: SalesIntakeJobModel | None = None,
        product_vendor: VendorModel | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)
        
        self.product_id = product_id
        self.product_vendor_id = product_vendor_id
        self.retailer_id = retailer_id
        self.retailer_location_id = retailer_location_id
        self.sales_intake_job_id = sales_intake_job_id 
        self.historical_sale_id = historical_sale_id
        self.pos_sale_id = pos_sale_id
        self.pos_product_id = pos_product_id
        self.lot_identifier = lot_identifier
        self.unit_of_weight = unit_of_weight
        self.weight_in_units = weight_in_units
        self.sale_product_name = sale_product_name
        self.sale_timestamp = sale_timestamp
        self.sku = sku
        self.sale_count = sale_count
        self.total = total
        self.sub_total = sub_total
        self.discount = discount
        self.tax = tax
        self.cost = cost  
        
        self.product = product
        self.retailer = retailer
        self.retailer_location = retailer_location
        self.historical_sale = historical_sale
        self.sales_intake_job = sales_intake_job
        self.product_vendor = product_vendor
        
    
        
# Pydantic causes these class variables to safely be instance variables.
class HistoricalSaleItemOutboundModel(CommonOutboundResponseModel):

    product_id: UUID
    retailer_id: UUID
    retailer_location_id: UUID
    historical_sale_id: UUID
    sale_timestamp: str
    sku: str
    sale_count: float
    total: int
    sub_total: int | None = None
    pos_sale_id: str | None = None
    pos_product_id: str | None = None
    lot_identifier: str | None = None
    unit_of_weight: ProductUnitOfMeasurements | None = None
    weight_in_units: float | None = None
    sale_product_name: str | None = None
    discount: int | None = None
    tax: int | None = None
    cost : int | None = None
    
    product_vendor_id: UUID | None = None 
    sales_intake_job_id: UUID | None = None  
    
    product: ProductOutboundModel | None = None
    retailer: RetailerOutboundModel | None = None
    retailer_location: RetailerLocationOutboundModel | None = None
    historical_sale: HistoricalSaleOutboundModel | None = None
    sales_intake_job: SalesIntakeJobOutboundModel | None = None
    product_vendor: VendorOutboundModel | None = None
