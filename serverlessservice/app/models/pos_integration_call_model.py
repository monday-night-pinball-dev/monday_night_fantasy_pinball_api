from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Optional
from uuid import UUID
from fastapi import Query
from pydantic import UUID4, BaseModel, BeforeValidator, Field, Json, Strict 
  
from models.common_model import (
    CommonDatabaseModel,
    CommonInboundSearchModel,
    CommonModel,
    CommonOutboundResponseModel,
    CommonSearchModel,
    validate_ids,
)
from models.pos_integration_model import PosIntegrationModel, PosIntegrationOutboundModel
from models.retailer_location_model import RetailerLocationModel, RetailerLocationOutboundModel
from models.retailer_model import RetailerModel, RetailerOutboundModel


# Pydantic causes these class variables to safely be instance variables.
class PosIntegrationCallInboundCreateModel(BaseModel): 
    pos_integration_id: Annotated[UUID4, Strict(False)] = Field(...)
    request: dict[str, Any] = Field(...)
    response: dict[str, Any]= Field(...)
    response_status_code: int = Field(...)  
    
# Pydantic causes these class variables to safely be instance variables.
class PosIntegrationCallInboundSearchModel(CommonInboundSearchModel):
    retailer_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    retailer_location_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    pos_integration_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
 
    response_status_code: Optional[int] = Query(default=None)

class PosIntegrationCallCreateModel:

    def __init__(
        self, 
        pos_integration_id: UUID, 
        request: dict[str,Any], 
        response: dict[str,Any], 
        response_status_code: int,     
        retailer_location_id: UUID | None = None,
        retailer_id: UUID | None = None
    ) -> None:

        self.pos_integration_id = pos_integration_id
        self.request = request
        self.response = response
        self.response_status_code = response_status_code  
        self.retailer_location_id = retailer_location_id
        self.retailer_id = retailer_id
  
class PosIntegrationCallSearchModel(CommonSearchModel):

    def __init__(
        self,
        ids: list[UUID] | None = None,
        retailer_ids: list[UUID] | None = None,
        retailer_location_ids: list[UUID] | None = None,
        pos_integration_ids: list[UUID] | None = None,
        response_status_code: int | None = None, 
    ) -> None:

        super().__init__(ids)

        self.retailer_ids = retailer_ids
        self.retailer_location_ids = retailer_location_ids
        self.pos_integration_ids = pos_integration_ids
        self.response_status_code = response_status_code 
 
class PosIntegrationCallDatabaseModel(CommonDatabaseModel):

    def __init__(
        self,
        id: UUID,
        retailer_id: UUID,
        retailer_location_id: UUID,
        pos_integration_id: UUID,
        request: dict[str,Any],
        response: dict[str,Any],
        response_status_code: int,
        created_at: datetime, 
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)
 
        self.retailer_id = retailer_id
        self.retailer_location_id = retailer_location_id
        self.pos_integration_id = pos_integration_id
        self.request = request
        self.response = response
        self.response_status_code = response_status_code 


class PosIntegrationCallModel(CommonModel):

    def __init__(
        self,
        id: UUID,
        retailer_id: UUID,
        retailer_location_id: UUID,
        pos_integration_id: UUID,
        request: dict[str,Any],
        response: dict[str,Any],
        response_status_code: int,
        created_at: datetime, 
        retailer: RetailerModel | None = None,
        retailer_location: RetailerLocationModel | None = None,
        pos_integration: PosIntegrationModel | None = None,
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)

        self.retailer_id = retailer_id
        self.retailer_location_id = retailer_location_id
        self.pos_integration_id = pos_integration_id
        self.request = request
        self.response = response
        self.response_status_code = response_status_code 
        
        self.retailer = retailer
        self.retailer_location = retailer_location
        self.pos_integration = pos_integration


# Pydantic causes these class variables to safely be instance variables.
class PosIntegrationCallOutboundModel(CommonOutboundResponseModel):
    retailer_id: str
    retailer: RetailerOutboundModel | None = None
    retailer_location_id: str 
    retailer_location: RetailerLocationOutboundModel | None = None
    pos_integration_id: str
    pos_integration: PosIntegrationOutboundModel | None = None
    request: dict[str,Any]
    response: dict[str,Any]
    response_status_code: int 
