from time import sleep
from typing import Any

from tests.qdk.operators.retailer_locations import RetailerLocationCreateModel, RetailerLocationModel, RetailerLocationSearchModel, create_retailer_location, get_retailer_location_by_id, get_retailer_locations, retailer_location_hydration_check
from tests.qdk.qa_requests import qa_get, qa_post
from tests.qdk.types import PagedResponseItemList, RequestOperators, TestContext
from tests.qdk.utils import assert_objects_are_equal, generate_random_string
from urllib.parse import urlencode   
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_gets_retailer_location_by_id() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object = create_retailer_location(context)

    result = get_retailer_location_by_id(context, posted_object.id)

    assert result is not None
    assert result.id == posted_object.id

def test_gets_retailer_location_by_id_with_hydration() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object = create_retailer_location(context)

    result = get_retailer_location_by_id(
        context, 
        posted_object.id,
        request_operators=RequestOperators(hydration_properties=["retailer"])
    )

    assert result is not None
    assert result.id == posted_object.id

    retailer_location_hydration_check(result)

def test_gets_retailer_locations_invalid_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)
     
    result = qa_get(f"{context.api_url}/retailer_locations", query_params={
        'ids': 'not an id,also not an id',
        'retailer_ids': 'not valid,at all,cmon man', 
        'page' : 'not a page num',
        'page_length' : 'not a length num',
        'is_sort_descending' : 'not a bool'
    })

    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 5
    
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: not an id,\n\t1: also not an id\n].'

    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'retailer_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: not valid,\n\t1: at all,\n\t2: cmon man\n].'
     
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

def test_gets_retailer_locations_with_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: RetailerLocationModel = create_retailer_location(context)
    posted_object_2: RetailerLocationModel = create_retailer_location(context)
    posted_object_3: RetailerLocationModel = create_retailer_location(context)
    posted_object_4: RetailerLocationModel = create_retailer_location(context)

    filters: RetailerLocationSearchModel = RetailerLocationSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )
    
    result: PagedResponseItemList[RetailerLocationModel] = get_retailer_locations(context, filters)

    assert result is not None
    assert result.items is not None
    
    assert result.paging is not None
    assert result.paging.page == 1
    assert result.paging.page_length == 25
    assert result.paging.sort_by == 'created_at'
    assert result.paging.is_sort_descending == False

    assert len(result.items) == 4 
    
    posted_item_1: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1)

    posted_item_2: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2)
  
    posted_item_3: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)
  
    posted_item_4: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)
     
def test_gets_retailer_locations_with_ids_filter_with_hydration() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: RetailerLocationModel = create_retailer_location(context)
    posted_object_2: RetailerLocationModel = create_retailer_location(context)
    posted_object_3: RetailerLocationModel = create_retailer_location(context)
    posted_object_4: RetailerLocationModel = create_retailer_location(context)

    filters: RetailerLocationSearchModel = RetailerLocationSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )
    
    result: PagedResponseItemList[RetailerLocationModel] = get_retailer_locations(
        context, 
        filters,
        request_operators=RequestOperators(hydration_properties=["retailer"])
    )

    assert result is not None
    assert result.items is not None
    
    assert result.paging is not None
    assert result.paging.page == 1
    assert result.paging.page_length == 25
    assert result.paging.sort_by == 'created_at'
    assert result.paging.is_sort_descending == False

    assert len(result.items) == 4 
    
    posted_item_1: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1, ["retailer"])
        
    assert posted_item_1[0].retailer is not None
    assert posted_item_1[0].retailer.id is not None
    assert posted_item_1[0].retailer.id == posted_item_1[0].retailer_id

    posted_item_2: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2, ["retailer"])
    
    assert posted_item_2[0].retailer is not None
    assert posted_item_2[0].retailer.id is not None
    assert posted_item_2[0].retailer.id == posted_item_2[0].retailer_id
  
    posted_item_3: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3, ["retailer"])
    
    assert posted_item_3[0].retailer is not None
    assert posted_item_3[0].retailer.id is not None
    assert posted_item_3[0].retailer.id == posted_item_3[0].retailer_id
  
    posted_item_4: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4, ["retailer"])
    
    assert posted_item_4[0].retailer is not None
    assert posted_item_4[0].retailer.id is not None
    assert posted_item_4[0].retailer.id == posted_item_4[0].retailer_id

