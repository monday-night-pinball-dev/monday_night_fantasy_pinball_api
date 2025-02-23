from datetime import datetime
from enum import Enum
from typing import Annotated, Optional
from uuid import UUID
from fastapi import Query
from pydantic import UUID4, BaseModel, BeforeValidator, EmailStr, Field, Strict
from pydantic_core import PydanticUndefined
from enum import Enum

from models.retailer_location_model import RetailerLocationModel, RetailerLocationOutboundModel
from models.retailer_model import RetailerModel, RetailerOutboundModel


class PosPlatforms(str, Enum):
    Posabit = 'Posabit'
    Flowhub = 'Flowhub'
    Dutchie = 'Dutchie'
    KlickTrack = 'KlickTrack'
    Cova = 'Cova'
    Meadow = 'Meadow'
    GrowFlow = 'GrowFlow'
    Unknown = 'Unknown'


from models.common_model import (
    CommonDatabaseModel,
    CommonInboundSearchModel,
    CommonModel,
    CommonOutboundResponseModel,
    CommonSearchModel,
    validate_ids,
)


# Pydantic causes these class variables to safely be instance variables.
class PosIntegrationInboundCreateModel(BaseModel):
    name: str = Field(..., max_length=255) 
    retailer_location_id: Annotated[UUID4, Strict(False)] = Field(...)
    url: str = Field(...)
    key: str = Field(..., max_length=255)
    description: Optional[str] = Field(default=None)
    pos_platform: PosPlatforms = Field(...)


# Pydantic causes these class variables to safely be instance variables.
class PosIntegrationInboundUpdateModel(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255)    
    url: Optional[str] = Field(default=None)
    key: Optional[str] = Field(max_length=255, default=None)
    description: Optional[str] = Field(default=None)
    pos_platform: Optional[PosPlatforms] = Field(default=None)


# Pydantic causes these class variables to safely be instance variables.
class PosIntegrationInboundSearchModel(CommonInboundSearchModel):
    name: Optional[str] = Query(default=None)
    name_like: Optional[str] = Query(default=None)
    pos_platform: Optional[PosPlatforms] = Query(default=None)
    retailer_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    retailer_location_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 


class PosIntegrationCreateModel:

    def __init__(
        self,
        retailer_location_id: UUID,
        name: str,
        url: str,
        key: str,
        pos_platform: PosPlatforms, 
        retailer_id: UUID | None = None,
        description: str | None = None,
    ) -> None:
 
        self.retailer_location_id = retailer_location_id
        
        self.retailer_id = retailer_id
        self.name = name
        self.url = url
        self.key = key
        self.pos_platform = pos_platform
        self.description = description


class PosIntegrationUpdateModel:

    def __init__(
        self,
        name: str | None = None,
        url: str | None = None,
        key: str | None = None,
        pos_platform: str | None = None,
        description: str | None = None,
    ) -> None:

        self.name = name
        self.url = url
        self.key = key
        self.pos_platform = pos_platform
        self.description = description
 
class PosIntegrationSearchModel(CommonSearchModel):

    def __init__(
        self,
        ids: list[UUID] | None = None,
        retailer_ids: list[UUID] | None = None,
        retailer_location_ids: list[UUID] | None = None,
        name: str | None = None,
        name_like: str | None = None,
        pos_platform: PosPlatforms | None = None,
    ) -> None:

        super().__init__(ids)

        self.retailer_ids = retailer_ids
        self.retailer_location_ids = retailer_location_ids
        self.name = name
        self.name_like = name_like
        self.pos_platform = pos_platform





class PosIntegrationDatabaseModel(CommonDatabaseModel):

    def __init__(
        self,
        id: UUID,
        retailer_id: UUID,
        retailer_location_id: UUID,
        name: str,
        url: str,
        key: str,
        pos_platform: PosPlatforms,
        created_at: datetime, 
        description: str | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)

        self.retailer_id = retailer_id
        self.retailer_location_id = retailer_location_id 
        self.name = name
        self.url = url
        self.key = key
        self.pos_platform = pos_platform
        self.description = description

class PosIntegrationModel(CommonModel):

    def __init__(
        self,
        id: UUID,
        retailer_id: UUID,
        retailer_location_id: UUID,
        name: str,
        url: str,
        key: str,
        pos_platform: PosPlatforms,
        created_at: datetime,
        retailer: RetailerModel | None = None,
        retailer_location: RetailerLocationModel | None = None,
        description: str | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)

        self.retailer_id = retailer_id
        self.retailer_location_id = retailer_location_id
        self.retailer = retailer
        self.retailer_location = retailer_location
        self.name = name
        self.url = url
        self.key = key
        self.pos_platform = pos_platform
        self.description = description


# Pydantic causes these class variables to safely be instance variables.
class PosIntegrationOutboundModel(CommonOutboundResponseModel):
    retailer_id: str
    retailer_location_id: str
    name: str
    url: str
    key: str
    retailer: RetailerOutboundModel | None = None
    retailer_location: RetailerLocationOutboundModel | None = None
    pos_platform: PosPlatforms | None = None
    description: str | None = None
