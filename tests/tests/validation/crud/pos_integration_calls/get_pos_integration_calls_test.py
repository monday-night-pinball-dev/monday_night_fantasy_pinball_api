from time import sleep
from typing import Any

from tests.qdk.operators.pos_integration_calls import PosIntegrationCallCreateModel, PosIntegrationCallModel, PosIntegrationCallSearchModel, create_pos_integration_call, get_pos_integration_call_by_id, get_pos_integration_calls, pos_integration_call_hydration_check
from tests.qdk.qa_requests import qa_get, qa_post
from tests.qdk.types import PagedResponseItemList, RequestOperators, TestContext
from tests.qdk.utils import assert_objects_are_equal, generate_random_string
from urllib.parse import urlencode   
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_gets_pos_integration_call_by_id() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object = create_pos_integration_call(context)

    result = get_pos_integration_call_by_id(context, posted_object.id)

    assert result is not None
    assert result.id == posted_object.id
 
def test_gets_pos_integration_call_by_id() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object = create_pos_integration_call(context)

    result = get_pos_integration_call_by_id(context, posted_object.id, request_operators = RequestOperators(hydration_properties=["retailer", "retailer_location", "pos_integration"]))

    assert result is not None
    assert result.id == posted_object.id
    
    pos_integration_call_hydration_check(result)

def test_gets_pos_integration_calls_invalid_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)
     
    result = qa_get(f"{context.api_url}/pos_integration_calls", query_params={
        'ids': 'not an id,also not an id', 
        'pos_integration_ids': 'BAD IDS',  
        'response_status_code' : 'not an integer',
        'retailer_ids': 'not valid,at all,cmon man',  
        'retailer_location_ids': 'invalid,id,jamboree', 
        'page' : 'not a page num',
        'page_length' : 'not a length num',
        'is_sort_descending' : 'not a bool'
    })

    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 8
    
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: not an id,\n\t1: also not an id\n].'
     
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'pos_integration_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: BAD IDS\n].'
    
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'retailer_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: not valid,\n\t1: at all,\n\t2: cmon man\n].'
        
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'retailer_location_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: invalid,\n\t1: id,\n\t2: jamboree\n].'
    
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'response_status_code' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'int_parsing'
    assert error[0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'
     
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

def test_gets_pos_integration_calls_with_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: PosIntegrationCallModel = create_pos_integration_call(context)
    posted_object_2: PosIntegrationCallModel = create_pos_integration_call(context)
    posted_object_3: PosIntegrationCallModel = create_pos_integration_call(context)
    posted_object_4: PosIntegrationCallModel = create_pos_integration_call(context)

    filters: PosIntegrationCallSearchModel = PosIntegrationCallSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )
    
    result: PagedResponseItemList[PosIntegrationCallModel] = get_pos_integration_calls(context, filters, request_operators = RequestOperators(hydration_properties=["retailer", "retailer_location", "pos_integration"]))

    assert result is not None
    assert result.items is not None
    
    assert result.paging is not None
    assert result.paging.page == 1
    assert result.paging.page_length == 25
    assert result.paging.sort_by == 'created_at'
    assert result.paging.is_sort_descending == False

    assert len(result.items) == 4 
    
    posted_item_1: list[PosIntegrationCallModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1, ["retailer", "retailer_location", "pos_integration"])
    
    pos_integration_call_hydration_check(posted_item_1[0])

    posted_item_2: list[PosIntegrationCallModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2, ["retailer", "retailer_location", "pos_integration"])
    
    pos_integration_call_hydration_check(posted_item_2[0])
  
    posted_item_3: list[PosIntegrationCallModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3, ["retailer", "retailer_location", "pos_integration"])
    
    pos_integration_call_hydration_check(posted_item_3[0])
  
    posted_item_4: list[PosIntegrationCallModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4, ["retailer", "retailer_location", "pos_integration"])
    
    pos_integration_call_hydration_check(posted_item_4[0])
    
