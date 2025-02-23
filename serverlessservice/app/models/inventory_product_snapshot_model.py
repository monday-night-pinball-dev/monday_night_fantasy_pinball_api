from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Optional
from uuid import UUID
from fastapi import Query
from pydantic import UUID4, BaseModel, BeforeValidator, EmailStr, Field, Strict
from pydantic_core import PydanticUndefined
from enum import Enum

from models.inventory_intake_job_model import InventoryIntakeJobModel, InventoryIntakeJobOutboundModel
from models.product_model import ProductModel, ProductOutboundModel
from models.retailer_location_model import RetailerLocationModel, RetailerLocationOutboundModel
from models.retailer_model import RetailerModel, RetailerOutboundModel
from models.vendor_model import VendorModel, VendorOutboundModel


class InventoryProductSnapshotStatuses(str, Enum):
    Requested = 'Requested'
    Processing = 'Processing'
    Completed = 'Completed'
    Failed = 'Failed' 
 
from models.common_model import (
    CommonDatabaseModel,
    CommonInboundSearchModel,
    CommonModel,
    CommonOutboundResponseModel,
    CommonSearchModel,
    validate_ids,
)


# Pydantic causes these class variables to safely be instance variables.
class InventoryProductSnapshotInboundCreateModel(BaseModel):  
    retailer_location_id: Annotated[UUID4, Strict(False)] = Field(...)
    product_id: Annotated[UUID4, Strict(False)] = Field(...) 
    inventory_intake_job_id: Optional[Annotated[UUID4, Strict(False)]] = Field(default=None)
    
    snapshot_hour: datetime = Field(...)   
    sku: str = Field(..., max_length=255)
    stock_on_hand: int = Field(...)
    price: int = Field(...) 
  

# Pydantic causes these class variables to safely be instance variables.
class InventoryProductSnapshotInboundSearchModel(CommonInboundSearchModel): 
    snapshot_hour_min: Optional[datetime] = Query(default=None) 
    snapshot_hour_max: Optional[datetime] = Query(default=None) 
    retailer_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    retailer_location_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    product_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    vendor_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    inventory_intake_job_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None)
    sku: Optional[str] = Query(default=None) 

class InventoryProductSnapshotCreateModel:

    def __init__(
        self,
        product_id: UUID,       
        retailer_location_id: UUID,
        snapshot_hour: datetime ,
        sku: str ,
        stock_on_hand: int ,
        price: int, 
        retailer_id: UUID | None = None,
        vendor_id: UUID | None = None,
        inventory_intake_job_id: UUID | None = None, 
    ) -> None:
    
        self.retailer_location_id = retailer_location_id
        self.product_id = product_id
        self.inventory_intake_job_id = inventory_intake_job_id
        self.retailer_id = retailer_id
        self.vendor_id = vendor_id
        self.snapshot_hour = snapshot_hour
        self.sku = sku
            
        self.stock_on_hand = stock_on_hand
        self.price = price 
  
class InventoryProductSnapshotSearchModel(CommonSearchModel):

    def __init__(
        self,
        ids: list[UUID] | None = None,
        retailer_ids: list[UUID] | None = None,
        retailer_location_ids: list[UUID] | None = None,
        snapshot_hour_min: datetime | None = None, 
        snapshot_hour_max: datetime | None = None, 
        product_ids: list[UUID] | None = None,
        vendor_ids: list[UUID] | None = None,
        inventory_intake_job_ids: list[UUID] | None = None, 
        
        sku: str | None = None,
    ) -> None:

        super().__init__(ids)

        self.retailer_ids = retailer_ids
        self.retailer_location_ids = retailer_location_ids
        self.snapshot_hour_min = snapshot_hour_min
        self.snapshot_hour_max = snapshot_hour_max
        self.product_ids = product_ids
        self.vendor_ids = vendor_ids
        self.inventory_intake_job_ids = inventory_intake_job_ids 
        self.sku = sku


class InventoryProductSnapshotDatabaseModel(CommonDatabaseModel):

    def __init__(
        self,
        id: UUID,
        retailer_id: UUID,
        retailer_location_id: UUID,
        product_id: UUID,
        sku: str,
        stock_on_hand: int,
        price: int,
        snapshot_hour: datetime ,
        created_at: datetime,
        inventory_intake_job_id: UUID | None = None, 
        vendor_id: UUID | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)
        
        self.retailer_location_id
        self.retailer_id=retailer_id
        self.product_id = product_id
        self.retailer_location_id = retailer_location_id
        self.inventory_intake_job_id = inventory_intake_job_id
        self.snapshot_hour = snapshot_hour
        self.sku = sku
        self.stock_on_hand = stock_on_hand
        self.price = price 
        self.vendor_id = vendor_id


class InventoryProductSnapshotModel(CommonModel):

    def __init__(
        self,
        id: UUID,
        retailer_id: UUID,
        retailer_location_id: UUID,
        product_id: UUID,
        snapshot_hour: datetime,
        sku: str,
        stock_on_hand: int,
        price: int,
        created_at: datetime, 
        inventory_intake_job_id: UUID | None = None, 
        retailer: RetailerModel | None = None,
        retailer_location: RetailerLocationModel | None = None,
        product: ProductModel | None = None,
        vendor: VendorModel | None = None,
        inventory_intake_job: InventoryIntakeJobModel | None = None,
        vendor_id: UUID | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)
        
        self.retailer_location_id = retailer_location_id
        self.retailer_id = retailer_id
        self.product_id = product_id
        self.retailer_location_id = retailer_location_id
        self.inventory_intake_job_id = inventory_intake_job_id
        self.snapshot_hour = snapshot_hour
        self.sku = sku
        self.stock_on_hand = stock_on_hand
        self.price = price 
        self.vendor_id = vendor_id
        
        self.retailer = retailer
        self.retailer_location = retailer_location
        self.product = product
        self.vendor = vendor
        self.inventory_intake_job = inventory_intake_job

# Pydantic causes these class variables to safely be instance variables.
class InventoryProductSnapshotOutboundModel(CommonOutboundResponseModel):
     
    retailer_id: UUID
    retailer_location_id: UUID
    product_id: UUID
    created_at: str
    sku: str
    stock_on_hand: int
    price: int
    snapshot_hour: str 
    inventory_intake_job_id: UUID | None = None  
    vendor_id: UUID | None = None
    retailer: RetailerOutboundModel | None = None,
    retailer_location: RetailerLocationOutboundModel | None = None,
    product: ProductOutboundModel | None = None,
    vendor: VendorOutboundModel | None = None,
    inventory_intake_job: InventoryIntakeJobOutboundModel | None = None,
