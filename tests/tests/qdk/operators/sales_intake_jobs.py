import datetime
from typing import Any

from requests import Response 
from tests.qdk.operators.sales_intake_batch_jobs import SalesIntakeBatchJobCreateModel, SalesIntakeBatchJobModel, create_sales_intake_batch_job
from tests.qdk.operators.retailer_locations import RetailerLocationCreateModel, RetailerLocationModel, create_retailer_location
from tests.qdk.operators.retailers import RetailerCreateModel, RetailerModel
from tests.qdk.qa_requests import qa_get, qa_patch, qa_post
from tests.qdk.types import PagedResponseItemList, PagingResponseModel, PagingRequestModel, RequestOperators, TestContext
from tests.qdk.utils import assert_object_was_updated, assert_objects_are_equal, copy_object_when_appropriate, generate_random_string
 
class SalesIntakeJobCreateModel():  

    def __init__(
        self, 
        retailer_location_id: str | None = None,
        retailer_location: RetailerLocationCreateModel | None = None, 
        parent_batch_job_id: str | None = None,
        parent_batch_job: SalesIntakeBatchJobCreateModel | None = None,
        create_parent_batch_job_if_null: bool | None = False,
        start_time: str | None = None,
        end_time: str | None = None,
        status: str | None = None,
        status_details: dict[str,Any] | None = None,
    ) -> None:
         
        self.retailer_location_id = retailer_location_id
        self.retailer_location = retailer_location
 
        self.parent_batch_job_id = parent_batch_job_id
        self.parent_batch_job = parent_batch_job
        self.create_parent_batch_job_if_null = create_parent_batch_job_if_null
        
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.status_details = status_details
         
        
class SalesIntakeJobUpdateModel():  

    def __init__(
        self,  
        status: str | None = None,
        status_details: dict[str,Any] | None = None,
    ) -> None:
        
        self.status = status
        self.status_details = status_details
        
class SalesIntakeJobModel():  

    def __init__(
        self, 
        id: str, 
        retailer_location_id: str,
        retailer_id: str,
        parent_batch_job_id: str,
        start_time: str,
        end_time: str,
        status: str,
        created_at: datetime.datetime,
        retailer_location: RetailerLocationModel | None = None, 
        parent_batch_job: SalesIntakeBatchJobModel | None = None,
        retailer: RetailerModel | None = None,
        status_details: dict[str,Any] | None = None, 
        updated_at: datetime.datetime | None = None
    ) -> None:

        self.id = id
        self.retailer_location_id = retailer_location_id
        self.retailer_id = retailer_id
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.parent_batch_job_id = parent_batch_job_id
        self.retailer = RetailerModel(**retailer) if retailer is not None else None
        self.retailer_location = RetailerLocationModel(**retailer_location) if retailer_location is not None else None
        self.parent_batch_job = SalesIntakeBatchJobModel(**parent_batch_job) if parent_batch_job is not None else None
        self.status_details = status_details
        self.created_at = created_at
        self.updated_at = updated_at
        
class SalesIntakeJobSearchModel(PagingRequestModel):  

    def __init__(self, 
        ids: str | None = None,  
        retailer_ids: str | None = None,  
        retailer_location_ids: str | None = None,  
        parent_batch_job_ids: str | None = None, 
        status: str | None = None,
        page: int | None = None,
        page_length: int | None = None,
        is_sort_descending: bool | None = None,
        sort_by: str | None = None
    ) -> None:
    
        super().__init__(
            page = page,
            page_length = page_length,
            is_sort_descending = is_sort_descending,
            sort_by = sort_by
        )
        
        self.ids = ids 
        self.retailer_ids = retailer_ids 
        self.retailer_location_ids = retailer_location_ids 
        self.parent_batch_job_ids = parent_batch_job_ids 
             
        self.status = status
 
 
def mint_default_sales_intake_job(
    context: TestContext, 
    overrides: SalesIntakeJobCreateModel | None = None, 
    request_operators: RequestOperators | None = None
) -> SalesIntakeJobCreateModel: 
    random_string = generate_random_string()

    overrides = overrides or SalesIntakeJobCreateModel()
    
    if(overrides.retailer_location_id is None):

        new_retailer_location = create_retailer_location(context, overrides.retailer_location, request_operators = request_operators)
        overrides.retailer_location_id = new_retailer_location.id

        del overrides.retailer_location
        
            
    if(overrides.parent_batch_job_id is None and overrides.create_parent_batch_job_if_null is True):

        new_parent_batch_job = create_sales_intake_batch_job(context, overrides.parent_batch_job, request_operators = request_operators)
        overrides.parent_batch_job_id = new_parent_batch_job.id 

        del overrides.parent_batch_job
        
    default_sales_intake_job: SalesIntakeJobCreateModel = SalesIntakeJobCreateModel(
        start_time = '2024-11-01T11:11:11.111Z',
        end_time = '2024-12-02T22:22:22.222Z',
        status = 'Requested',
        status_details = {
            "key": "value"
        }, 
    )

    copy_object_when_appropriate(default_sales_intake_job, overrides)
     
    return default_sales_intake_job

