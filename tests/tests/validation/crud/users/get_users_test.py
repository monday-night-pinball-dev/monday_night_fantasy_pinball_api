from time import sleep
from typing import Any

from tests.qdk.operators.users import UserCreateModel, UserModel, UserSearchModel, create_user, get_user_by_id, get_users
from tests.qdk.qa_requests import qa_get, qa_post
from tests.qdk.types import PagedResponseItemList, TestContext
from tests.qdk.utils import assert_objects_are_equal, generate_random_string
from urllib.parse import urlencode   
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_gets_user_by_id() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object = create_user(context)

    result = get_user_by_id(context, posted_object.id)

    assert result is not None
    assert result.id == posted_object.id

def test_gets_users_invalid_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)
     
    result = qa_get(f"{context.api_url}/users", query_params={
        'ids': 'not an id,also not an id',
        'page' : 'not a page num',
        'page_length' : 'not a length num',
        'is_sort_descending' : 'not a bool'
    })

    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 4
    
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'ids' in error['loc']]

    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: not an id,\n\t1: also not an id\n].'

    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'page' in error['loc']]

    assert len(error) == 1
    assert error[0]['type'] == 'int_parsing'
    assert error[0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'
 
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'page_length' in error['loc']]

    assert len(error) == 1
    assert error[0]['type'] == 'int_parsing'
    assert error[0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'

    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'is_sort_descending' in error['loc']]

    assert len(error) == 1
    assert error[0]['type'] == 'bool_parsing'
    assert error[0]['msg'] == 'Input should be a valid boolean, unable to interpret input'

def test_gets_users_with_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: UserModel = create_user(context)
    posted_object_2: UserModel = create_user(context)
    posted_object_3: UserModel = create_user(context)
    posted_object_4: UserModel = create_user(context)

    filters: UserSearchModel = UserSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )
    
    result: PagedResponseItemList[UserModel] = get_users(context, filters)

    assert result is not None
    assert result.items is not None
    
    assert result.paging is not None
    assert result.paging.page == 1
    assert result.paging.page_length == 25
    assert result.paging.sort_by == 'created_at'
    assert result.paging.is_sort_descending == False

    assert len(result.items) == 4 
    
    posted_item_1: list[UserModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1)

    posted_item_2: list[UserModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2)
  
    posted_item_3: list[UserModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)
  
    posted_item_4: list[UserModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)

def test_gets_users_with_paging() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: UserModel = create_user(context)
    posted_object_2: UserModel = create_user(context)
    
    sleep(1)
    
    posted_object_3: UserModel = create_user(context)
    posted_object_4: UserModel = create_user(context)

    filters_1: UserSearchModel = UserSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page = 1,
        page_length = 2
    )

    filters_2: UserSearchModel = UserSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page = 2,
        page_length = 2
    )
    
    result_page_1: PagedResponseItemList[UserModel] = get_users(context, filters_1)
    result_page_2: PagedResponseItemList[UserModel] = get_users(context, filters_2)

    ## Page 1

    assert result_page_1 is not None
    assert result_page_1.items is not None
    
    assert result_page_1.paging is not None
    assert result_page_1.paging.page == 1
    assert result_page_1.paging.page_length == 2
    assert result_page_1.paging.sort_by == 'created_at'
    assert result_page_1.paging.is_sort_descending == False

    posted_item_page_1_item_1: list[UserModel] = [item for item in result_page_1.items if item.id == posted_object_1.id]
    assert len(posted_item_page_1_item_1) == 1  
    assert_objects_are_equal(posted_item_page_1_item_1[0], posted_object_1)

    posted_item_page_1_item_2: list[UserModel] = [item for item in result_page_1.items if item.id == posted_object_2.id]
    assert len(posted_item_page_1_item_2) == 1  
    assert_objects_are_equal(posted_item_page_1_item_2[0], posted_object_2)
   
    ## Page 2

    assert result_page_2 is not None
    assert result_page_2.items is not None
    
    assert result_page_2.paging is not None
    assert result_page_2.paging.page == 2
    assert result_page_2.paging.page_length == 2
    assert result_page_2.paging.sort_by == 'created_at'
    assert result_page_2.paging.is_sort_descending == False

    assert len(result_page_1.items) == 2
     
    posted_item_page_2_item_1: list[UserModel] = [item for item in result_page_2.items if item.id == posted_object_3.id]
    assert len(posted_item_page_2_item_1) == 1  
    assert_objects_are_equal(posted_item_page_2_item_1[0], posted_object_3)

    posted_item_page_2_item_2: list[UserModel] = [item for item in result_page_2.items if item.id == posted_object_4.id]
    assert len(posted_item_page_2_item_2) == 1  
    assert_objects_are_equal(posted_item_page_2_item_2[0], posted_object_4)
    
