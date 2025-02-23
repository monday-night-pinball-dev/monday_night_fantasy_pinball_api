from time import sleep
from typing import Any

from tests.qdk.operators.vendors import VendorCreateModel, VendorModel, VendorSearchModel, create_vendor, get_vendor_by_id, get_vendors
from tests.qdk.qa_requests import qa_get, qa_post
from tests.qdk.types import PagedResponseItemList, TestContext
from tests.qdk.utils import assert_objects_are_equal, generate_random_string
from urllib.parse import urlencode   
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_gets_vendor_by_id() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object = create_vendor(context)

    result = get_vendor_by_id(context, posted_object.id)

    assert result is not None
    assert result.id == posted_object.id

def test_gets_vendors_invalid_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)
     
    result = qa_get(f"{context.api_url}/vendors", query_params={
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

def test_gets_vendors_with_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: VendorModel = create_vendor(context)
    posted_object_2: VendorModel = create_vendor(context)
    posted_object_3: VendorModel = create_vendor(context)
    posted_object_4: VendorModel = create_vendor(context)

    filters: VendorSearchModel = VendorSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )
    
    result: PagedResponseItemList[VendorModel] = get_vendors(context, filters)

    assert result is not None
    assert result.items is not None
    
    assert result.paging is not None
    assert result.paging.page == 1
    assert result.paging.page_length == 25
    assert result.paging.sort_by == 'created_at'
    assert result.paging.is_sort_descending == False

    assert len(result.items) == 4 
    
    posted_item_1: list[VendorModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1)

    posted_item_2: list[VendorModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2)
  
    posted_item_3: list[VendorModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)
  
    posted_item_4: list[VendorModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)

def test_gets_vendors_with_paging() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: VendorModel = create_vendor(context)
    posted_object_2: VendorModel = create_vendor(context)
    
    sleep(1)
    
    posted_object_3: VendorModel = create_vendor(context)
    posted_object_4: VendorModel = create_vendor(context)

    filters_1: VendorSearchModel = VendorSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page = 1,
        page_length = 2
    )

    filters_2: VendorSearchModel = VendorSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page = 2,
        page_length = 2
    )
    
    result_page_1: PagedResponseItemList[VendorModel] = get_vendors(context, filters_1)
    result_page_2: PagedResponseItemList[VendorModel] = get_vendors(context, filters_2)

    ## Page 1

    assert result_page_1 is not None
    assert result_page_1.items is not None
    
    assert result_page_1.paging is not None
    assert result_page_1.paging.page == 1
    assert result_page_1.paging.page_length == 2
    assert result_page_1.paging.sort_by == 'created_at'
    assert result_page_1.paging.is_sort_descending == False

    posted_item_page_1_item_1: list[VendorModel] = [item for item in result_page_1.items if item.id == posted_object_1.id]
    assert len(posted_item_page_1_item_1) == 1  
    assert_objects_are_equal(posted_item_page_1_item_1[0], posted_object_1)

    posted_item_page_1_item_2: list[VendorModel] = [item for item in result_page_1.items if item.id == posted_object_2.id]
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
     
    posted_item_page_2_item_1: list[VendorModel] = [item for item in result_page_2.items if item.id == posted_object_3.id]
    assert len(posted_item_page_2_item_1) == 1  
    assert_objects_are_equal(posted_item_page_2_item_1[0], posted_object_3)

    posted_item_page_2_item_2: list[VendorModel] = [item for item in result_page_2.items if item.id == posted_object_4.id]
    assert len(posted_item_page_2_item_2) == 1  
    assert_objects_are_equal(posted_item_page_2_item_2[0], posted_object_4)
  
