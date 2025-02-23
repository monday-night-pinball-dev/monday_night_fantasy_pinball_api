from time import sleep
from typing import Any

from tests.qdk.operators.inventory_intake_jobs import InventoryIntakeJobCreateModel, InventoryIntakeJobModel, InventoryIntakeJobSearchModel, create_inventory_intake_job, get_inventory_intake_job_by_id, get_inventory_intake_jobs, inventory_intake_job_hydration_check
from tests.qdk.qa_requests import qa_get
from tests.qdk.types import PagedResponseItemList, RequestOperators, TestContext
from tests.qdk.utils import assert_objects_are_equal 
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_gets_inventory_intake_job_by_id() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object = create_inventory_intake_job(context)

    result = get_inventory_intake_job_by_id(context, posted_object.id)

    assert result is not None
    assert result.id == posted_object.id

def test_gets_inventory_intake_job_by_id_with_hydration() -> None:

    populate_configuration_if_not_exists(

    ) 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object = create_inventory_intake_job(
        context, 
        InventoryIntakeJobCreateModel(
            create_parent_batch_job_if_null = True,
            create_simulator_response_if_null= True
        )
    )

    result = get_inventory_intake_job_by_id(context, posted_object.id, request_operators = RequestOperators(hydration_properties=[
        "retailer_location",
         "retailer",
          "parent_batch_job"
          , "simulator_response"]))

    assert result is not None
    assert result.id == posted_object.id

    inventory_intake_job_hydration_check(result)

def test_gets_inventory_intake_jobs_invalid_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)
     
    result = qa_get(f"{context.api_url}/inventory_intake_jobs", query_params={
        'ids': 'not an id,also not an id', 
        'retailer_ids': 'not valid,at all,cmon man',  
        'retailer_location_ids': 'invalid,id,jamboree', 
        'status' : 'not a valid status',
        'snapshot_hour_min' : 'not a valid time',
        'snapshot_hour_max' : 'not a valid time',
        'page' : 'not a page num',
        'page_length' : 'not a length num',
        'is_sort_descending' : 'not a bool'
    })

    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 9
    
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: not an id,\n\t1: also not an id\n].'
    
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'retailer_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: not valid,\n\t1: at all,\n\t2: cmon man\n].'
        
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'retailer_location_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: invalid,\n\t1: id,\n\t2: jamboree\n].'
        
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'snapshot_hour_min' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'datetime_from_date_parsing'
    assert error[0]['msg'] == 'Input should be a valid datetime or date, invalid character in year'

    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'snapshot_hour_max' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'datetime_from_date_parsing'
    assert error[0]['msg'] == 'Input should be a valid datetime or date, invalid character in year'
    
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'status' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'enum'
    assert error[0]['msg'] == "Input should be 'Requested', 'Processing', 'Complete' or 'Failed'"
    
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

def test_gets_inventory_intake_jobs_with_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: InventoryIntakeJobModel = create_inventory_intake_job(context)
    posted_object_2: InventoryIntakeJobModel = create_inventory_intake_job(context)
    posted_object_3: InventoryIntakeJobModel = create_inventory_intake_job(context)
    posted_object_4: InventoryIntakeJobModel = create_inventory_intake_job(context)

    filters: InventoryIntakeJobSearchModel = InventoryIntakeJobSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )
    
    result: PagedResponseItemList[InventoryIntakeJobModel] = get_inventory_intake_jobs(context, filters)

    assert result is not None
    assert result.items is not None
    
    assert result.paging is not None
    assert result.paging.page == 1
    assert result.paging.page_length == 25
    assert result.paging.sort_by == 'created_at'
    assert result.paging.is_sort_descending == False

    assert len(result.items) == 4 
    
    posted_item_1: list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1)

    posted_item_2: list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2)
  
    posted_item_3: list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)
  
    posted_item_4: list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)

