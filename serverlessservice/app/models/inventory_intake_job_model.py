from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Optional
from uuid import UUID
from fastapi import Query
from pydantic import UUID4, BaseModel, BeforeValidator, EmailStr, Field, Strict
from pydantic_core import PydanticUndefined
from enum import Enum

from models.pos_simulator_response_model import PosSimulatorResponseModel, PosSimulatorResponseOutboundModel
from models.retailer_location_model import RetailerLocationModel, RetailerLocationOutboundModel
from models.retailer_model import RetailerModel, RetailerOutboundModel
from models.sales_intake_batch_job_model import SalesIntakeBatchJobModel, SalesIntakeBatchJobOutboundModel


class InventoryIntakeJobStatuses(str, Enum):
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
class InventoryIntakeJobInboundCreateModel(BaseModel):  
    retailer_location_id: Annotated[UUID4, Strict(False)] = Field(...)
    parent_batch_job_id: Annotated[Optional[UUID4], Strict(False)] = Field(default=None)
    simulator_response_id: Annotated[Optional[UUID4], Strict(False)] = Field(default=None)
    snapshot_hour: datetime = Field(...)  
    status: Optional[InventoryIntakeJobStatuses] = Field(default=None)
    status_details: Optional[dict[str,Any]] = Field(default=None)


# Pydantic causes these class variables to safely be instance variables.
class InventoryIntakeJobInboundUpdateModel(BaseModel):
    status: Optional[InventoryIntakeJobStatuses] = Field( default=None)
    status_details: Optional[dict[str,Any]] = Field(default=None)



# Pydantic causes these class variables to safely be instance variables.
class InventoryIntakeJobInboundSearchModel(CommonInboundSearchModel): 
    snapshot_hour_min: Optional[datetime] = Query(default=None)
    snapshot_hour_max: Optional[datetime] = Query(default=None)
    status: Optional[InventoryIntakeJobStatuses] = Query(default=None)
    retailer_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    retailer_location_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    parent_batch_job_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 


class InventoryIntakeJobCreateModel:

    def __init__(
        self,
        retailer_location_id: UUID , 
        snapshot_hour: datetime,
        retailer_id: UUID | None = None,
        parent_batch_job_id: UUID | None = None,
        simulator_response_id: UUID | None = None,
        status: InventoryIntakeJobStatuses | None = None,
        status_details: dict[str,Any] | None = None,
        
    ) -> None:
 
        self.retailer_location_id = retailer_location_id
        self.parent_batch_job_id = parent_batch_job_id
        self.simulator_response_id = simulator_response_id
        self.retailer_id = retailer_id
        self.snapshot_hour = snapshot_hour
        self.status = status
        self.status_details = status_details


class InventoryIntakeJobUpdateModel:

    def __init__(
        self,
        status: InventoryIntakeJobStatuses | None = None,
        status_details: dict[str,Any] | None = None,
            
        
    ) -> None:

        self.status = status
        self.status_details = status_details
 
class InventoryIntakeJobSearchModel(CommonSearchModel):

    def __init__(
        self,
        ids: list[UUID] | None = None,
        retailer_ids: list[UUID] | None = None,
        retailer_location_ids: list[UUID] | None = None,
        parent_batch_job_ids: list[UUID] | None = None,
        snapshot_hour_min: datetime | None = None,
        snapshot_hour_max: datetime | None = None,
        status: InventoryIntakeJobStatuses | None = None,
    ) -> None:

        super().__init__(ids)

        self.retailer_ids = retailer_ids
        self.retailer_location_ids = retailer_location_ids
        self.parent_batch_job_ids = parent_batch_job_ids
        self.snapshot_hour_min = snapshot_hour_min
        self.snapshot_hour_max = snapshot_hour_max
        self.status = status


class InventoryIntakeJobDatabaseModel(CommonDatabaseModel):

    def __init__(
        self,
        id: UUID,
        retailer_id: UUID,
        retailer_location_id: UUID,
        snapshot_hour: datetime,
        status: InventoryIntakeJobStatuses,
        status_details: dict[str,Any],
        created_at: datetime, 
        parent_batch_job_id: UUID | None = None,
        simulator_response_id: UUID | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)

        self.retailer_id = retailer_id
        self.retailer_location_id = retailer_location_id
        self.parent_batch_job_id = parent_batch_job_id
        self.snapshot_hour = snapshot_hour
        self.status = status 
        self.simulator_response_id = simulator_response_id
        self.status_details = status_details 

class InventoryIntakeJobModel(CommonModel):

    def __init__(
        self,
        id: UUID,
        retailer_id: UUID,
        retailer_location_id: UUID,
        snapshot_hour: datetime,
        status: InventoryIntakeJobStatuses,
        status_details: dict[str,Any], 
        created_at: datetime, 
        simulator_response_id: UUID | None = None,
        simulator_response: PosSimulatorResponseModel | None = None,
        parent_batch_job_id: UUID | None = None,
        parent_batch_job: SalesIntakeBatchJobModel | None = None,
        retailer: RetailerModel | None = None,
        retailer_location: RetailerLocationModel | None = None,
        updated_at: datetime | None = None,
        
    ):

        super().__init__(id, created_at, updated_at)

        self.retailer_id = retailer_id
        self.retailer_location_id = retailer_location_id        
        self.parent_batch_job_id = parent_batch_job_id        
        self.snapshot_hour = snapshot_hour
        self.status = status
        
        self.status_details = status_details
        self.simulator_response_id = simulator_response_id
        self.parent_batch_job = parent_batch_job
        self.retailer = retailer
        self.retailer_location = retailer_location
        self.simulator_response = simulator_response


# Pydantic causes these class variables to safely be instance variables.
class InventoryIntakeJobOutboundModel(CommonOutboundResponseModel):
    retailer_id: UUID   
    retailer_location_id: UUID
    parent_batch_job_id: UUID | None = None
    retailer: RetailerOutboundModel | None = None,
    retailer_location: RetailerLocationOutboundModel | None = None,
    parent_batch_job: SalesIntakeBatchJobOutboundModel | None = None,
    simulator_response: PosSimulatorResponseOutboundModel | None = None,
    simulator_response_id: UUID | None = None,
    snapshot_hour: str
    status: InventoryIntakeJobStatuses 
    status_details: dict[str,Any] 
