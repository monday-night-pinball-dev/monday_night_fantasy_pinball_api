from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Optional
from uuid import UUID
from fastapi import Query
from pydantic import UUID4, BaseModel, BeforeValidator, EmailStr, Field, Strict
from pydantic_core import PydanticUndefined
from enum import Enum


class SalesIntakeBatchJobStatuses(str, Enum):
    Requested = 'Requested'
    Processing = 'Processing'
    Complete = 'Complete'
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
class SalesIntakeBatchJobInboundCreateModel(BaseModel):   
    restricted_retailer_location_ids: Annotated[Optional[str | list[str]], BeforeValidator(validate_ids)] = Field(default=None)
    status: Optional[SalesIntakeBatchJobStatuses] = Field(default=None) 
    status_details: Optional[dict[str,Any]] = Field(default=None)


# Pydantic causes these class variables to safely be instance variables.
class SalesIntakeBatchJobInboundUpdateModel(BaseModel):
    status: Optional[SalesIntakeBatchJobStatuses] = Field( default=None)
    status_details: Optional[dict[str,Any]] = Field(default=None)

# Pydantic causes these class variables to safely be instance variables.
class SalesIntakeBatchJobInboundSearchModel(CommonInboundSearchModel):  
    status: Optional[SalesIntakeBatchJobStatuses] = Query(default=None) 


class SalesIntakeBatchJobCreateModel:

    def __init__(
        self,  
        status: SalesIntakeBatchJobStatuses | None = None,
        status_details: dict[str,Any] | None = None,
        restricted_retailer_location_ids: list[UUID] | None = None,
        
    ) -> None:
        
        self.status = status
        self.status_details = status_details
        self.restricted_retailer_location_ids = restricted_retailer_location_ids


class SalesIntakeBatchJobUpdateModel:

    def __init__(
        self,
        status: SalesIntakeBatchJobStatuses | None = None,
        status_details: dict[str,Any] | None = None,
            
        
    ) -> None:

        self.status = status
        self.status_details = status_details
 
class SalesIntakeBatchJobSearchModel(CommonSearchModel):

    def __init__(
        self,
        ids: list[UUID] | None = None,  
        status: SalesIntakeBatchJobStatuses | None = None,
    ) -> None:

        super().__init__(ids)

        self.status = status


class SalesIntakeBatchJobModel(CommonModel):

    def __init__(
        self,
        id: UUID,  
        status: SalesIntakeBatchJobStatuses,
        status_details: dict[str,Any],
        created_at: datetime, 
        restricted_retailer_location_ids: list[UUID] | None = None, 
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)
 
            
        self.status = status
        self.status_details = status_details
        self.restricted_retailer_location_ids = restricted_retailer_location_ids
    


class SalesIntakeBatchJobDatabaseModel(CommonDatabaseModel):

    def __init__(
        self,
        id: UUID,  
        status: SalesIntakeBatchJobStatuses,
        status_details: dict[str,Any],
        created_at: datetime, 
        restricted_retailer_location_ids: list[UUID] | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)

  
        self.status = status
        self.status_details = status_details 
        self.restricted_retailer_location_ids = restricted_retailer_location_ids


# Pydantic causes these class variables to safely be instance variables.
class SalesIntakeBatchJobOutboundModel(CommonOutboundResponseModel):
    
    status: SalesIntakeBatchJobStatuses
    
    restricted_retailer_location_ids: list[UUID] | None = None,
    status_details: dict[str,Any]