def test_gets_inventory_intake_jobs_with_ids_filter_with_hydration() -> None:

    populate_configuration_if_not_exists(

    ) 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: InventoryIntakeJobModel = create_inventory_intake_job(
        context,
        InventoryIntakeJobCreateModel(
            create_parent_batch_job_if_null = True,
            create_simulator_response_if_null= True
        )
    )
    
    posted_object_2: InventoryIntakeJobModel = create_inventory_intake_job(
        context,
        InventoryIntakeJobCreateModel(
            create_parent_batch_job_if_null = True,
            create_simulator_response_if_null=True
        )
    )
    
    posted_object_3: InventoryIntakeJobModel = create_inventory_intake_job(
        context,
        InventoryIntakeJobCreateModel(
            create_parent_batch_job_if_null = True,
            create_simulator_response_if_null=True
        )
    )
    
    posted_object_4: InventoryIntakeJobModel = create_inventory_intake_job(
        context,
        InventoryIntakeJobCreateModel(
            create_parent_batch_job_if_null = True,
            create_simulator_response_if_null=True
        )
    )

    filters: InventoryIntakeJobSearchModel = InventoryIntakeJobSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )
    
    result: PagedResponseItemList[InventoryIntakeJobModel] = get_inventory_intake_jobs(
        context,
        filters,
        request_operators = RequestOperators(
            hydration_properties=[
                "retailer_location",
                "retailer",
                "parent_batch_job",
                "simulator_response"
            ]
        )
    )

    assert result is not None
    assert result.items is not None
    
    assert result.paging is not None
    assert result.paging.page == 1
    assert result.paging.page_length == 25
    assert result.paging.sort_by == 'created_at'
    assert result.paging.is_sort_descending == False

    assert len(result.items) == 4 
    
    posted_item_1: list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1, ['retailer_location', 'retailer', 'parent_batch_job', 'simulator_response'])
    
    inventory_intake_job_hydration_check(posted_item_1[0])

    posted_item_2: list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2, ['retailer_location', 'retailer', 'parent_batch_job', 'simulator_response'])
    
    inventory_intake_job_hydration_check(posted_item_2[0])

    posted_item_3: list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3, ['retailer_location', 'retailer', 'parent_batch_job', 'simulator_response'])
    
    inventory_intake_job_hydration_check(posted_item_3[0])
  
    posted_item_4:list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4, ['retailer_location', 'retailer', 'parent_batch_job', 'simulator_response'])
    
    inventory_intake_job_hydration_check(posted_item_4[0])


def test_gets_inventory_intake_jobs_with_paging() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: InventoryIntakeJobModel = create_inventory_intake_job(context)
    posted_object_2: InventoryIntakeJobModel = create_inventory_intake_job(context)
    
    sleep(1)
    
    posted_object_3: InventoryIntakeJobModel = create_inventory_intake_job(context)
    posted_object_4: InventoryIntakeJobModel = create_inventory_intake_job(context)

    filters_1: InventoryIntakeJobSearchModel = InventoryIntakeJobSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page = 1,
        page_length = 2
    )

    filters_2: InventoryIntakeJobSearchModel = InventoryIntakeJobSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page = 2,
        page_length = 2
    )
    
    result_page_1: PagedResponseItemList[InventoryIntakeJobModel] = get_inventory_intake_jobs(context, filters_1)
    result_page_2: PagedResponseItemList[InventoryIntakeJobModel] = get_inventory_intake_jobs(context, filters_2)

    ## Page 1

    assert result_page_1 is not None
    assert result_page_1.items is not None
    
    assert result_page_1.paging is not None
    assert result_page_1.paging.page == 1
    assert result_page_1.paging.page_length == 2
    assert result_page_1.paging.sort_by == 'created_at'
    assert result_page_1.paging.is_sort_descending == False

    posted_item_page_1_item_1: list[InventoryIntakeJobModel] = [item for item in result_page_1.items if item.id == posted_object_1.id]
    assert len(posted_item_page_1_item_1) == 1  
    assert_objects_are_equal(posted_item_page_1_item_1[0], posted_object_1)

    posted_item_page_1_item_2: list[InventoryIntakeJobModel] = [item for item in result_page_1.items if item.id == posted_object_2.id]
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
     
    posted_item_page_2_item_1: list[InventoryIntakeJobModel] = [item for item in result_page_2.items if item.id == posted_object_3.id]
    assert len(posted_item_page_2_item_1) == 1  
    assert_objects_are_equal(posted_item_page_2_item_1[0], posted_object_3)

    posted_item_page_2_item_2: list[InventoryIntakeJobModel] = [item for item in result_page_2.items if item.id == posted_object_4.id]
    assert len(posted_item_page_2_item_2) == 1  
    assert_objects_are_equal(posted_item_page_2_item_2[0], posted_object_4)
      
def test_gets_inventory_intake_jobs_with_retailer_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: InventoryIntakeJobModel = create_inventory_intake_job(context)
    posted_object_2: InventoryIntakeJobModel = create_inventory_intake_job(context)
    posted_object_3: InventoryIntakeJobModel = create_inventory_intake_job(context, InventoryIntakeJobCreateModel(retailer_location_id = posted_object_1.retailer_location_id))
    posted_object_4: InventoryIntakeJobModel = create_inventory_intake_job(context)

    filters: InventoryIntakeJobSearchModel = InventoryIntakeJobSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        retailer_ids = f"{posted_object_1.retailer_id},{posted_object_4.retailer_id}"
    )
    
    result: PagedResponseItemList[InventoryIntakeJobModel] = get_inventory_intake_jobs(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4) 
    
def test_gets_inventory_intake_jobs_with_retailer_location_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: InventoryIntakeJobModel = create_inventory_intake_job(context)
    posted_object_2: InventoryIntakeJobModel = create_inventory_intake_job(context)
    posted_object_3: InventoryIntakeJobModel = create_inventory_intake_job(context, InventoryIntakeJobCreateModel(retailer_location_id = posted_object_1.retailer_location_id))
    posted_object_4: InventoryIntakeJobModel = create_inventory_intake_job(context)

    filters: InventoryIntakeJobSearchModel = InventoryIntakeJobSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        retailer_location_ids = f"{posted_object_1.retailer_location_id},{posted_object_4.retailer_location_id}"
    )
    
    result: PagedResponseItemList[InventoryIntakeJobModel] = get_inventory_intake_jobs(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4) 
    
    
