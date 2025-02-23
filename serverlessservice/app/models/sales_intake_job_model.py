from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Optional
from uuid import UUID
from fastapi import Query
from pydantic import UUID4, BaseModel, BeforeValidator, EmailStr, Field, Strict
from pydantic_core import PydanticUndefined
from enum import Enum

from models.retailer_location_model import RetailerLocationModel, RetailerLocationOutboundModel
from models.retailer_model import RetailerModel, RetailerOutboundModel
from models.sales_intake_batch_job_model import SalesIntakeBatchJobModel, SalesIntakeBatchJobOutboundModel
 
class SalesIntakeJobStatuses(str, Enum):
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
class SalesIntakeJobInboundCreateModel(BaseModel):  
    retailer_location_id: Annotated[UUID4, Strict(False)] = Field(...)
    parent_batch_job_id: Annotated[Optional[UUID4], Strict(False)] = Field(default=None) 
    simulator_response_id: Annotated[Optional[UUID4], Strict(False)] = Field(default=None)
    status: Optional[SalesIntakeJobStatuses] = Field(default=None)
    status_details: Optional[dict[str,Any]] = Field(default=None)
    start_time: Optional[datetime] = Field(default=None)
    end_time: Optional[datetime] = Field(default=None)


# Pydantic causes these class variables to safely be instance variables.
class SalesIntakeJobInboundUpdateModel(BaseModel):
    status: Optional[SalesIntakeJobStatuses] = Field( default=None)
    status_details: Optional[dict[str,Any]] = Field(default=None)



# Pydantic causes these class variables to safely be instance variables.
class SalesIntakeJobInboundSearchModel(CommonInboundSearchModel):  
    status: Optional[SalesIntakeJobStatuses] = Query(default=None)
    retailer_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    retailer_location_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    parent_batch_job_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 


class SalesIntakeJobCreateModel:

    def __init__(
        self,
        retailer_location_id: UUID , 
        start_time: datetime,
        end_time: datetime | None = None,
        retailer_id: UUID | None = None,
        parent_batch_job_id: UUID | None = None,
        status: SalesIntakeJobStatuses | None = None,
        status_details: dict[str,Any] | None = None,
        simulator_response_id: UUID | None = None,
        
    ) -> None:
 
        self.retailer_location_id = retailer_location_id
        self.parent_batch_job_id = parent_batch_job_id
        self.retailer_id = retailer_id
        self.start_time = start_time
        self.status = status
        self.status_details = status_details
        self.end_time = end_time
        self.simulator_response_id = simulator_response_id


class SalesIntakeJobUpdateModel:

    def __init__(
        self,
        status: SalesIntakeJobStatuses | None = None,
        status_details: dict[str,Any] | None = None,
            
        
    ) -> None:

        self.status = status
        self.status_details = status_details
 
class SalesIntakeJobSearchModel(CommonSearchModel):

    def __init__(
        self,
        ids: list[UUID] | None = None,
        retailer_ids: list[UUID] | None = None,
        retailer_location_ids: list[UUID] | None = None,
        parent_batch_job_ids: list[UUID] | None = None,
        snapshot_hour_min: datetime | None = None,
        snapshot_hour_max: datetime | None = None,
        status: SalesIntakeJobStatuses | None = None,
    ) -> None:

        super().__init__(ids)

        self.retailer_ids = retailer_ids
        self.retailer_location_ids = retailer_location_ids
        self.parent_batch_job_ids = parent_batch_job_ids
        self.snapshot_hour_min = snapshot_hour_min
        self.snapshot_hour_max = snapshot_hour_max
        self.status = status


class SalesIntakeJobDatabaseModel(CommonDatabaseModel):

    def __init__(
        self,
        id: UUID,
        retailer_id: UUID,
        retailer_location_id: UUID, 
        status: SalesIntakeJobStatuses,
        status_details: dict[str,Any],
        start_time: datetime,
        end_time: datetime,
        created_at: datetime, 
        parent_batch_job_id: UUID | None = None, 
        simulator_response_id: UUID | None = None,
        updated_at: datetime | None = None,
        
        
    ):

        super().__init__(id, created_at, updated_at)

        self.retailer_id = retailer_id
        self.retailer_location_id = retailer_location_id
        self.parent_batch_job_id = parent_batch_job_id 
        self.status = status
        self.simulator_response_id = simulator_response_id
        self.status_details = status_details
        self.start_time = start_time
        self.end_time = end_time


class SalesIntakeJobModel(CommonModel):

    def __init__(
        self,
        id: UUID,
        retailer_id: UUID,
        retailer_location_id: UUID,
        start_time: datetime,
        end_time: datetime,
        status: SalesIntakeJobStatuses,
        status_details: dict[str,Any], 
        created_at: datetime, 
        parent_batch_job_id: UUID | None = None,
        retailer: RetailerModel | None = None,
        retailer_location: RetailerLocationModel | None = None,
        parent_batch_job: SalesIntakeBatchJobModel | None = None,
        simulator_response_id: UUID | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)

        self.retailer_id = retailer_id
        self.retailer_location_id = retailer_location_id        
        self.parent_batch_job_id = parent_batch_job_id        
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.status_details = status_details
        self.simulator_response_id = simulator_response_id
         
        self.retailer = retailer
        self.retailer_location = retailer_location
        self.parent_batch_job = parent_batch_job


# Pydantic causes these class variables to safely be instance variables.
class SalesIntakeJobOutboundModel(CommonOutboundResponseModel):
    retailer_id: UUID   
    retailer_location_id: UUID
    parent_batch_job_id: UUID | None = None
    simulator_response_id: UUID | None = None
    start_time: str
    end_time: str
    status: SalesIntakeJobStatuses 
    status_details: dict[str,Any] 
    retailer: RetailerOutboundModel | None = None
    retailer_location: RetailerLocationOutboundModel | None = None
    parent_batch_job: SalesIntakeBatchJobOutboundModel | None = None