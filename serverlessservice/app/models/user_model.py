from datetime import datetime
from enum import Enum
from typing import Annotated, Optional
from uuid import UUID
from fastapi import Query
from pydantic import UUID4, BaseModel, BeforeValidator, EmailStr, Field, Strict 

from models.common_model import (
    CommonDatabaseModel,
    CommonInboundSearchModel,
    CommonModel,
    CommonOutboundResponseModel,
    CommonSearchModel, 
    validate_ids,
)

class UserRoles(Enum):
    SamsonAdmin = 'SamsonAdmin'
    SamsonUser = 'SamsonUser' 
    RetailerAdmin = 'RetailerAdmin' 
    RetailerUser = 'RetailerUser' 
    RetailerManager = 'RetailerManager' 
    VendorAdmin = 'VendorAdmin'
    VendorUser = 'VendorUser' 
    
# Pydantic causes these class variables to safely be instance variables.
class UserInboundCreateModel(BaseModel):

    vendor_id: Optional[Annotated[UUID4, Strict(False)]] = Field(default=None) 
    retailer_location_id: Optional[Annotated[UUID4, Strict(False)]] = Field(default=None)  
    
    role: UserRoles = Field(...)
 
    first_name: str = Field(..., max_length=255)
    last_name: str = Field(..., max_length=255)
    username: EmailStr = Field(..., max_length=320)

# Pydantic causes these class variables to safely be instance variables.
class UserInboundUpdateModel(BaseModel):
    first_name: Optional[str] = Field(default=None, max_length=255)
    last_name: Optional[str] = Field(default=None, max_length=255) 
    role: Optional[UserRoles] = Field(default=None) 


# Pydantic causes these class variables to safely be instance variables.
class UserInboundSearchModel(CommonInboundSearchModel):
    username_like: Optional[str] = Query(default=None) 
    username: Optional[str] = Query(default=None) 
    name_like: Optional[str] = Query(default=None) 
    role: Optional[UserRoles] = Query(default=None)
    vendor_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    retailer_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    retailer_location_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None)


class UserCreateModel: 
    def __init__(
        self,
        username: str, 
        first_name: str, 
        last_name: str, 
        role: UserRoles,
        retailer_id: UUID | None = None, 
        retailer_location_id: UUID | None = None, 
        vendor_id: UUID | None = None, 
    ) -> None:

        self.username = username
        self.first_name = first_name
        self.last_name = last_name 
        self.role = role
        self.retailer_id = retailer_id
        self.retailer_location_id = retailer_location_id
        self.vendor_id = vendor_id 


class UserUpdateModel:

    def __init__(
        self,        
        first_name: str, 
        last_name: str, 
        role: UserRoles, 
    ) -> None:

        self.first_name = first_name
        self.last_name = last_name
        self.role = role

class UserSearchModel(CommonSearchModel):

    def __init__(
        self,
        ids: list[UUID] | None = None,
        retailer_ids: list[UUID] | None = None,  
        retailer_location_ids: list[UUID] | None = None,  
        vendor_ids: list[UUID] | None = None,   
        name_like: str | None = None,
        username_like: str | None = None,
        username: str | None = None,
        role: UserRoles | None = None,
   
    ) -> None:

        super().__init__(ids)

        self.retailer_ids = retailer_ids
        self.retailer_location_ids = retailer_location_ids
        self.vendor_ids = vendor_ids
        self.name_like = name_like
        self.username = username
        self.username_like = username_like
        self.role = role

class UserDatabaseModel(CommonDatabaseModel):

    def __init__(
        self,
        id: UUID,
        username: str,
        first_name: str,
        last_name: str,
        full_name: str,
        role: UserRoles,
        created_at: datetime,  
        retailer_id: UUID | None = None,
        retailer_location_id: UUID | None = None,
        vendor_id: UUID | None = None, 
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)

        self.first_name = first_name 
        self.last_name = last_name 
        self.username = username
        self.full_name = full_name
        self.role = role 
        self.first_name = first_name 
        self.retailer_id = retailer_id 
        self.retailer_location_id = retailer_location_id
        self.vendor_id = vendor_id  

class UserModel(CommonModel):

    def __init__(
        self,
        id: UUID,
        username: str,
        first_name: str,
        last_name: str,
        full_name: str,
        role: UserRoles,
        created_at: datetime,  
        retailer_id: UUID | None = None,
        retailer_location_id: UUID | None = None,
        vendor_id: UUID | None = None, 
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)
 
        self.username = username 
        self.first_name = first_name 
        self.last_name = last_name 
        self.full_name = full_name 
        self.role = role 
        self.first_name = first_name 
        self.retailer_id = retailer_id 
        self.retailer_location_id = retailer_location_id
        self.vendor_id = vendor_id  


# Pydantic causes these class variables to safely be instance variables.
class UserOutboundModel(CommonOutboundResponseModel):
    
    retailer_id: UUID | None = None 
    retailer_location_id: UUID | None = None 
    vendor_id: UUID | None = None 
    
    username: str
    first_name: str
    last_name: str
    full_name: str
    role: UserRoles