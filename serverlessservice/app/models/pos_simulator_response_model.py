from datetime import datetime 
from typing import Any, Optional
from uuid import UUID 
from pydantic import BaseModel, Field 
from enum import Enum
  
from models.common_model import (
    CommonDatabaseModel,
    CommonInboundSearchModel,
    CommonModel,
    CommonOutboundResponseModel,
    CommonSearchModel
) 

class PosSimulatorActionTypes(str, Enum):
    GetHistoricalSales = 'GetHistoricalSales'
    GetInventorySnapshots = 'GetInventorySnapshots'
 
# Pydantic causes these class variables to safely be instance variables.
class PosSimulatorResponseInboundCreateModel(BaseModel):   

    response_status_code: int = Field(...) 
    action_type: PosSimulatorActionTypes = Field(...)
    response_body: dict[str, Any]= Field(...)
    description: Optional[str] = Field(default=None)
     
# Pydantic causes these class variables to safely be instance variables.
class PosSimulatorResponseInboundSearchModel(CommonInboundSearchModel):
    pass
     
class PosSimulatorResponseCreateModel:
 
    def __init__(
        self,
         response_status_code: int | None = None,
         action_type: PosSimulatorActionTypes | None = None,
         response_body: dict[str, Any] | None = None,
         description: str | None = None,
    ) -> None:
     
        self.response_status_code = response_status_code
        self.action_type = action_type
        self.response_body = response_body
        self.description = description
     
class PosSimulatorResponseSearchModel(CommonSearchModel): 
 
    
    def __init__(
        self,
        ids: list[UUID] | None = None
    ) -> None:

        super().__init__(ids) 

class PosSimulatorResponseDatabaseModel(CommonDatabaseModel):

    def __init__(
        self,
        id: UUID,
        response_status_code: int,
        action_type: PosSimulatorActionTypes,
        response_body: dict[str, Any], 
        created_at: datetime,  
        description: str | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)
 
        self.response_status_code = response_status_code
        self.action_type = action_type
        self.response_body = response_body
        self.description = description
         
class PosSimulatorResponseModel(CommonModel):
  
    def __init__(
        self,
        id: UUID, 
        response_status_code: int,
        action_type: PosSimulatorActionTypes,
        response_body: dict[str, Any],
        created_at: datetime,  
        description: str | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)
        
        self.response_status_code = response_status_code
        self.action_type = action_type
        self.response_body = response_body
        
        self.description = description
    
        
# Pydantic causes these class variables to safely be instance variables.
class PosSimulatorResponseOutboundModel(CommonOutboundResponseModel):

    response_status_code: int
    action_type: PosSimulatorActionTypes
    response_body: dict[str, Any]
    description: str | None = None
 
    
    