def test_gets_vendors_with_name_exact_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)
    
    matching_random_string = generate_random_string(16)

    posted_object_1: VendorModel = create_vendor(context, VendorCreateModel(name = f"prefix-{matching_random_string}-matches"))
    posted_object_2: VendorModel = create_vendor(context, VendorCreateModel(name = f"{matching_random_string}-matches"))
    posted_object_3: VendorModel = create_vendor(context, VendorCreateModel(name = f"{matching_random_string}-matches-suffix"))
    posted_object_4: VendorModel = create_vendor(context, VendorCreateModel(name = f"prefix-{matching_random_string}-matches-suffix"))

    filters: VendorSearchModel = VendorSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        name = f"{matching_random_string}-matches"
    )
    
    result: PagedResponseItemList[VendorModel] = get_vendors(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 1
     
    posted_item_2: list[VendorModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2) 

def test_gets_vendors_with_name_like_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)
    
    matching_random_string = generate_random_string(16).upper()
    non_matching_random_string = generate_random_string(16)

    posted_object_1: VendorModel = create_vendor(context, VendorCreateModel(name = f"prefix-{matching_random_string}-suffix"))
    posted_object_2: VendorModel = create_vendor(context, VendorCreateModel(name = f"{matching_random_string}-suffix"))
    posted_object_3: VendorModel = create_vendor(context, VendorCreateModel(name = f"not a match-{non_matching_random_string}"))
    posted_object_4: VendorModel = create_vendor(context, VendorCreateModel(name = f"prefix-{matching_random_string}"))

    filters: VendorSearchModel = VendorSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        name_like = f"{matching_random_string.lower()}"
    )
    
    result: PagedResponseItemList[VendorModel] = get_vendors(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3 
    
    posted_item_1: list[VendorModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1)

    posted_item_2: list[VendorModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2)
  
    posted_item_4: list[VendorModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)
 

def test_gets_vendor_locations_with_unregistered_vendor_referring_retailer_location_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: VendorModel = create_vendor(context, VendorCreateModel(create_unregistered_vendor_referring_retailer_location_if_null=True))
    posted_object_2: VendorModel = create_vendor(context, VendorCreateModel(create_unregistered_vendor_referring_retailer_location_if_null=True))
    posted_object_3: VendorModel = create_vendor(context, VendorCreateModel(unregistered_vendor_referring_retailer_location_id = posted_object_1.unregistered_vendor_referring_retailer_location_id))
    posted_object_4: VendorModel = create_vendor(context, VendorCreateModel(create_unregistered_vendor_referring_retailer_location_if_null=True))

    filters: VendorSearchModel = VendorSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        unregistered_vendor_referring_retailer_location_ids = f"{posted_object_1.unregistered_vendor_referring_retailer_location_id},{posted_object_4.unregistered_vendor_referring_retailer_location_id}"
    )
    
    result: PagedResponseItemList[VendorModel] = get_vendors(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[VendorModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[VendorModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[VendorModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4) 
    
def test_gets_vendors_with_hq_city_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: VendorModel = create_vendor(context, VendorCreateModel(hq_city = f"matchingville"))
    posted_object_2: VendorModel = create_vendor(context, VendorCreateModel(hq_city = f"nomatch city"))
    posted_object_3: VendorModel = create_vendor(context, VendorCreateModel(hq_city = f"matchingVILLE"))
    posted_object_4: VendorModel = create_vendor(context, VendorCreateModel(hq_city = f"matchlesston"))

    filters: VendorSearchModel = VendorSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        hq_city = f"MATCHingville"
    )
    
    result: PagedResponseItemList[VendorModel] = get_vendors(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 2
    
    posted_item_1: list[VendorModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[VendorModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)


def test_gets_vendors_with_hq_state_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: VendorModel = create_vendor(context, VendorCreateModel(hq_state = f"not the state"))
    posted_object_2: VendorModel = create_vendor(context, VendorCreateModel(hq_state = f"yes the STATE"))
    posted_object_3: VendorModel = create_vendor(context, VendorCreateModel(hq_state = f"YES the state"))
    posted_object_4: VendorModel = create_vendor(context, VendorCreateModel(hq_state = f"Not it mate"))

    filters: VendorSearchModel = VendorSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        hq_state = f"yes THE state"
    )
    
    result: PagedResponseItemList[VendorModel] = get_vendors(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 2
    
    posted_item_2: list[VendorModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1  
    assert_objects_are_equal(posted_item_2[0], posted_object_2) 
  
    posted_item_3: list[VendorModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

def test_gets_vendors_with_hq_country_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: VendorModel = create_vendor(context, VendorCreateModel(hq_country = f"MC"))
    posted_object_2: VendorModel = create_vendor(context, VendorCreateModel(hq_country = f"US"))
    posted_object_3: VendorModel = create_vendor(context, VendorCreateModel(hq_country = f"JP"))
    posted_object_4: VendorModel = create_vendor(context, VendorCreateModel(hq_country = f"MC"))

    filters: VendorSearchModel = VendorSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        hq_country = "MC"
    )
    
    result: PagedResponseItemList[VendorModel] = get_vendors(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 2
    
    posted_item_1: list[VendorModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_4: list[VendorModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)
    
def test_gets_vendors_with_account_status_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: VendorModel = create_vendor(context, VendorCreateModel(account_status = "PausedByBilling"))
    posted_object_2: VendorModel = create_vendor(context, VendorCreateModel(account_status = "PausedByRequest"))
    posted_object_3: VendorModel = create_vendor(context, VendorCreateModel(account_status = "PausedByBilling"))
    posted_object_4: VendorModel = create_vendor(context, VendorCreateModel(account_status = "Unregistered"))

    filters: VendorSearchModel = VendorSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        account_status = "PausedByBilling"
    )
    
    result: PagedResponseItemList[VendorModel] = get_vendors(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 2
    
    posted_item_1: list[VendorModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[VendorModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3) 