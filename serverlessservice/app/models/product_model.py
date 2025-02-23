from datetime import datetime
from enum import Enum
from typing import Annotated, Optional, Self
from uuid import UUID
from fastapi import Query
from pydantic import UUID4, BaseModel, BeforeValidator, EmailStr, Field, Strict

from models.common_model import (
    CommonDatabaseModel,
    CommonInboundSearchModel,
    CommonModel,
    CommonOutboundResponseModel,
    CommonSearchModel,
    DicsPhoneNumber,
    validate_ids,
)
from models.retailer_location_model import RetailerLocationModel, RetailerLocationOutboundModel
from models.retailer_model import RetailerModel, RetailerOutboundModel
from models.vendor_model import VendorModel, VendorOutboundModel

class ProductVendorConfirmationStatuses(Enum):
    Candidate = 'Candidate'
    ConfirmedByVendor = 'ConfirmedByVendor' 
    DeniedByVendor = 'DeniedByVendor' 
    Discontinued = 'Discontinued' 
    Unknown = 'Unknown'  

# Pydantic causes these class variables to safely be instance variables.
class ProductInboundCreateModel(BaseModel): 
    referring_retailer_location_id: Optional[Annotated[UUID4, Strict(False)]] = Field(default=None) 
    vendor_id: Optional[Annotated[UUID4, Strict(False)]] = Field(default=None)  
    confirmed_core_product_id: Optional[Annotated[UUID4, Strict(False)]] = Field(default=None) 
    
    name: str = Field(..., max_length=255)
    vendor_sku: Optional[str] = Field(..., max_length=255)
    vendor_confirmation_status: Optional[ProductVendorConfirmationStatuses] = Field(default = None)
    


# Pydantic causes these class variables to safely be instance variables.
class ProductInboundUpdateModel(BaseModel):
    vendor_id: Optional[Annotated[UUID4, Strict(False)]] = Field(default=None)  
    confirmed_core_product_id: Optional[Annotated[UUID4, Strict(False)]] = Field(default=None) 
    vendor_confirmation_status: Optional[ProductVendorConfirmationStatuses] = Field(default = None)    
    name: Optional[str] = Field(default = None, max_length=255)
    vendor_sku: Optional[str] = Field(default = None, max_length=255)
    vendor_confirmation_status: Optional[ProductVendorConfirmationStatuses] = Field(default = None)

# Pydantic causes these class variables to safely be instance variables.
class ProductInboundSearchModel(CommonInboundSearchModel):
    name: Optional[str] = Query(default=None)
    name_like: Optional[str] = Query(default=None)
    referring_retailer_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    referring_retailer_location_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    vendor_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    confirmed_core_product_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    vendor_sku: Optional[str] = Query(default=None) 
    vendor_confirmation_status: Optional[ProductVendorConfirmationStatuses] = Query(default=None)
    location_country: Optional[str] = Query(default=None)


class ProductCreateModel:

    def __init__(
        self,
        name: str,
        vendor_sku: str | None = None, 
        referring_retailer_id: UUID | None = None,
        referring_retailer_location_id: UUID | None = None,
        vendor_id: UUID | None = None,
        confirmed_core_product_id: UUID | None = None,  
        vendor_confirmation_status: ProductVendorConfirmationStatuses | None = None,
        proposed_vendor_name: str | None = None,
        proposed_category: str | None = None,
        proposed_brand: str | None = None,
    ) -> None:

        self.name = name
        self.vendor_sku = vendor_sku 
        self.referring_retailer_id = referring_retailer_id
        self.referring_retailer_location_id = referring_retailer_location_id
        self.vendor_id = vendor_id
            
        self.confirmed_core_product_id = confirmed_core_product_id
        self.vendor_confirmation_status = vendor_confirmation_status
        self.proposed_vendor_name = proposed_vendor_name
        self.proposed_category = proposed_category
        self.proposed_brand = proposed_brand


