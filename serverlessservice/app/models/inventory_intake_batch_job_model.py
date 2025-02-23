from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Optional
from uuid import UUID
from fastapi import Query
from pydantic import BaseModel, BeforeValidator, Field 
from enum import Enum
 
class InventoryIntakeBatchJobStatuses(str, Enum):
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
class InventoryIntakeBatchJobInboundCreateModel(BaseModel):   
    restricted_retailer_location_ids: Annotated[Optional[str | list[str]], BeforeValidator(validate_ids)] = Field(default=None)
    status: Optional[InventoryIntakeBatchJobStatuses] = Field(default=None) 
    status_details: Optional[dict[str,Any]] = Field(default=None)


# Pydantic causes these class variables to safely be instance variables.
class InventoryIntakeBatchJobInboundUpdateModel(BaseModel):
    status: Optional[InventoryIntakeBatchJobStatuses] = Field( default=None)
    status_details: Optional[dict[str,Any]] = Field(default=None)

# Pydantic causes these class variables to safely be instance variables.
class InventoryIntakeBatchJobInboundSearchModel(CommonInboundSearchModel): 
    status: Optional[InventoryIntakeBatchJobStatuses] = Query(default=None) 


class InventoryIntakeBatchJobCreateModel:

    def __init__(
        self,
        status: InventoryIntakeBatchJobStatuses | None = None,
        status_details: dict[str,Any] | None = None,
        restricted_retailer_location_ids: list[UUID] | None = None,
        
    ) -> None: 
        self.status = status
        self.status_details = status_details
        self.restricted_retailer_location_ids = restricted_retailer_location_ids


class InventoryIntakeBatchJobUpdateModel:

    def __init__(
        self,
        status: InventoryIntakeBatchJobStatuses | None = None,
        status_details: dict[str,Any] | None = None,
            
        
    ) -> None:

        self.status = status
        self.status_details = status_details
 
class InventoryIntakeBatchJobSearchModel(CommonSearchModel):

    def __init__(
        self,
        ids: list[UUID] | None = None,  
        status: InventoryIntakeBatchJobStatuses | None = None,
    ) -> None:

        super().__init__(ids)
        
        self.status = status


class InventoryIntakeBatchJobModel(CommonModel):

    def __init__(
        self,
        id: UUID,  
        status: InventoryIntakeBatchJobStatuses,
        status_details: dict[str,Any],
        created_at: datetime, 
        restricted_retailer_location_ids: list[UUID] | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)
            
        self.status = status
        self.status_details = status_details
        self.restricted_retailer_location_ids = restricted_retailer_location_ids


class InventoryIntakeBatchJobDatabaseModel(CommonDatabaseModel):

    def __init__(
        self,
        id: UUID, 
        status: InventoryIntakeBatchJobStatuses,
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
class InventoryIntakeBatchJobOutboundModel(CommonOutboundResponseModel):
    
    status: InventoryIntakeBatchJobStatuses
    
    restricted_retailer_location_ids: list[UUID] | None = None,
    status_details: dict[str,Any]
