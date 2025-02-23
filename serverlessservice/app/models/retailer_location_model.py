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
    DicsPhoneNumber,
    validate_ids,
)
from models.retailer_model import RetailerModel, RetailerOutboundModel

class RetailerLocationAccountStatuses(Enum):
    Unregistered = 'Unregistered'
    RegisteredInactive = 'RegisteredInactive' 
    RegisteredActive = 'RegisteredActive' 
    PausedByRequest = 'PausedByRequest' 
    PausedByBilling = 'PausedByBilling' 
    Deactivated = 'Deactivated'

# Pydantic causes these class variables to safely be instance variables.
class RetailerLocationInboundCreateModel(BaseModel):
    name: str = Field(..., max_length=255)
    retailer_id: Annotated[UUID4, Strict(False)] = Field(...)
    contact_email: Optional[EmailStr] = Field(default=None, max_length=320)
    contact_phone: Optional[DicsPhoneNumber] = Field(default=None, max_length=32)
    location_city: Optional[str] = Field(default=None, max_length=255)
    location_state: Optional[str] = Field(default=None, max_length=255)
    location_country: Optional[str] = Field(default=None, max_length=2, min_length=2)
    account_status: Optional[RetailerLocationAccountStatuses] = Field(default = None)


# Pydantic causes these class variables to safely be instance variables.
class RetailerLocationInboundUpdateModel(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255) 
    contact_email: Optional[EmailStr] = Field(default=None, max_length=320)
    contact_phone: Optional[DicsPhoneNumber] = Field(default=None, max_length=32)
    location_city: Optional[str] = Field(default=None, max_length=255)
    location_state: Optional[str] = Field(default=None, max_length=255)
    location_country: Optional[str] = Field(default=None, max_length=2, min_length=2)
    account_status: Optional[RetailerLocationAccountStatuses] = Field(default = None)


# Pydantic causes these class variables to safely be instance variables.
class RetailerLocationInboundSearchModel(CommonInboundSearchModel):
    name: Optional[str] = Query(default=None)
    name_like: Optional[str] = Query(default=None)
    retailer_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    account_status: Optional[RetailerLocationAccountStatuses] = Query(default=None)
    location_city: Optional[str] = Query(default=None)
    location_state: Optional[str] = Query(default=None)
    location_country: Optional[str] = Query(default=None)


class RetailerLocationCreateModel:

    def __init__(
        self,
        name: str,
        retailer_id: UUID,
        contact_email: EmailStr | None = None,
        contact_phone: DicsPhoneNumber | None = None, 
        location_city: str | None = None,
        location_state: str | None = None,
        location_country: str | None = None,
        account_status: RetailerLocationAccountStatuses | None = None,
    ) -> None:

        self.name = name
        self.retailer_id = retailer_id 
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.location_city = location_city
        self.location_state = location_state
        self.location_country = location_country
        self.account_status = account_status


class RetailerLocationUpdateModel:

    def __init__(
        self,
        name: str | None = None, 
        contact_email: EmailStr | None = None,
        contact_phone: DicsPhoneNumber | None = None,
        location_city: str | None = None,
        location_state: str | None = None,
        location_country: str | None = None,
        account_status: RetailerLocationAccountStatuses | None = None,
    ) -> None:

        self.name = name 
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.location_city = location_city
        self.location_state = location_state
        self.location_country = location_country
        self.account_status = account_status


class RetailerLocationSearchModel(CommonSearchModel):

    def __init__(
        self,
        ids: list[UUID] | None = None,
        retailer_ids: list[UUID] | None = None, 
        name: str | None = None,
        name_like: str | None = None,
        account_status: RetailerLocationAccountStatuses | None = None,
        location_city: str | None = None,
        location_state: str | None = None,
        location_country: str | None = None,
    ) -> None:

        super().__init__(ids)

        self.name = name
        self.name_like = name_like
        self.retailer_ids = retailer_ids 
        self.account_status = account_status
        self.location_city = location_city
        self.location_state = location_state
        self.location_country = location_country


class RetailerLocationDatabaseModel(CommonDatabaseModel):

    def __init__(
        self,
        id: UUID,
        retailer_id: UUID,
        name: str,
        account_status: RetailerLocationAccountStatuses,
        created_at: datetime, 
        location_city: str | None = None,
        location_state: str | None = None,
        location_country: str | None = None,
        contact_email: EmailStr | None = None,
        contact_phone: DicsPhoneNumber | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)

        self.name = name
        self.retailer_id = retailer_id 
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.location_city = location_city
        self.location_state = location_state
        self.location_country = location_country
        self.account_status = account_status


class RetailerLocationModel(CommonModel):

    def __init__(
        self,
        id: UUID,
        retailer_id: UUID,
        name: str,
        account_status: RetailerLocationAccountStatuses,
        created_at: datetime, 
        retailer: RetailerModel | None = None,
        location_city: str | None = None,
        location_state: str | None = None,
        location_country: str | None = None,
        contact_email: EmailStr | None = None,
        contact_phone: DicsPhoneNumber | None = None, 
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)

        self.name = name
        self.retailer_id = retailer_id  
        self.retailer = retailer
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.location_city = location_city
        self.location_state = location_state
        self.location_country = location_country
        self.account_status = account_status


# Pydantic causes these class variables to safely be instance variables.
class RetailerLocationOutboundModel(CommonOutboundResponseModel):
    name: str
    retailer_id: UUID
    account_status: RetailerLocationAccountStatuses 
    retailer: RetailerOutboundModel | None = None
    location_city: str | None = None
    location_state: str | None = None
    location_country: str | None = None
    contact_email: EmailStr | None = None
    contact_phone: DicsPhoneNumber | None = None
    account_status: RetailerLocationAccountStatuses | None = None
