from time import sleep
from typing import Any

from tests.qdk.operators.inventory_product_snapshots import InventoryProductSnapshotCreateModel, InventoryProductSnapshotModel, InventoryProductSnapshotSearchModel, create_inventory_product_snapshot, get_inventory_product_snapshot_by_id, get_inventory_product_snapshots, inventory_product_snapshot_hydration_check
from tests.qdk.operators.products import ProductCreateModel
from tests.qdk.qa_requests import qa_get, qa_post
from tests.qdk.types import PagedResponseItemList, RequestOperators, TestContext
from tests.qdk.utils import assert_objects_are_equal, generate_random_string
from urllib.parse import urlencode   
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_gets_inventory_product_snapshot_by_id() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object = create_inventory_product_snapshot(context)

    result = get_inventory_product_snapshot_by_id(context, posted_object.id)

    assert result is not None
    assert result.id == posted_object.id
    
def test_gets_inventory_product_snapshot_by_id_with_hydration() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object = create_inventory_product_snapshot(
        context,
        InventoryProductSnapshotCreateModel(
            create_inventory_intake_job_if_null= True,
            product= ProductCreateModel(
                create_vendor_if_null= True
            )
        )
    )

    result = get_inventory_product_snapshot_by_id(context, posted_object.id, request_operators = RequestOperators(hydration_properties=["retailer_location", "retailer", "inventory_intake_job", "product", "vendor"]))

    assert result is not None
    assert result.id == posted_object.id
    
    inventory_product_snapshot_hydration_check(result)

def test_gets_inventory_product_snapshots_invalid_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)
     
    result = qa_get(f"{context.api_url}/inventory_product_snapshots", query_params={
        'ids': 'not an id,also not an id', 
        'retailer_ids': 'not valid,at all,cmon man',  
        'product_ids': 'also,not,valid',  
        'vendor_ids': 'are,you,trying?',  
        'inventory_intake_job_ids': 'lolcmon',  
        'retailer_location_ids': 'invalid,id,jamboree', 
        'snapshot_hour_min' : 'not a valid datetime',
        'snapshot_hour_max' : 'also not a valid datetime',
        'page' : 'not a page num',
        'page_length' : 'not a length num',
        'is_sort_descending' : 'not a bool'
    })

    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 11
    
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: not an id,\n\t1: also not an id\n].'
    
    
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'product_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'    
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: also,\n\t1: not,\n\t2: valid\n].'
    
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'vendor_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'    
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: are,\n\t1: you,\n\t2: trying?\n].'
    
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'inventory_intake_job_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'    
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: lolcmon\n].'
    
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'retailer_location_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'    
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: invalid,\n\t1: id,\n\t2: jamboree\n].'
    
        
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'retailer_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'    
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: not valid,\n\t1: at all,\n\t2: cmon man\n].'
    
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'snapshot_hour_min' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'datetime_from_date_parsing'
    assert error[0]['msg'] == 'Input should be a valid datetime or date, invalid character in year'
    
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'snapshot_hour_max' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'datetime_from_date_parsing'
    assert error[0]['msg'] == 'Input should be a valid datetime or date, invalid character in year'
    
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
    
    
def test_gets_inventory_product_snapshots_with_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: InventoryProductSnapshotModel = create_inventory_product_snapshot(context)
    posted_object_2: InventoryProductSnapshotModel = create_inventory_product_snapshot(context)
    posted_object_3: InventoryProductSnapshotModel = create_inventory_product_snapshot(context)
    posted_object_4: InventoryProductSnapshotModel = create_inventory_product_snapshot(context)

    filters: InventoryProductSnapshotSearchModel = InventoryProductSnapshotSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )
    
    result: PagedResponseItemList[InventoryProductSnapshotModel] = get_inventory_product_snapshots(context, filters)

    assert result is not None
    assert result.items is not None
    
    assert result.paging is not None
    assert result.paging.page == 1
    assert result.paging.page_length == 25
    assert result.paging.sort_by == 'created_at'
    assert result.paging.is_sort_descending == False

    assert len(result.items) == 4 
    
    posted_item_1: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1)

    posted_item_2: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2)
  
    posted_item_3: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)
  
    posted_item_4: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)
     