def test_gets_pos_integration_calls_with_retailer_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: PosIntegrationCallModel = create_pos_integration_call(context)
    posted_object_2: PosIntegrationCallModel = create_pos_integration_call(context)
    posted_object_3: PosIntegrationCallModel = create_pos_integration_call(context, PosIntegrationCallCreateModel(pos_integration_id = posted_object_1.pos_integration_id))
    posted_object_4: PosIntegrationCallModel = create_pos_integration_call(context)

    filters: PosIntegrationCallSearchModel = PosIntegrationCallSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        retailer_ids = f"{posted_object_1.retailer_id},{posted_object_4.retailer_id}"
    )
    
    result: PagedResponseItemList[PosIntegrationCallModel] = get_pos_integration_calls(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[PosIntegrationCallModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[PosIntegrationCallModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[PosIntegrationCallModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4) 
    
def test_gets_pos_integration_calls_with_retailer_location_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: PosIntegrationCallModel = create_pos_integration_call(context)
    posted_object_2: PosIntegrationCallModel = create_pos_integration_call(context)
    posted_object_3: PosIntegrationCallModel = create_pos_integration_call(context, PosIntegrationCallCreateModel(pos_integration_id = posted_object_1.pos_integration_id))
    posted_object_4: PosIntegrationCallModel = create_pos_integration_call(context)

    filters: PosIntegrationCallSearchModel = PosIntegrationCallSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        retailer_location_ids = f"{posted_object_1.retailer_location_id},{posted_object_4.retailer_location_id}"
    )
    
    result: PagedResponseItemList[PosIntegrationCallModel] = get_pos_integration_calls(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[PosIntegrationCallModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[PosIntegrationCallModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[PosIntegrationCallModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4) 
    
def test_gets_pos_integration_calls_with_pos_integration_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: PosIntegrationCallModel = create_pos_integration_call(context)
    posted_object_2: PosIntegrationCallModel = create_pos_integration_call(context)
    posted_object_3: PosIntegrationCallModel = create_pos_integration_call(context, PosIntegrationCallCreateModel(pos_integration_id = posted_object_1.pos_integration_id))
    posted_object_4: PosIntegrationCallModel = create_pos_integration_call(context)

    filters: PosIntegrationCallSearchModel = PosIntegrationCallSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        pos_integration_ids = f"{posted_object_1.pos_integration_id},{posted_object_4.pos_integration_id}"
    )
    
    result: PagedResponseItemList[PosIntegrationCallModel] = get_pos_integration_calls(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[PosIntegrationCallModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[PosIntegrationCallModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[PosIntegrationCallModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4) 

def test_gets_pos_integration_calls_with_paging() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: PosIntegrationCallModel = create_pos_integration_call(context)
    posted_object_2: PosIntegrationCallModel = create_pos_integration_call(context)
    
    sleep(1)
    
    posted_object_3: PosIntegrationCallModel = create_pos_integration_call(context)
    posted_object_4: PosIntegrationCallModel = create_pos_integration_call(context)

    filters_1: PosIntegrationCallSearchModel = PosIntegrationCallSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page = 1,
        page_length = 2
    )

    filters_2: PosIntegrationCallSearchModel = PosIntegrationCallSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page = 2,
        page_length = 2
    )
    
    result_page_1: PagedResponseItemList[PosIntegrationCallModel] = get_pos_integration_calls(context, filters_1)
    result_page_2: PagedResponseItemList[PosIntegrationCallModel] = get_pos_integration_calls(context, filters_2)

    ## Page 1

    assert result_page_1 is not None
    assert result_page_1.items is not None
    
    assert result_page_1.paging is not None
    assert result_page_1.paging.page == 1
    assert result_page_1.paging.page_length == 2
    assert result_page_1.paging.sort_by == 'created_at'
    assert result_page_1.paging.is_sort_descending == False

    posted_item_page_1_item_1: list[PosIntegrationCallModel] = [item for item in result_page_1.items if item.id == posted_object_1.id]
    assert len(posted_item_page_1_item_1) == 1  
    assert_objects_are_equal(posted_item_page_1_item_1[0], posted_object_1)

    posted_item_page_1_item_2: list[PosIntegrationCallModel] = [item for item in result_page_1.items if item.id == posted_object_2.id]
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
     
    posted_item_page_2_item_1: list[PosIntegrationCallModel] = [item for item in result_page_2.items if item.id == posted_object_3.id]
    assert len(posted_item_page_2_item_1) == 1  
    assert_objects_are_equal(posted_item_page_2_item_1[0], posted_object_3)

    posted_item_page_2_item_2: list[PosIntegrationCallModel] = [item for item in result_page_2.items if item.id == posted_object_4.id]
    assert len(posted_item_page_2_item_2) == 1  
    assert_objects_are_equal(posted_item_page_2_item_2[0], posted_object_4)
  
def test_gets_pos_integration_calls_with_response_status_code_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)
    
    matching_random_string = generate_random_string(16)

    posted_object_1: PosIntegrationCallModel = create_pos_integration_call(context, PosIntegrationCallCreateModel(response_status_code = 200))
    posted_object_2: PosIntegrationCallModel = create_pos_integration_call(context, PosIntegrationCallCreateModel(response_status_code = 401))
    posted_object_3: PosIntegrationCallModel = create_pos_integration_call(context, PosIntegrationCallCreateModel(response_status_code = 200))
    posted_object_4: PosIntegrationCallModel = create_pos_integration_call(context, PosIntegrationCallCreateModel(response_status_code = 500))

    filters: PosIntegrationCallSearchModel = PosIntegrationCallSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        response_status_code = 200
    )
    
    result: PagedResponseItemList[PosIntegrationCallModel] = get_pos_integration_calls(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 2
     
    posted_item_1: list[PosIntegrationCallModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1 
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
    
    posted_item_3: list[PosIntegrationCallModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3) 
 