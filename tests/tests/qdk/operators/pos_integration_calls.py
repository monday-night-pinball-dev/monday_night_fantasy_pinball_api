import datetime
from typing import Any

from requests import Response 
from tests.qdk.operators.pos_integrations import PosIntegrationCreateModel, PosIntegrationModel, create_pos_integration
from tests.qdk.operators.retailer_locations import RetailerLocationModel
from tests.qdk.operators.retailers import RetailerModel
from tests.qdk.qa_requests import qa_get, qa_post
from tests.qdk.types import PagedResponseItemList, PagingResponseModel, PagingRequestModel, RequestOperators, TestContext
from tests.qdk.utils import assert_objects_are_equal, copy_object_when_appropriate, generate_random_string
 
class PosIntegrationCallCreateModel():  

    def __init__(self, 
            pos_integration_id: str | None = None,
            pos_integration: PosIntegrationCreateModel | None = None,
            request: dict[str, Any] | None = None,
            response: dict[str, Any] | None = None,
            response_status_code: str | None = None
        ) -> None:
         
        self.pos_integration_id = pos_integration_id
        self.pos_integration = pos_integration
        self.request = request
        self.response = response
        self.response_status_code = response_status_code 
    
class PosIntegrationCallModel():  

    def __init__(self, 
            id: str, 
            retailer_id: str, 
            retailer_location_id: str, 
            pos_integration_id: str, 
            request: str,
            response: str,
            response_status_code: str, 
            created_at: datetime.datetime,
            retailer_location: RetailerLocationModel | None = None, 
            retailer: RetailerModel | None = None, 
            pos_integration: PosIntegrationModel | None = None,
            updated_at: datetime.datetime | None = None
        ) -> None:
        
        self.id = id
        self.retailer_id = retailer_id
        self.retailer = RetailerModel(**retailer) if retailer is not None else None
        self.retailer_location_id = retailer_location_id
        self.retailer_location = RetailerLocationModel(**retailer_location) if retailer_location is not None else None
        self.pos_integration_id = pos_integration_id
        self.pos_integration =  PosIntegrationModel(**pos_integration) if pos_integration is not None else None
        self.request = request
        self.response = response
        self.response_status_code = response_status_code
 
        self.created_at = created_at
        self.updated_at = updated_at
        
class PosIntegrationCallSearchModel(PagingRequestModel):  

    def __init__(self, 
                ids: str | None = None,  
                retailer_ids: str | None = None,  
                retailer_location_ids: str | None = None,  
                pos_integration_ids: str | None = None,   
                response_status_code: str | None = None, 
                page: int | None = None,
                page_length: int | None = None,
                is_sort_descending: bool | None = None,
                sort_by: str | None = None) -> None:
        super().__init__(
            page = page,
            page_length = page_length,
            is_sort_descending = is_sort_descending,
            sort_by = sort_by
        )
        
        self.ids = ids 
        self.retailer_ids = retailer_ids 
        self.retailer_location_ids = retailer_location_ids 
        self.pos_integration_ids = pos_integration_ids
        self.response_status_code = response_status_code 
 
def mint_default_pos_integration_call(
    context: TestContext, 
    overrides: PosIntegrationCallCreateModel | None = None, 
    request_operators: RequestOperators | None = None
) -> PosIntegrationCallCreateModel: 
    random_string = generate_random_string()

    overrides = overrides or PosIntegrationCallCreateModel()
    
    if(overrides.pos_integration_id is None):

        new_pos_integration = create_pos_integration(context, overrides.pos_integration, request_operators = request_operators)
        overrides.pos_integration_id = new_pos_integration.id

        del overrides.pos_integration
      
    default_pos_integration_call: PosIntegrationCallCreateModel = PosIntegrationCallCreateModel(
        request = dict[str, Any]({
            "requestProperty": "requestvalue",
            "anotherProperty": "andbelieveitornotanothervalue"
        }),
        
        response = dict[str, Any]({
            "responsibility": "what's that?",
            "jkIknowwhat it iS": "unbleievavble this guy"
        }),
        
        response_status_code = 999
    )

    copy_object_when_appropriate(default_pos_integration_call, overrides)
     
    return default_pos_integration_call

def create_pos_integration_call(
        context: TestContext,
        overrides: PosIntegrationCallCreateModel | None = None, 
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ) -> PosIntegrationCallModel:
    
    post_object: PosIntegrationCallCreateModel = mint_default_pos_integration_call(context = context, overrides = overrides, request_operators = request_operators)

    result: Response = qa_post(context.api_url + "/pos_integration_calls", post_object, request_operators)

    if(allow_failures == False):
        assert result.status_code == 201
 
        result_dict = result.json()

        assert_objects_are_equal(result_dict, post_object.__dict__, ["id", "created_at", "updated_at", "retailer_id", "retailer", "retailer_location_id", "retailer_location", "pos_integration_id", "pos_integration"])

        assert result_dict['id'] is not None
        assert result_dict['created_at'] is not None
        assert result_dict['updated_at'] is None
    
    return_object = PosIntegrationCallModel(**result.json())
    
    return return_object 
 
def get_pos_integration_call_by_id(
        context: TestContext, 
        id: str,
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ) -> PosIntegrationCallModel:

    url: str = f"{context.api_url}/pos_integration_calls/{id}"
    
    result: Response = qa_get(url, request_operators = request_operators)
     
    return_object = PosIntegrationCallModel(**result.json())
    
    return return_object 

def get_pos_integration_calls(
        context: TestContext, 
        search_model: PosIntegrationCallSearchModel | None,
        request_operators: RequestOperators | None = None 
    ) -> PagedResponseItemList[PosIntegrationCallModel]: 

    url: str = f"{context.api_url}/pos_integration_calls"
    
    result: Response = qa_get(
        url = url, 
        query_params = search_model if search_model is not None else {},
        request_operators = request_operators
    )
    
    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict['paging'])
     
    return_items: list[PosIntegrationCallModel] = [PosIntegrationCallModel(**obj) for obj in result_dict['items']]

    return_object = PagedResponseItemList[PosIntegrationCallModel](
        items = return_items, paging = return_paging_object
    )
    
    return return_object 
  
def pos_integration_call_hydration_check(pos_integration_call: PosIntegrationCallModel) -> None:
    assert pos_integration_call.retailer is not None
    assert pos_integration_call.retailer.id is not None
    assert pos_integration_call.retailer.id == pos_integration_call.retailer_id
     
    assert pos_integration_call.retailer_location is not None
    assert pos_integration_call.retailer_location.id is not None
    assert pos_integration_call.retailer_location.id == pos_integration_call.retailer_location_id
     
    assert pos_integration_call.pos_integration is not None
    assert pos_integration_call.pos_integration.id is not None
    assert pos_integration_call.pos_integration.id == pos_integration_call.pos_integration_id
     
 