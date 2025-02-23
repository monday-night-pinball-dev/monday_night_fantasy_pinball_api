from datetime import datetime 
from typing import Annotated, Optional
from uuid import UUID
from fastapi import Query
from pydantic import UUID4, BaseModel, BeforeValidator, Field, Strict  

from models.common_model import (
    CommonDatabaseModel,
    CommonInboundSearchModel,
    CommonModel,
    CommonOutboundResponseModel,
    CommonSearchModel,
    validate_ids,
)

from models.retailer_location_model import RetailerLocationModel, RetailerLocationOutboundModel
from models.sales_intake_job_model import SalesIntakeJobModel, SalesIntakeJobOutboundModel
from models.retailer_model import RetailerModel, RetailerOutboundModel 

# Pydantic causes these class variables to safely be instance variables.
class HistoricalSaleInboundCreateModel(BaseModel):  
    retailer_location_id: Annotated[UUID4, Strict(False)] = Field(...) 
    sales_intake_job_id: Optional[Annotated[UUID4, Strict(False)]] = Field(default=None)
    pos_sale_id: str = Field(..., max_length=255)
    
    sale_timestamp: datetime = Field(...)    
    sub_total: Optional[int] = Field(default=None)
    discount: Optional[int] = Field(default=None)
    tax: Optional[int] = Field( default=None)
    total: int = Field(...)
    cost: Optional[int] = Field( default=None)
    
  

# Pydantic causes these class variables to safely be instance variables.
class HistoricalSaleInboundSearchModel(CommonInboundSearchModel): 
    pos_sale_ids: Optional[str] = Query(default=None)
    sales_intake_job_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None)
    retailer_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    retailer_location_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(default=None) 
    sale_timestamp_min:  Optional[datetime] = Query(default=None) 
    sale_timestamp_max: Optional[datetime] = Query(default=None) 

class HistoricalSaleCreateModel:

    def __init__(
        self,
        retailer_location_id: UUID,
        sale_timestamp: datetime ,
        pos_sale_id: str ,  
        total: int,
        sub_total: int | None = None,
        discount: int | None = None,
        tax: int | None = None,
        cost : int | None = None,
        retailer_id: UUID | None = None, 
        sales_intake_job_id: UUID | None = None, 
    ) -> None:
    
        self.retailer_location_id = retailer_location_id
        self.sales_intake_job_id = sales_intake_job_id
        self.pos_sale_id = pos_sale_id
        self.total = total
        self.sub_total = sub_total
        self.discount = discount
        self.tax = tax
        self.cost = cost
        self.retailer_id = retailer_id 
        self.sale_timestamp = sale_timestamp 
    
  
class HistoricalSaleSearchModel(CommonSearchModel):
   
    def __init__(
        self,
        ids: list[UUID] | None = None,
        retailer_ids: list[UUID] | None = None,
        retailer_location_ids: list[UUID] | None = None,
        sales_intake_job_ids: list[UUID] | None = None, 
        pos_sale_ids: list[str] | None = None,
        sale_timestamp_min: datetime | None = None,
        sale_timestamp_max: datetime | None = None 
    ) -> None:

        super().__init__(ids)

        self.retailer_ids = retailer_ids
        self.retailer_location_ids = retailer_location_ids
        self.sales_intake_job_ids = sales_intake_job_ids 
        self.pos_sale_ids = pos_sale_ids
        self.sale_timestamp_min = sale_timestamp_min
        self.sale_timestamp_max = sale_timestamp_max

 
class HistoricalSaleDatabaseModel(CommonDatabaseModel):

    def __init__(
        self,
        id: UUID,
        retailer_id: UUID,
        retailer_location_id: UUID,
        pos_sale_id: str,
        sale_timestamp: datetime,
        total: int,
        created_at: datetime, 
        sub_total: int | None = None,
        discount: int | None = None,
        tax: int | None = None,
        cost : int | None = None,
        
        sales_intake_job_id: UUID | None = None,  
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)
 
        self.retailer_location_id = retailer_location_id 
        self.retailer_id = retailer_id
        self.sales_intake_job_id = sales_intake_job_id
        self.pos_sale_id = pos_sale_id
        self.sale_timestamp = sale_timestamp
        self.total = total
        self.sub_total = sub_total
        self.discount = discount
        self.tax = tax
        self.cost = cost
          
class HistoricalSaleModel(CommonModel):

    def __init__(
        self,
        id: UUID,
        retailer_id: UUID,
        retailer_location_id: UUID,
        pos_sale_id: str,
        sale_timestamp: datetime,
        total: int,
        created_at: datetime, 
        sub_total: int | None = None,
        discount: int | None = None,
        tax: int | None = None,
        cost : int | None = None, 
        retailer: RetailerModel | None = None,
        retailer_location: RetailerLocationModel | None = None, 
        sales_intake_job: SalesIntakeJobModel | None = None,
        sales_intake_job_id: UUID | None = None,  
        updated_at: datetime | None = None,
    ):

        super().__init__(id, created_at, updated_at)
        
        self.retailer_location_id = retailer_location_id
        self.retailer_id = retailer_id
        self.pos_sale_id = pos_sale_id
        self.sale_timestamp = sale_timestamp
        self.total = total
        self.sub_total = sub_total
        self.discount = discount
        self.tax = tax
        self.cost = cost
        self.sales_intake_job_id = sales_intake_job_id

        self.retailer = retailer
        self.retailer_location = retailer_location
        self.sales_intake_job = sales_intake_job
        
        
# Pydantic causes these class variables to safely be instance variables.
class HistoricalSaleOutboundModel(CommonOutboundResponseModel):
     
    retailer_id: UUID
    retailer_location_id: UUID 
    pos_sale_id: str
    sale_timestamp: str
    total: int
    sub_total: int | None = None
    discount: int | None = None
    tax: int | None = None
    cost : int | None = None  
    sales_intake_job_id: UUID | None = None    
    retailer: RetailerOutboundModel | None = None,
    retailer_location: RetailerLocationOutboundModel | None = None, 
    sales_intake_job: SalesIntakeJobOutboundModel | None = None,
