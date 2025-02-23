import datetime

from requests import Response 
from tests.qdk.qa_requests import qa_get, qa_patch, qa_post
from tests.qdk.types import PagedResponseItemList, PagingResponseModel, PagingRequestModel, RequestOperators, TestContext
from tests.qdk.utils import assert_object_was_updated, assert_objects_are_equal, copy_object_when_appropriate, generate_random_string
 
class RetailerCreateModel():  

    def __init__(self,
                name: str | None = None,
                contact_email: str | None = None,
                account_status: str | None = None,
                hq_city: str | None = None,
                hq_state: str | None = None,
                hq_country: str | None = None) -> None:
        
        self.name = name
        self.contact_email = contact_email
        self.account_status = account_status
        self.hq_city = hq_city
        self.hq_state = hq_state
        self.hq_country = hq_country 
        
class RetailerUpdateModel():  

    def __init__(self,
                name: str | None = None,
                contact_email: str | None = None,
                account_status: str | None = None,
                hq_city: str | None = None,
                hq_state: str | None = None,
                hq_country: str | None = None) -> None:
        
        self.name = name
        self.contact_email = contact_email
        self.account_status = account_status
        self.hq_city = hq_city
        self.hq_state = hq_state
        self.hq_country = hq_country 

class RetailerModel():  

    def __init__(self, 
                id: str, 
                name: str,
                created_at: datetime.datetime,
                contact_email: str | None = None, 
                account_status: str | None = None,
                hq_city: str | None = None,
                hq_state: str | None = None,
                hq_country: str | None = None,
                updated_at: datetime.datetime | None = None) -> None:
        
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.name = name
        self.contact_email = contact_email
        self.account_status = account_status
        self.hq_city = hq_city
        self.hq_state = hq_state
        self.hq_country = hq_country
        
class RetailerSearchModel(PagingRequestModel):  

    def __init__(self, 
                ids: str | None = None,  
                name: str | None = None,
                name_like: str | None = None,
                account_status: str | None = None,
                hq_city: str | None = None,
                hq_state: str | None = None,
                hq_country: str | None = None,
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
        self.name = name
        self.name_like = name_like
        self.account_status = account_status
        self.hq_city = hq_city
        self.hq_state = hq_state
        self.hq_country = hq_country
 
def mint_default_retailer(
    context: TestContext, 
    overrides: RetailerCreateModel | None = None, 
    request_operators: RequestOperators | None = None
) -> RetailerCreateModel: 
    random_string = generate_random_string()

    overrides = overrides or RetailerCreateModel()
    
    default_retailer: RetailerCreateModel = RetailerCreateModel(
        name = random_string + '_name',
        hq_city = 'cityville',
        hq_state = 'north new stateplace',
        hq_country = 'CK',
        contact_email = 'madeupemailaddress@example.com',
        account_status= 'PausedByRequest'
    )

    copy_object_when_appropriate(default_retailer, overrides)
     
    return default_retailer

def create_retailer(
        context: TestContext,
        overrides: RetailerCreateModel | None = None, 
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ) -> RetailerModel:
    
    post_object: RetailerCreateModel = mint_default_retailer(context = context, overrides = overrides, request_operators = request_operators)

    result: Response = qa_post(context.api_url + "/retailers", post_object, request_operators)

    if(allow_failures == False):
        assert result.status_code == 201
 
        result_dict = result.json()

        assert_objects_are_equal(result_dict, post_object.__dict__, ["id", "created_at", "updated_at"])

        assert result_dict['id'] is not None
        assert result_dict['created_at'] is not None
        assert result_dict['updated_at'] is None
    
    return_object = RetailerModel(**result.json())
    
    return return_object 
 
def get_retailer_by_id(
        context: TestContext, 
        id: str,
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ) -> RetailerModel:

    url: str = f"{context.api_url}/retailers/{id}"
    
    result: Response = qa_get(url)
     
    return_object = RetailerModel(**result.json())
    
    return return_object 

def get_retailers(
        context: TestContext, 
        search_model: RetailerSearchModel | None,
        request_operators: RequestOperators | None = None 
    ) -> PagedResponseItemList[RetailerModel]: 

    url: str = f"{context.api_url}/retailers"
    
    result: Response = qa_get(
        url = url, 
        query_params = search_model if search_model is not None else {},
        request_operators = request_operators
    )
    
    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict['paging'])
     
    return_items: list[RetailerModel] = [RetailerModel(**obj) for obj in result_dict['items']]

    return_object = PagedResponseItemList[RetailerModel](
        items = return_items, paging = return_paging_object
    )
    
    return return_object 

def update_retailer(
        context: TestContext,
        id: str,
        update_model: RetailerUpdateModel | None = None, 
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
    ) -> RetailerModel:
    
    original_object: RetailerModel = get_retailer_by_id(context, id, request_operators)

    result: Response = qa_patch(f"{context.api_url}/retailers/{id}", update_model, request_operators)

    if(allow_failures == False):
        assert result.status_code == 200
 
        result_dict = result.json()

        assert_object_was_updated(original_object.__dict__, update_model.__dict__, result_dict, ["updated_at"])
 
        assert result_dict['updated_at'] is not None
    
    return_object = RetailerModel(**result.json())
    
    return return_object