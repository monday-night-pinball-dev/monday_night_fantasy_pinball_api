import datetime
from typing import Any

from requests import Response 
from tests.qdk.operators.pos_integrations import PosIntegrationCreateModel, PosIntegrationModel, create_pos_integration
from tests.qdk.operators.retailer_locations import RetailerLocationModel
from tests.qdk.operators.retailers import RetailerModel
from tests.qdk.qa_requests import qa_get, qa_post
from tests.qdk.types import PagedResponseItemList, PagingResponseModel, PagingRequestModel, RequestOperators, TestContext
from tests.qdk.utils import assert_objects_are_equal, copy_object_when_appropriate, generate_random_string
 
class PosSimulatorResponseCreateModel():  

    def __init__(self,  
            response_body: dict[str, Any] | None = None,
            response_status_code: str | None = None,
            description: str | None = None,
            action_type: str | None = None,
        ) -> None:
         
        self.description = description
        self.action_type = action_type
        self.response_body = response_body
        self.response_status_code = response_status_code 
    
class PosSimulatorResponseModel():  

    def __init__(self, 
            id: str,  
            response_body: str,
            response_status_code: str, 
            action_type: str,
            created_at: datetime.datetime,
            description: str | None = None, 
            updated_at: datetime.datetime | None = None
        ) -> None:
        
        self.id = id

        self.response_body = response_body
        self.response_status_code = response_status_code
        self.action_type = action_type
 
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        
class PosSimulatorResponseSearchModel(PagingRequestModel):  

    def __init__(self, 
                ids: str | None = None,  
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
 
def mint_default_pos_simulator_response(
    context: TestContext, 
    overrides: PosSimulatorResponseCreateModel | None = None, 
    request_operators: RequestOperators | None = None
) -> PosSimulatorResponseCreateModel: 
    random_string = generate_random_string()

    overrides = overrides or PosSimulatorResponseCreateModel()
      
    default_pos_simulator_response: PosSimulatorResponseCreateModel = PosSimulatorResponseCreateModel(
 
        response_body = dict[str, Any]({
            "key1": "value1",
            "key2": "value2",
            "key3": {
                "key4": "value4",
                "key5": "value5",
            }
        }),
        description= "this is a description",
        action_type= "GetHistoricalSales",
        response_status_code = 999
    )

    copy_object_when_appropriate(default_pos_simulator_response, overrides)
     
    return default_pos_simulator_response

def create_pos_simulator_response(
        context: TestContext,
        overrides: PosSimulatorResponseCreateModel | None = None, 
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ) -> PosSimulatorResponseModel:
    
    post_object: PosSimulatorResponseCreateModel = mint_default_pos_simulator_response(context = context, overrides = overrides, request_operators = request_operators)

    result: Response = qa_post(context.api_url + "/pos_simulator_responses", post_object, request_operators)

    if(allow_failures == False):
        assert result.status_code == 201
 
        result_dict = result.json()

        assert_objects_are_equal(result_dict, post_object.__dict__, ["id", "created_at", "updated_at", "retailer_id", "retailer", "retailer_location_id", "retailer_location", "pos_integration_id", "pos_integration"])

        assert result_dict['id'] is not None
        assert result_dict['created_at'] is not None
        assert result_dict['updated_at'] is None
    
    return_object = PosSimulatorResponseModel(**result.json())
    
    return return_object 
 
def get_pos_simulator_response_by_id(
        context: TestContext, 
        id: str,
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ) -> PosSimulatorResponseModel:

    url: str = f"{context.api_url}/pos_simulator_responses/{id}"
    
    result: Response = qa_get(url, request_operators = request_operators)
     
    return_object = PosSimulatorResponseModel(**result.json())
    
    return return_object 

def get_pos_simulator_responses(
        context: TestContext, 
        search_model: PosSimulatorResponseSearchModel | None,
        request_operators: RequestOperators | None = None 
    ) -> PagedResponseItemList[PosSimulatorResponseModel]: 

    url: str = f"{context.api_url}/pos_simulator_responses"
    
    result: Response = qa_get(
        url = url, 
        query_params = search_model if search_model is not None else {},
        request_operators = request_operators
    )
    
    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict['paging'])
     
    return_items: list[PosSimulatorResponseModel] = [PosSimulatorResponseModel(**obj) for obj in result_dict['items']]

    return_object = PagedResponseItemList[PosSimulatorResponseModel](
        items = return_items, paging = return_paging_object
    )
    
    return return_object
 