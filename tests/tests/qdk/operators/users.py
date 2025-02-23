import datetime
from typing import Any, Self

from requests import Response 
from tests.qdk.operators.retailer_locations import RetailerLocationCreateModel, RetailerLocationModel, create_retailer_location
from tests.qdk.operators.retailers import RetailerCreateModel, RetailerModel, create_retailer
from tests.qdk.operators.vendors import VendorCreateModel, VendorModel, create_vendor
from tests.qdk.qa_requests import qa_get, qa_patch, qa_post
from tests.qdk.types import PagedResponseItemList, PagingResponseModel, PagingRequestModel, RequestOperators, TestContext
from tests.qdk.utils import assert_object_was_updated, assert_objects_are_equal, copy_object_when_appropriate, generate_random_string
 
class UserCreateModel():  

    def __init__(self, 
                retailer_location_id: str | None = None,
                retailer_location: RetailerLocationCreateModel | None = None, 
                create_retailer_location_if_null: bool | None = False, 
                vendor_id: str | None = None,
                vendor: VendorCreateModel | None = None, 
                create_vendor_if_null: bool | None = False, 
                first_name: str | None = None,
                last_name: str | None = None,
                username: str | None = None,
                role: str | None = None) -> None: 
        
        self.retailer_location_id = retailer_location_id 
        self.retailer_location = retailer_location 
        self.create_retailer_location_if_null = create_retailer_location_if_null 
        self.vendor_id = vendor_id 
        self.vendor = vendor 
        self.create_vendor_if_null = create_vendor_if_null
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.role = role 
        
class UserUpdateModel():  

    def __init__(self,
                first_name: str | None = None,
                last_name: str | None = None,
                role: str | None = None) -> None:
        
        self.first_name = first_name
        self.last_name = last_name
        self.role = role 

class UserModel():  

    def __init__(self, 
                id: str, 
                first_name: str, 
                last_name: str, 
                full_name: str, 
                username: str, 
                role: str, 
                created_at: datetime.datetime,
                vendor_id: str | None = None, 
                vendor: VendorModel | None = None, 
                retailer_id: str | None = None, 
                retailer: RetailerModel | None = None, 
                retailer_location_id: str | None = None, 
                retailer_location: RetailerLocationModel | None = None, 
                updated_at: datetime.datetime | None = None) -> None:
        
        self.id = id 
        self.first_name = first_name 
        self.last_name = last_name 
        self.full_name = full_name 
        self.username = username  
        self.role = role  
        self.vendor_id = vendor_id
        self.vendor = vendor
        self.retailer_id = retailer_id
        self.retailer = retailer
        self.retailer_location_id = retailer_location_id
        self.retailer_location = retailer_location
 
        self.created_at = created_at
        self.updated_at = updated_at
 
        
class UserSearchModel(PagingRequestModel):  

    def __init__(self, 
                ids: str | None = None,  
                retailer_ids: str | None = None,  
                vendor_ids: str | None = None,  
                retailer_location_ids: str | None = None,
                name_like: str | None = None,
                username_like: str | None = None,
                username: str | None = None,
                role: str | None = None, 
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
        self.vendor_ids = vendor_ids
        self.retailer_location_ids = retailer_location_ids
        self.role = role
        self.name_like = name_like
        self.username_like = username_like
        self.username = username
 
def mint_default_user(
    context: TestContext, 
    overrides: UserCreateModel | None = None, 
    request_operators: RequestOperators | None = None
) -> UserCreateModel: 
    random_string = generate_random_string()

    overrides = overrides or UserCreateModel()
     
    if(overrides.retailer_location_id is None and overrides.create_retailer_location_if_null):

        new_retailer_location = create_retailer_location(context, overrides.retailer_location, request_operators = request_operators)
        overrides.retailer_location_id = new_retailer_location.id

        del overrides.retailer_location
        del overrides.create_retailer_location_if_null
        
    if(overrides.vendor is None and overrides.create_vendor_if_null):

        new_vendor = create_vendor(context, overrides.vendor, request_operators = request_operators)
        overrides.vendor_id = new_vendor.id

        del overrides.vendor
        del overrides.create_vendor_if_null
  
    default_user: UserCreateModel = UserCreateModel(
        first_name = random_string + '_first_name',
        last_name = random_string + '_last_name',
        username = random_string + '_username@example.com',
        role = 'SamsonUser', 
    )
        
    copy_object_when_appropriate(default_user, overrides)
     
    return default_user

def create_user(
        context: TestContext,
        overrides: UserCreateModel | None = None, 
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ) -> UserModel:
    
    post_object: UserCreateModel = mint_default_user(context = context, overrides = overrides, request_operators = request_operators)

    result: Response = qa_post(context.api_url + "/users", post_object, request_operators)

    if(allow_failures == False):
        assert result.status_code == 201
 
        result_dict = result.json()

        assert_objects_are_equal(result_dict, post_object.__dict__, ["id", "created_at", "updated_at", "username", "retailer_id", "retailer", "retailer_location_id", "retailer_location", "vendor_id", "vendor", "full_name"])

        assert result_dict['id'] is not None
        assert result_dict['created_at'] is not None
        assert result_dict['updated_at'] is None
         
        assert result_dict['full_name'] == post_object.first_name + " " + post_object.last_name
        assert result_dict['username'].lower() == post_object.username.lower()
    
    return_object = UserModel(**result.json())
    
    return return_object 
 
def get_user_by_id(
        context: TestContext, 
        id: str,
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ) -> UserModel:

    url: str = f"{context.api_url}/users/{id}"
    
    result: Response = qa_get(url)
     
    return_object = UserModel(**result.json())
    
    return return_object 

def get_users(
        context: TestContext, 
        search_model: UserSearchModel | None,
        request_operators: RequestOperators | None = None 
    ) -> PagedResponseItemList[UserModel]: 

    url: str = f"{context.api_url}/users"
    
    result: Response = qa_get(
        url = url, 
        query_params = search_model if search_model is not None else {},
        request_operators = request_operators
    )
    
    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict['paging'])
     
    return_items: list[UserModel] = [UserModel(**obj) for obj in result_dict['items']]

    return_object = PagedResponseItemList[UserModel](
        items = return_items, paging = return_paging_object
    )
    
    return return_object 

def update_user(
        context: TestContext,
        id: str,
        update_model: UserUpdateModel | None = None, 
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
    ) -> UserModel:
    
    original_object: UserModel = get_user_by_id(context, id, request_operators)

    result: Response = qa_patch(f"{context.api_url}/users/{id}", update_model, request_operators)

    if(allow_failures == False):
        assert result.status_code == 200
 
        result_dict = result.json()

        assert_object_was_updated(original_object.__dict__, update_model.__dict__, result_dict, ["full_name", "updated_at"])
        
        assert result_dict['full_name'] == update_model.first_name + " " + update_model.last_name 
        assert result_dict['updated_at'] is not None
    
    return_object = UserModel(**result.json())
    
    return return_object