def test_gets_inventory_intake_jobs_with_status_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: InventoryIntakeJobModel = create_inventory_intake_job(context, InventoryIntakeJobCreateModel(status = f"Complete"))
    posted_object_2: InventoryIntakeJobModel = create_inventory_intake_job(context, InventoryIntakeJobCreateModel(status = f"Failed"))
    posted_object_3: InventoryIntakeJobModel = create_inventory_intake_job(context, InventoryIntakeJobCreateModel(status = f"Complete"))
    posted_object_4: InventoryIntakeJobModel = create_inventory_intake_job(context, InventoryIntakeJobCreateModel(status = f"Requested"))

    filters: InventoryIntakeJobSearchModel = InventoryIntakeJobSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        status = f"Complete"
    )
    
    result: PagedResponseItemList[InventoryIntakeJobModel] = get_inventory_intake_jobs(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 2
    
    posted_item_1: list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)
    
    
def test_gets_inventory_intake_jobs_with_snapshot_hour_filter_min_only() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: InventoryIntakeJobModel = create_inventory_intake_job(context, InventoryIntakeJobCreateModel(snapshot_hour = "2021-01-01T01:00:00.000Z"))
    posted_object_2: InventoryIntakeJobModel = create_inventory_intake_job(context, InventoryIntakeJobCreateModel(snapshot_hour = "2024-04-04T04:00:00.000Z"))
    posted_object_3: InventoryIntakeJobModel = create_inventory_intake_job(context, InventoryIntakeJobCreateModel(snapshot_hour = "2022-02-02T02:00:00.000Z"))
    posted_object_4: InventoryIntakeJobModel = create_inventory_intake_job(context, InventoryIntakeJobCreateModel(snapshot_hour = "2023-03-03T03:00:00.000Z"))

    filters: InventoryIntakeJobSearchModel = InventoryIntakeJobSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        snapshot_hour_min = "2023-03-03T03:00:00.000Z" 
    )
    
    result: PagedResponseItemList[InventoryIntakeJobModel] = get_inventory_intake_jobs(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 2
    
    posted_item_2: list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1  
    assert_objects_are_equal(posted_item_2[0], posted_object_2) 
  
    posted_item_4: list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)

def test_gets_inventory_intake_jobs_with_snapshot_hour_filter_max_only() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: InventoryIntakeJobModel = create_inventory_intake_job(context, InventoryIntakeJobCreateModel(snapshot_hour = "2021-01-01T01:00:00.000Z"))
    posted_object_2: InventoryIntakeJobModel = create_inventory_intake_job(context, InventoryIntakeJobCreateModel(snapshot_hour = "2024-04-04T04:00:00.000Z"))
    posted_object_3: InventoryIntakeJobModel = create_inventory_intake_job(context, InventoryIntakeJobCreateModel(snapshot_hour = "2022-02-02T02:00:00.000Z"))
    posted_object_4: InventoryIntakeJobModel = create_inventory_intake_job(context, InventoryIntakeJobCreateModel(snapshot_hour = "2023-03-03T03:00:00.000Z"))

    filters: InventoryIntakeJobSearchModel = InventoryIntakeJobSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        snapshot_hour_max = "2022-02-02T02:00:00.000Z" 
    )
    
    result: PagedResponseItemList[InventoryIntakeJobModel] = get_inventory_intake_jobs(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 2
    
    posted_item_1: list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)
    

def test_gets_inventory_intake_jobs_with_status_filter_max_only() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: InventoryIntakeJobModel = create_inventory_intake_job(context, InventoryIntakeJobCreateModel(snapshot_hour = "2021-01-01T01:00:00.000Z"))
    posted_object_2: InventoryIntakeJobModel = create_inventory_intake_job(context, InventoryIntakeJobCreateModel(snapshot_hour = "2024-04-04T04:00:00.000Z"))
    posted_object_3: InventoryIntakeJobModel = create_inventory_intake_job(context, InventoryIntakeJobCreateModel(snapshot_hour = "2022-02-02T02:00:00.000Z"))
    posted_object_4: InventoryIntakeJobModel = create_inventory_intake_job(context, InventoryIntakeJobCreateModel(snapshot_hour = "2023-03-03T03:00:00.000Z"))

    filters: InventoryIntakeJobSearchModel = InventoryIntakeJobSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        snapshot_hour_min = "2022-02-02T02:00:00.000Z",
        snapshot_hour_max = "2023-03-03T03:00:00.000Z" 
    )
    
    result: PagedResponseItemList[InventoryIntakeJobModel] = get_inventory_intake_jobs(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 2
  
    posted_item_3: list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)
        
    posted_item_4: list[InventoryIntakeJobModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1  
    assert_objects_are_equal(posted_item_4[0], posted_object_4) 