def test_gets_retailer_locations_with_paging() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: RetailerLocationModel = create_retailer_location(context)
    posted_object_2: RetailerLocationModel = create_retailer_location(context)
    
    sleep(1)
    
    posted_object_3: RetailerLocationModel = create_retailer_location(context)
    posted_object_4: RetailerLocationModel = create_retailer_location(context)

    filters_1: RetailerLocationSearchModel = RetailerLocationSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page = 1,
        page_length = 2
    )

    filters_2: RetailerLocationSearchModel = RetailerLocationSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page = 2,
        page_length = 2
    )
    
    result_page_1: PagedResponseItemList[RetailerLocationModel] = get_retailer_locations(context, filters_1)
    result_page_2: PagedResponseItemList[RetailerLocationModel] = get_retailer_locations(context, filters_2)

    ## Page 1

    assert result_page_1 is not None
    assert result_page_1.items is not None
    
    assert result_page_1.paging is not None
    assert result_page_1.paging.page == 1
    assert result_page_1.paging.page_length == 2
    assert result_page_1.paging.sort_by == 'created_at'
    assert result_page_1.paging.is_sort_descending == False

    posted_item_page_1_item_1: list[RetailerLocationModel] = [item for item in result_page_1.items if item.id == posted_object_1.id]
    assert len(posted_item_page_1_item_1) == 1  
    assert_objects_are_equal(posted_item_page_1_item_1[0], posted_object_1)

    posted_item_page_1_item_2: list[RetailerLocationModel] = [item for item in result_page_1.items if item.id == posted_object_2.id]
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
     
    posted_item_page_2_item_1: list[RetailerLocationModel] = [item for item in result_page_2.items if item.id == posted_object_3.id]
    assert len(posted_item_page_2_item_1) == 1  
    assert_objects_are_equal(posted_item_page_2_item_1[0], posted_object_3)

    posted_item_page_2_item_2: list[RetailerLocationModel] = [item for item in result_page_2.items if item.id == posted_object_4.id]
    assert len(posted_item_page_2_item_2) == 1  
    assert_objects_are_equal(posted_item_page_2_item_2[0], posted_object_4)
  
def test_gets_retailer_locations_with_name_exact_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)
    
    matching_random_string = generate_random_string(16)

    posted_object_1: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(name = f"prefix-{matching_random_string}-matches"))
    posted_object_2: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(name = f"{matching_random_string}-matches"))
    posted_object_3: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(name = f"{matching_random_string}-matches-suffix"))
    posted_object_4: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(name = f"prefix-{matching_random_string}-matches-suffix"))

    filters: RetailerLocationSearchModel = RetailerLocationSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        name = f"{matching_random_string}-matches"
    )
    
    result: PagedResponseItemList[RetailerLocationModel] = get_retailer_locations(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 1
     
    posted_item_2: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2) 

def test_gets_retailer_locations_with_name_like_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)
    
    matching_random_string = generate_random_string(16).upper()
    non_matching_random_string = generate_random_string(16)

    posted_object_1: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(name = f"prefix-{matching_random_string}-suffix"))
    posted_object_2: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(name = f"{matching_random_string}-suffix"))
    posted_object_3: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(name = f"not a match-{non_matching_random_string}"))
    posted_object_4: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(name = f"prefix-{matching_random_string}"))

    filters: RetailerLocationSearchModel = RetailerLocationSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        name_like = f"{matching_random_string.lower()}"
    )
    
    result: PagedResponseItemList[RetailerLocationModel] = get_retailer_locations(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3 
    
    posted_item_1: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1)

    posted_item_2: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2)
  
    posted_item_4: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)
 
def test_gets_retailer_locations_with_retailer_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: RetailerLocationModel = create_retailer_location(context)
    posted_object_2: RetailerLocationModel = create_retailer_location(context)
    posted_object_3: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(retailer_id = posted_object_1.retailer_id))
    posted_object_4: RetailerLocationModel = create_retailer_location(context)

    filters: RetailerLocationSearchModel = RetailerLocationSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        retailer_ids = f"{posted_object_1.retailer_id},{posted_object_4.retailer_id}"
    )
    
    result: PagedResponseItemList[RetailerLocationModel] = get_retailer_locations(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4) 

def test_gets_retailers_with_location_city_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(location_city = f"matchingville"))
    posted_object_2: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(location_city = f"nomatch city"))
    posted_object_3: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(location_city = f"matchingVILLE"))
    posted_object_4: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(location_city = f"matchlesston"))

    filters: RetailerLocationSearchModel = RetailerLocationSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        location_city = f"MATCHingville"
    )
    
    result: PagedResponseItemList[RetailerLocationModel] = get_retailer_locations(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 2
    
    posted_item_1: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)


def test_gets_retailers_with_location_state_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(location_state = f"not the state"))
    posted_object_2: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(location_state = f"yes the STATE"))
    posted_object_3: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(location_state = f"YES the state"))
    posted_object_4: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(location_state = f"Not it mate"))

    filters: RetailerLocationSearchModel = RetailerLocationSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        location_state = f"yes THE state"
    )
    
    result: PagedResponseItemList[RetailerLocationModel] = get_retailer_locations(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 2
    
    posted_item_2: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1  
    assert_objects_are_equal(posted_item_2[0], posted_object_2) 
  
    posted_item_3: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

def test_gets_retailers_with_location_country_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(location_country = f"MC"))
    posted_object_2: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(location_country = f"US"))
    posted_object_3: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(location_country = f"JP"))
    posted_object_4: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(location_country = f"MC"))

    filters: RetailerLocationSearchModel = RetailerLocationSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        location_country = "MC"
    )
    
    result: PagedResponseItemList[RetailerLocationModel] = get_retailer_locations(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 2
    
    posted_item_1: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_4: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)
    
        
def test_gets_retailer_locations_with_account_status_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(account_status = "PausedByBilling"))
    posted_object_2: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(account_status = "PausedByRequest"))
    posted_object_3: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(account_status = "PausedByBilling"))
    posted_object_4: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel(account_status = "Unregistered"))

    filters: RetailerLocationSearchModel = RetailerLocationSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        account_status = "PausedByBilling"
    )
    
    result: PagedResponseItemList[RetailerLocationModel] = get_retailer_locations(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 2
    
    posted_item_1: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[RetailerLocationModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3) 