def test_gets_inventory_product_snapshots_with_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: InventoryProductSnapshotModel = create_inventory_product_snapshot(
        context,
        InventoryProductSnapshotCreateModel(
            create_inventory_intake_job_if_null= True,
            product= ProductCreateModel(
                create_vendor_if_null= True
            )
        )
    )
    posted_object_2: InventoryProductSnapshotModel = create_inventory_product_snapshot(
        context,
        InventoryProductSnapshotCreateModel(
            create_inventory_intake_job_if_null= True,
            product= ProductCreateModel(
                create_vendor_if_null= True
            )
        )
    )
    posted_object_3: InventoryProductSnapshotModel = create_inventory_product_snapshot(
        context,
        InventoryProductSnapshotCreateModel(
            create_inventory_intake_job_if_null= True,
            product= ProductCreateModel(
                create_vendor_if_null= True
            )
        )
    )
    posted_object_4: InventoryProductSnapshotModel = create_inventory_product_snapshot(
        context,
        InventoryProductSnapshotCreateModel(
            create_inventory_intake_job_if_null= True,
            product= ProductCreateModel(
                create_vendor_if_null= True
            )
        )
    )

    filters: InventoryProductSnapshotSearchModel = InventoryProductSnapshotSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )
    
    result: PagedResponseItemList[InventoryProductSnapshotModel] = get_inventory_product_snapshots(context, filters, request_operators = RequestOperators(hydration_properties=["retailer_location", "retailer", "inventory_intake_job", "product", "vendor"]))

    assert result is not None
    assert result.items is not None
    
    assert result.paging is not None
    assert result.paging.page == 1
    assert result.paging.page_length == 25
    assert result.paging.sort_by == 'created_at'
    assert result.paging.is_sort_descending == False

    assert len(result.items) == 4 
    
    posted_item_1: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1, ["retailer_location", "retailer", "inventory_intake_job", "product", "vendor"])
    
    inventory_product_snapshot_hydration_check(posted_item_1[0])

    posted_item_2: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2, ["retailer_location", "retailer", "inventory_intake_job", "product", "vendor"])
    
    inventory_product_snapshot_hydration_check(posted_item_2[0])
  
    posted_item_3: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3, ["retailer_location", "retailer", "inventory_intake_job", "product", "vendor"])
    
    inventory_product_snapshot_hydration_check(posted_item_3[0])
  
    posted_item_4: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4, ["retailer_location", "retailer", "inventory_intake_job", "product", "vendor"])
    
    inventory_product_snapshot_hydration_check(posted_item_4[0])
    
def test_gets_inventory_product_snapshots_with_retailer_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: InventoryProductSnapshotModel = create_inventory_product_snapshot(context)
    posted_object_2: InventoryProductSnapshotModel = create_inventory_product_snapshot(context)
    posted_object_3: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(retailer_location_id = posted_object_1.retailer_location_id))
    posted_object_4: InventoryProductSnapshotModel = create_inventory_product_snapshot(context)

    filters: InventoryProductSnapshotSearchModel = InventoryProductSnapshotSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        retailer_ids = f"{posted_object_1.retailer_id},{posted_object_4.retailer_id}"
    )
    
    result: PagedResponseItemList[InventoryProductSnapshotModel] = get_inventory_product_snapshots(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4) 
    
def test_gets_inventory_product_snapshots_with_retailer_location_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: InventoryProductSnapshotModel = create_inventory_product_snapshot(context)
    posted_object_2: InventoryProductSnapshotModel = create_inventory_product_snapshot(context)
    posted_object_3: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(retailer_location_id = posted_object_1.retailer_location_id))
    posted_object_4: InventoryProductSnapshotModel = create_inventory_product_snapshot(context)

    filters: InventoryProductSnapshotSearchModel = InventoryProductSnapshotSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        retailer_location_ids = f"{posted_object_1.retailer_location_id},{posted_object_4.retailer_location_id}"
    )
    
    result: PagedResponseItemList[InventoryProductSnapshotModel] = get_inventory_product_snapshots(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4) 
    
     
    assert_objects_are_equal(posted_item_4[0], posted_object_4) 
    
def test_gets_inventory_product_snapshots_with_vendor_ids_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(product = ProductCreateModel(create_vendor_if_null= True)))
    posted_object_2: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(product = ProductCreateModel(create_vendor_if_null= True)))
    posted_object_3: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(product_id = posted_object_1.product_id))
    posted_object_4: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(product = ProductCreateModel(create_vendor_if_null= True)))

    filters: InventoryProductSnapshotSearchModel = InventoryProductSnapshotSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        vendor_ids = f"{posted_object_1.vendor_id},{posted_object_4.vendor_id}"
    )
    
    result: PagedResponseItemList[InventoryProductSnapshotModel] = get_inventory_product_snapshots(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)
    
def test_gets_inventory_product_snapshots_with_inventory_intake_job_ids_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(create_inventory_intake_job_if_null= True))
    posted_object_2: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(create_inventory_intake_job_if_null= True))    
    posted_object_3: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(inventory_intake_job_id = posted_object_1.inventory_intake_job_id))
    posted_object_4: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(create_inventory_intake_job_if_null= True))

    filters: InventoryProductSnapshotSearchModel = InventoryProductSnapshotSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        inventory_intake_job_ids = f"{posted_object_1.inventory_intake_job_id},{posted_object_4.inventory_intake_job_id}"
    )
    
    result: PagedResponseItemList[InventoryProductSnapshotModel] = get_inventory_product_snapshots(context, filters)
    
    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)
    