def create_sales_intake_job(
        context: TestContext,
        overrides: SalesIntakeJobCreateModel | None = None, 
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
    ) -> SalesIntakeJobModel:
    
    post_object: SalesIntakeJobCreateModel = mint_default_sales_intake_job(context = context, overrides = overrides, request_operators = request_operators)

    result: Response = qa_post(context.api_url + "/sales_intake_jobs", post_object, request_operators)

    if(allow_failures == False):
        assert result.status_code == 201
 
        result_dict = result.json()

        assert_objects_are_equal(result_dict, post_object.__dict__, ["id", "created_at", "updated_at", "end_time", "retailer_id", "retailer", "retailer_location_id", "retailer_location", "parent_batch_job_id", "parent_batch_job", "status", "status_details"])

        assert result_dict['id'] is not None
        assert result_dict['created_at'] is not None
        assert result_dict['updated_at'] is None
        
        if(post_object.status is None):
            assert result_dict['status'] == 'Requested'
        else:
            assert result_dict['status'] == post_object.status
        
        if(post_object.status_details is None):
            assert result_dict['status_details'] == {}
        else:
            assert result_dict['status_details'] == post_object.status_details
             
        if(post_object.end_time is None):
            assert result_dict['end_time'] is not None
        else:
            assert result_dict['end_time'] == post_object.end_time
   
    return_object = SalesIntakeJobModel(**result.json())
    
    return return_object 
 
def get_sales_intake_job_by_id(
        context: TestContext, 
        id: str,
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ) -> SalesIntakeJobModel:

    url: str = f"{context.api_url}/sales_intake_jobs/{id}"
    
    result: Response = qa_get(url, request_operators = request_operators)
     
    return_object = SalesIntakeJobModel(**result.json())
    
    return return_object 

def get_sales_intake_jobs(
        context: TestContext, 
        search_model: SalesIntakeJobSearchModel | None,
        request_operators: RequestOperators | None = None 
    ) -> PagedResponseItemList[SalesIntakeJobModel]: 

    url: str = f"{context.api_url}/sales_intake_jobs"
    
    result: Response = qa_get(
        url = url, 
        query_params = search_model if search_model is not None else {},
        request_operators = request_operators
    )
    
    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict['paging'])
     
    return_items: list[SalesIntakeJobModel] = [SalesIntakeJobModel(**obj) for obj in result_dict['items']]

    return_object = PagedResponseItemList[SalesIntakeJobModel](
        items = return_items, paging = return_paging_object
    )
    
    return return_object 

def update_sales_intake_job(
        context: TestContext,
        id: str,
        update_model: SalesIntakeJobUpdateModel | None = None, 
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
    ) -> SalesIntakeJobModel:
    
    original_object: SalesIntakeJobModel = get_sales_intake_job_by_id(context, id, request_operators)

    result: Response = qa_patch(f"{context.api_url}/sales_intake_jobs/{id}", update_model, request_operators)

    if(allow_failures == False):
        assert result.status_code == 200
 
        result_dict = result.json()

        assert_object_was_updated(original_object.__dict__, update_model.__dict__, result_dict, ["updated_at", "parent_batch_job", "retailer", "retailer_location"])
 
        assert result_dict['updated_at'] is not None
    
    return_object = SalesIntakeJobModel(**result.json())
    
    return return_object

def sales_intake_job_hydration_check(sales_intake_job: SalesIntakeJobModel) -> None:

    assert sales_intake_job.retailer_location is not None
    assert sales_intake_job.retailer_location.id is not None
    assert sales_intake_job.retailer_location.id == sales_intake_job.retailer_location_id
    
    assert sales_intake_job.retailer is not None
    assert sales_intake_job.retailer.id is not None
    assert sales_intake_job.retailer.id == sales_intake_job.retailer_id
    
    assert sales_intake_job.parent_batch_job is not None
    assert sales_intake_job.parent_batch_job.id is not None
    assert sales_intake_job.parent_batch_job.id == sales_intake_job.parent_batch_job_id
