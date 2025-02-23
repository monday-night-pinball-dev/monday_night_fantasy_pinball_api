from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from fastapi import Query
from pydantic import BaseModel, EmailStr, Field
from pydantic_core import PydanticUndefined

from models.common_model import (
    CommonDatabaseModel,
    CommonInboundSearchModel,
    CommonModel,
    CommonOutboundResponseModel,
    CommonSearchModel,
)

class RetailerAccountStatuses(Enum):
    Unregistered = 'Unregistered'
    RegisteredInactive = 'RegisteredInactive' 
    RegisteredActive = 'RegisteredActive' 
    PausedByRequest = 'PausedByRequest' 
    PausedByBilling = 'PausedByBilling' 
    Deactivated = 'Deactivated'
    
# Pydantic causes these class variables to safely be instance variables.
class RetailerInboundCreateModel(BaseModel):
    name: str = Field(..., max_length=255)
    contact_email: Optional[EmailStr] = Field(default=None, max_length=320)
    hq_city: Optional[str] = Field(default=None, max_length=255)
    hq_state: Optional[str] = Field(default=None, max_length=255)
    hq_country: Optional[str] = Field(default=None, max_length=2, min_length=2)
    account_status: Optional[RetailerAccountStatuses] = Field(default = None)


# Pydantic causes these class variables to safely be instance variables.
class RetailerInboundUpdateModel(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255)
    contact_email: Optional[EmailStr] = Field(default=None, max_length=320)
    hq_city: Optional[str] = Field(default=None, max_length=255)
    hq_state: Optional[str] = Field(default=None, max_length=255)
    hq_country: Optional[str] = Field(default=None, max_length=2, min_length=2)
    account_status: Optional[RetailerAccountStatuses] = Field(default = None)


# Pydantic causes these class variables to safely be instance variables.
class RetailerInboundSearchModel(CommonInboundSearchModel):
    name: Optional[str] = Query(default=None)
    name_like: Optional[str] = Query(default=None)
    account_status: Optional[RetailerAccountStatuses] = Query(default=None)
    hq_city: Optional[str] = Query(default=None)
    hq_state: Optional[str] = Query(default=None)
    hq_country: Optional[str] = Query(default=None)
 
class RetailerCreateModel:

    def __init__(
        self,
        name: str,
        contact_email: EmailStr | None = None,
        hq_city: str | None = None,
        hq_state: str | None = None,
        hq_country: str | None = None,
        account_status: RetailerAccountStatuses | None = None
    ) -> None:

        self.name = name
        self.contact_email = contact_email
        self.hq_city = hq_city
        self.hq_state = hq_state
        self.hq_country = hq_country
        self.account_status = account_status


class RetailerUpdateModel:

    def __init__(
        self,
        name: str | None = None,
        contact_email: EmailStr | None = None,
        hq_city: str | None = None,
        hq_state: str | None = None,
        hq_country: str | None = None,
        account_status: RetailerAccountStatuses | None = None,
    ) -> None:

        self.name = name
        self.contact_email = contact_email
        self.hq_city = hq_city
        self.hq_state = hq_state
        self.hq_country = hq_country
        self.account_status = account_status


class RetailerSearchModel(CommonSearchModel):

    def __init__(
        self,
        ids: list[UUID] | None = None,
        name: str | None = None,
        name_like: str | None = None,
        account_status: str | None = None,
        hq_city: str | None = None,
        hq_state: str | None = None,
        hq_country: str | None = None,
    ) -> None:

        super().__init__(ids)

        self.name = name
        self.name_like = name_like
        self.account_status = account_status
        self.hq_city = hq_city
        self.hq_state = hq_state
        self.hq_country = hq_country


class RetailerDatabaseModel(CommonDatabaseModel):

    def __init__(
        self,
        id: UUID,
        name: str,
        created_at: datetime,
        account_status: RetailerAccountStatuses | None = None,
        hq_city: str | None = None,
        hq_state: str | None = None,
        hq_country: str | None = None,
        contact_email: EmailStr | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)

        self.name = name
        self.account_status = account_status
        self.contact_email = contact_email
        self.hq_city = hq_city
        self.hq_state = hq_state
        self.hq_country = hq_country


class RetailerModel(CommonModel):

    def __init__(
        self,
        id: UUID,
        name: str,
        created_at: datetime,
        hq_city: str | None = None,
        hq_state: str | None = None,
        hq_country: str | None = None,
        contact_email: EmailStr | None = None,
        account_status: RetailerAccountStatuses | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)

        self.name = name
        self.contact_email = contact_email
        self.hq_city = hq_city
        self.hq_state = hq_state
        self.hq_country = hq_country
        self.account_status = account_status


# Pydantic causes these class variables to safely be instance variables.
class RetailerOutboundModel(CommonOutboundResponseModel):
    name: str
    contact_email: EmailStr | None = None
    hq_city: str | None = None
    hq_state: str | None = None
    hq_country: str | None = None
    account_status: RetailerAccountStatuses | None = None