def test_gets_inventory_product_snapshots_with_paging() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: InventoryProductSnapshotModel = create_inventory_product_snapshot(context)
    posted_object_2: InventoryProductSnapshotModel = create_inventory_product_snapshot(context)
    
    sleep(1)
    
    posted_object_3: InventoryProductSnapshotModel = create_inventory_product_snapshot(context)
    posted_object_4: InventoryProductSnapshotModel = create_inventory_product_snapshot(context)

    filters_1: InventoryProductSnapshotSearchModel = InventoryProductSnapshotSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page = 1,
        page_length = 2
    )

    filters_2: InventoryProductSnapshotSearchModel = InventoryProductSnapshotSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page = 2,
        page_length = 2
    )
    
    result_page_1: PagedResponseItemList[InventoryProductSnapshotModel] = get_inventory_product_snapshots(context, filters_1)
    result_page_2: PagedResponseItemList[InventoryProductSnapshotModel] = get_inventory_product_snapshots(context, filters_2)

    ## Page 1

    assert result_page_1 is not None
    assert result_page_1.items is not None
    
    assert result_page_1.paging is not None
    assert result_page_1.paging.page == 1
    assert result_page_1.paging.page_length == 2
    assert result_page_1.paging.sort_by == 'created_at'
    assert result_page_1.paging.is_sort_descending == False

    posted_item_page_1_item_1: list[InventoryProductSnapshotModel] = [item for item in result_page_1.items if item.id == posted_object_1.id]
    assert len(posted_item_page_1_item_1) == 1  
    assert_objects_are_equal(posted_item_page_1_item_1[0], posted_object_1)

    posted_item_page_1_item_2: list[InventoryProductSnapshotModel] = [item for item in result_page_1.items if item.id == posted_object_2.id]
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
     
    posted_item_page_2_item_1: list[InventoryProductSnapshotModel] = [item for item in result_page_2.items if item.id == posted_object_3.id]
    assert len(posted_item_page_2_item_1) == 1  
    assert_objects_are_equal(posted_item_page_2_item_1[0], posted_object_3)

    posted_item_page_2_item_2: list[InventoryProductSnapshotModel] = [item for item in result_page_2.items if item.id == posted_object_4.id]
    assert len(posted_item_page_2_item_2) == 1  
    assert_objects_are_equal(posted_item_page_2_item_2[0], posted_object_4)
    
def test_getsinventory_product_snapshots_with_snapshot_hour_min_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(snapshot_hour = "2021-01-01T01:00:00.000Z"))
    posted_object_2: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(snapshot_hour = "2024-04-04T04:00:00.000Z"))
    posted_object_3: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(snapshot_hour = "2022-02-02T02:00:00.000Z"))
    posted_object_4: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(snapshot_hour = "2023-03-03T03:00:00.000Z"))

    filters: InventoryProductSnapshotSearchModel = InventoryProductSnapshotSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        snapshot_hour_min = "2023-03-03T03:00:00.000Z"
    )
    
    result: PagedResponseItemList[InventoryProductSnapshotModel] = get_inventory_product_snapshots(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 2
 
  
    posted_item_2: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2)

    posted_item_4: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)
    
def test_getsinventory_product_snapshots_with_snapshot_hour_min_and_max_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(snapshot_hour = "2021-01-01T01:00:00.000Z"))
    posted_object_2: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(snapshot_hour = "2024-04-04T04:00:00.000Z"))
    posted_object_3: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(snapshot_hour = "2022-02-02T02:00:00.000Z"))
    posted_object_4: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(snapshot_hour = "2023-03-03T03:00:00.000Z"))

    filters: InventoryProductSnapshotSearchModel = InventoryProductSnapshotSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        snapshot_hour_max = "2023-03-03T03:00:00.000Z",
        snapshot_hour_min = "2022-02-02T02:00:00.000Z",
    )
    
    result: PagedResponseItemList[InventoryProductSnapshotModel] = get_inventory_product_snapshots(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 2
 
    posted_item_3: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3) 

    posted_item_4: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)
    
def test_gets_inventory_product_snapshots_with_product_ids_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel( ))
    posted_object_2: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel( ))   
    posted_object_3: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(product_id = posted_object_1.product_id))
    posted_object_4: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel())
    
    filters: InventoryProductSnapshotSearchModel = InventoryProductSnapshotSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        product_ids = f"{posted_object_1.product_id},{posted_object_4.product_id}"
    )
    result: PagedResponseItemList[InventoryProductSnapshotModel] = get_inventory_product_snapshots(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)
      
def test_gets_inventory_intake_jobs_with_sku_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(sku = f"abcdef"))
    posted_object_2: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(sku = f"asdasdadsasd"))
    posted_object_3: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(sku = f"abcdef"))
    posted_object_4: InventoryProductSnapshotModel = create_inventory_product_snapshot(context, InventoryProductSnapshotCreateModel(sku = f"te4wrwerwer"))

    filters: InventoryProductSnapshotSearchModel = InventoryProductSnapshotSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        sku = f"abcdef"
    )
    
    result: PagedResponseItemList[InventoryProductSnapshotModel] = get_inventory_product_snapshots(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 2
    
    posted_item_1: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[InventoryProductSnapshotModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

         