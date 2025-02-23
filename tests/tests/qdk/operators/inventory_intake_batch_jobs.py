import datetime
from typing import Any

from requests import Response 
from tests.qdk.operators.retailer_locations import RetailerLocationCreateModel, RetailerLocationModel, create_retailer_location
from tests.qdk.operators.retailers import RetailerCreateModel, RetailerModel
from tests.qdk.qa_requests import qa_get, qa_patch, qa_post
from tests.qdk.types import PagedResponseItemList, PagingResponseModel, PagingRequestModel, RequestOperators, TestContext
from tests.qdk.utils import assert_object_was_updated, assert_objects_are_equal, copy_object_when_appropriate, generate_random_string
 
class InventoryIntakeBatchJobCreateModel():  

    def __init__(
        self,   
        status: str | None = None,
        restricted_retailer_location_ids: str | None = None,
        status_details: dict[str,Any] | None = None,
    ) -> None:
        self.restricted_retailer_location_ids = restricted_retailer_location_ids 
        self.status = status
        self.status_details = status_details
         
        
class InventoryIntakeBatchJobUpdateModel():  

    def __init__(
        self,  
        status: str | None = None,
        status_details: dict[str,Any] | None = None,
    ) -> None:
        
        self.status = status
        self.status_details = status_details
        
class InventoryIntakeBatchJobModel():  

    def __init__(
        self, 
        id: str,  
        status: str,
        created_at: datetime.datetime,
        restricted_retailer_location_ids : list[str] | None = None,
        retailer_location: RetailerLocationModel | None = None, 
        retailer: RetailerModel | None = None,
        status_details: dict[str,Any] | None = None, 
        updated_at: datetime.datetime | None = None
    ) -> None:

        self.id = id 
        self.restricted_retailer_location_ids = restricted_retailer_location_ids
 
        self.status = status
        self.retailer = retailer
        self.retailer_location = retailer_location
        self.status_details = status_details
        self.created_at = created_at
        self.updated_at = updated_at
        
class InventoryIntakeBatchJobSearchModel(PagingRequestModel):  

    def __init__(self, 
        ids: str | None = None,   
 
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
 
        self.status = status
 
 
def mint_default_inventory_intake_batch_job(
    context: TestContext, 
    overrides: InventoryIntakeBatchJobCreateModel | None = None, 
    request_operators: RequestOperators | None = None
) -> InventoryIntakeBatchJobCreateModel: 
    random_string = generate_random_string()

    overrides = overrides or InventoryIntakeBatchJobCreateModel()
    
    default_inventory_intake_batch_job: InventoryIntakeBatchJobCreateModel = InventoryIntakeBatchJobCreateModel(
 
        restricted_retailer_location_ids = ['00000000-0000-0000-0000-000000000000','00000000-0000-0000-0000-111111111111','00000000-0000-0000-0000-222222222222'],
        status = 'Requested',
        status_details = {
            "key": "value"
        }, 
    )

    copy_object_when_appropriate(default_inventory_intake_batch_job, overrides)
     
    return default_inventory_intake_batch_job

def create_inventory_intake_batch_job(
        context: TestContext,
        overrides: InventoryIntakeBatchJobCreateModel | None = None, 
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
    ) -> InventoryIntakeBatchJobModel:
    
    post_object: InventoryIntakeBatchJobCreateModel = mint_default_inventory_intake_batch_job(context = context, overrides = overrides, request_operators = request_operators)

    result: Response = qa_post(context.api_url + "/inventory_intake_batch_jobs", post_object, request_operators)

    if(allow_failures == False):
        assert result.status_code == 201
 
        result_dict = result.json()

        assert_objects_are_equal(result_dict, post_object.__dict__, ["id", "created_at", "updated_at", "status", "status_details"])

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
 
    return_object = InventoryIntakeBatchJobModel(**result.json())
    
    return return_object 
 
def get_inventory_intake_batch_job_by_id(
        context: TestContext, 
        id: str,
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ) -> InventoryIntakeBatchJobModel:

    url: str = f"{context.api_url}/inventory_intake_batch_jobs/{id}"
    
    result: Response = qa_get(url)
     
    return_object = InventoryIntakeBatchJobModel(**result.json())
    
    return return_object 

def get_inventory_intake_batch_jobs(
        context: TestContext, 
        search_model: InventoryIntakeBatchJobSearchModel | None,
        request_operators: RequestOperators | None = None 
    ) -> PagedResponseItemList[InventoryIntakeBatchJobModel]: 

    url: str = f"{context.api_url}/inventory_intake_batch_jobs"
    
    result: Response = qa_get(
        url = url, 
        query_params = search_model if search_model is not None else {},
        request_operators = request_operators
    )
    
    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict['paging'])
     
    return_items: list[InventoryIntakeBatchJobModel] = [InventoryIntakeBatchJobModel(**obj) for obj in result_dict['items']]

    return_object = PagedResponseItemList[InventoryIntakeBatchJobModel](
        items = return_items, paging = return_paging_object
    )
    
    return return_object 

def update_inventory_intake_batch_job(
        context: TestContext,
        id: str,
        update_model: InventoryIntakeBatchJobUpdateModel | None = None, 
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
    ) -> InventoryIntakeBatchJobModel:
    
    original_object: InventoryIntakeBatchJobModel = get_inventory_intake_batch_job_by_id(context, id, request_operators)

    result: Response = qa_patch(f"{context.api_url}/inventory_intake_batch_jobs/{id}", update_model, request_operators)

    if(allow_failures == False):
        assert result.status_code == 200
 
        result_dict = result.json()

        assert_object_was_updated(original_object.__dict__, update_model.__dict__, result_dict, ["updated_at"])
 
        assert result_dict['updated_at'] is not None
    
    return_object = InventoryIntakeBatchJobModel(**result.json())
    
    return return_object