def test_gets_users_with_name_like_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)
    
    matching_random_string_part_1 = generate_random_string(16).upper() 
    matching_random_string_part_2 = generate_random_string(16).upper()
    
    matching_random_string = matching_random_string_part_1 + " " + matching_random_string_part_2
    
    non_matching_random_string = generate_random_string(16)

    posted_object_1: UserModel = create_user(context, UserCreateModel(first_name= f"prefix-{matching_random_string}-suffix"))
    posted_object_2: UserModel = create_user(context, UserCreateModel(last_name= f"{matching_random_string}-suffix"))
    posted_object_3: UserModel = create_user(context, UserCreateModel())
    posted_object_4: UserModel = create_user(context, UserCreateModel(first_name = f"prefix-{matching_random_string_part_1}", last_name= f"{matching_random_string_part_2}-suffix"))

    filters: UserSearchModel = UserSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        name_like = f"{matching_random_string.lower()}"
    )
    
    result: PagedResponseItemList[UserModel] = get_users(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3 
    
    posted_item_1: list[UserModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1)

    posted_item_2: list[UserModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2)
  
    posted_item_4: list[UserModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)
     
def test_gets_users_with_username_like_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)
  
    matching_random_string = generate_random_string(16).upper();
    
    non_matching_random_string = generate_random_string(16)

    posted_object_1: UserModel = create_user(context, UserCreateModel(username= f"prefix-{matching_random_string}-suffix@example.com"))
    posted_object_2: UserModel = create_user(context, UserCreateModel(username= f"{matching_random_string}-suffix@example.com"))
    posted_object_3: UserModel = create_user(context, UserCreateModel(username=f"{non_matching_random_string}@example.com"))
    posted_object_4: UserModel = create_user(context, UserCreateModel(username= f"username@{matching_random_string}.com"))

    filters: UserSearchModel = UserSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        username_like = f"{matching_random_string.lower()}"
    )
    
    result: PagedResponseItemList[UserModel] = get_users(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3 
    
    posted_item_1: list[UserModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1, ["username"])
    assert posted_item_1[0].username.lower() == posted_object_1.username.lower()
    

    posted_item_2: list[UserModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2, ["username"])
    assert posted_item_2[0].username.lower() == posted_object_2.username.lower()
  
    posted_item_4: list[UserModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4, ["username"])
    assert posted_item_4[0].username.lower() == posted_object_4.username.lower()
   
def test_gets_users_with_username_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)
  
    matching_random_string = generate_random_string(16).upper();
    
    non_matching_random_string = generate_random_string(16)

    posted_object_1: UserModel = create_user(context, UserCreateModel(username= f"prefix-{matching_random_string}-suffix@example.com"))
    posted_object_2: UserModel = create_user(context, UserCreateModel(username= f"{matching_random_string}-suffix@example.com"))
    posted_object_3: UserModel = create_user(context, UserCreateModel(username=f"{non_matching_random_string}@example.com"))
    posted_object_4: UserModel = create_user(context, UserCreateModel(username= f"{matching_random_string}@EXAMPLE.com"))

    filters: UserSearchModel = UserSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        username = f"{matching_random_string.lower()}@example.com"
    )
    
    result: PagedResponseItemList[UserModel] = get_users(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 1
     
    posted_item_4: list[UserModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4, ["username"])
    assert posted_item_4[0].username.lower() == posted_object_4.username.lower()
 

def test_gets_user_locations_with_retailer_location_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: UserModel = create_user(context, UserCreateModel(create_retailer_location_if_null=True))
    posted_object_2: UserModel = create_user(context, UserCreateModel(create_retailer_location_if_null=True))
    posted_object_3: UserModel = create_user(context, UserCreateModel(retailer_location_id = posted_object_1.retailer_location_id))
    posted_object_4: UserModel = create_user(context, UserCreateModel(create_retailer_location_if_null=True))

    filters: UserSearchModel = UserSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        retailer_location_ids = f"{posted_object_1.retailer_location_id},{posted_object_4.retailer_location_id}"
    )
    
    result: PagedResponseItemList[UserModel] = get_users(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[UserModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[UserModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[UserModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4) 
    
def test_gets_user_locations_with_retailer_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: UserModel = create_user(context, UserCreateModel(create_retailer_location_if_null=True))
    posted_object_2: UserModel = create_user(context, UserCreateModel(create_retailer_location_if_null=True))
    posted_object_3: UserModel = create_user(context, UserCreateModel(retailer_location_id = posted_object_1.retailer_location_id))
    posted_object_4: UserModel = create_user(context, UserCreateModel(create_retailer_location_if_null=True))

    filters: UserSearchModel = UserSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        retailer_ids = f"{posted_object_1.retailer_id},{posted_object_4.retailer_id}"
    )
    
    result: PagedResponseItemList[UserModel] = get_users(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[UserModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[UserModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[UserModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4) 
     
def test_gets_user_locations_with_vendor_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: UserModel = create_user(context, UserCreateModel(create_vendor_if_null=True))
    posted_object_2: UserModel = create_user(context, UserCreateModel(create_vendor_if_null=True))
    posted_object_3: UserModel = create_user(context, UserCreateModel(vendor_id = posted_object_1.vendor_id))
    posted_object_4: UserModel = create_user(context, UserCreateModel(create_vendor_if_null=True))

    filters: UserSearchModel = UserSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        vendor_ids = f"{posted_object_1.vendor_id},{posted_object_4.vendor_id}"
    )
    
    result: PagedResponseItemList[UserModel] = get_users(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[UserModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[UserModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[UserModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4) 
    
def test_gets_users_with_role_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: UserModel = create_user(context, UserCreateModel(role = "SamsonUser"))
    posted_object_2: UserModel = create_user(context, UserCreateModel(role =  "RetailerUser"))
    posted_object_3: UserModel = create_user(context, UserCreateModel(role =  "SamsonUser"))
    posted_object_4: UserModel = create_user(context, UserCreateModel(role =  "VendorAdmin"))

    filters: UserSearchModel = UserSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        role = "SamsonUser"
    )
    
    result: PagedResponseItemList[UserModel] = get_users(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 2
    
    posted_item_1: list[UserModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[UserModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3) 