class ProductUpdateModel:

    def __init__(
        self,
        name: str | None = None,
        vendor_sku: str | None = None,  
        vendor_id: UUID | None = None,
        confirmed_core_product_id: UUID | None = None,  
        vendor_confirmation_status: ProductVendorConfirmationStatuses | None = None,
    ) -> None:

        self.name = name 
        self.vendor_sku = vendor_sku 
        self.vendor_id = vendor_id
        self.confirmed_core_product_id = confirmed_core_product_id
        self.vendor_confirmation_status = vendor_confirmation_status
 
class ProductSearchModel(CommonSearchModel):

    def __init__(
        self,
        ids: list[UUID] | None = None,
        referring_retailer_ids: list[UUID] | None = None, 
        referring_retailer_location_ids: list[UUID] | None = None,  
        vendor_ids: list[UUID] | None = None,  
        confirmed_core_product_ids: list[UUID] | None = None,  
        
        name: str | None = None,
        name_like: str | None = None,
        vendor_sku: str | None = None,
        vendor_confirmation_status: ProductVendorConfirmationStatuses | None = None,
 
    ) -> None:

        super().__init__(ids)

        self.name = name
                
        self.name_like = name_like
        self.vendor_sku = vendor_sku
        self.referring_retailer_ids = referring_retailer_ids 
        self.referring_retailer_location_ids = referring_retailer_location_ids
        self.vendor_ids = vendor_ids
        self.confirmed_core_product_ids = confirmed_core_product_ids 
        self.vendor_confirmation_status = vendor_confirmation_status

class ProductDatabaseModel(CommonDatabaseModel):

    def __init__(
        self,
        id: UUID, 
        name: str,
        created_at: datetime, 
        vendor_confirmation_status: ProductVendorConfirmationStatuses,
        vendor_sku: str | None = None,
        referring_retailer_id: UUID | None = None,
        referring_retailer_location_id: UUID | None = None,
        vendor_id: UUID | None = None,
        confirmed_core_product_id: UUID | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)

        self.id = id
        self.name = name
        self.vendor_sku = vendor_sku
            
        self.referring_retailer_id = referring_retailer_id
        self.referring_retailer_location_id = referring_retailer_location_id
        self.vendor_id = vendor_id
        self.confirmed_core_product_id = confirmed_core_product_id
        self.vendor_confirmation_status = vendor_confirmation_status 

class ProductModel(CommonModel):

    def __init__(
        self,
        id: UUID, 
        name: str,
        created_at: datetime, 
        vendor_confirmation_status: ProductVendorConfirmationStatuses,
        vendor_sku: str | None = None,
        referring_retailer_id: UUID | None = None,
        referring_retailer_location_id: UUID | None = None,
        vendor_id: UUID | None = None,
        confirmed_core_product_id: UUID | None = None,
        referring_retailer: RetailerModel | None = None,
        referring_retailer_location: RetailerLocationModel | None = None,
        vendor: VendorModel | None = None,
        confirmed_core_product: Self | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)

        self.name = name
            
        self.vendor_sku = vendor_sku
        self.vendor_confirmation_status = vendor_confirmation_status
        self.referring_retailer_id = referring_retailer_id
        self.referring_retailer_location_id = referring_retailer_location_id
        self.vendor_id = vendor_id
        self.confirmed_core_product_id = confirmed_core_product_id     
        
        self.referring_retailer = referring_retailer
        self.referring_retailer_location = referring_retailer_location
        self.vendor = vendor
        self.confirmed_core_product = confirmed_core_product

 
# Pydantic causes these class variables to safely be instance variables.
class ProductOutboundModel(CommonOutboundResponseModel):
    name: str
    vendor_sku: str | None = None
    referring_retailer_id: UUID | None = None
    referring_retailer_location_id: UUID | None = None
    vendor_id: UUID | None = None
    confirmed_core_product_id: UUID | None = None
    vendor_confirmation_status: ProductVendorConfirmationStatuses | None = None
    referring_retailer: RetailerOutboundModel | None = None
    referring_retailer_location: RetailerLocationOutboundModel | None = None
    vendor: VendorOutboundModel | None = None
    confirmed_core_product: Self | None = None
