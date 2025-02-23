from typing import Any

from tests.qdk.operators.inventory_product_snapshots import InventoryProductSnapshotCreateModel, create_inventory_product_snapshot, inventory_product_snapshot_hydration_check
from tests.qdk.operators.products import ProductCreateModel
from tests.qdk.qa_requests import qa_post
from tests.qdk.types import RequestOperators, TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_posts_invalid_inventory_product_snapshot_missing_fields() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/inventory_product_snapshots", {
 
    })

    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 6
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'retailer_location_id' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'product_id' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'snapshot_hour' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'sku' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'stock_on_hand' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'price' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
 

def test_posts_invalid_inventory_product_snapshot_bad_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/inventory_product_snapshots", {
        'retailer_location_id' : "not an id", 
        'product_id' : "not an id either", 
        'inventory_intake_job_id' : "never an id",
        'snapshot_hour' : 'not a valid datetime', 
        'sku' : generate_random_string(256),
        'stock_on_hand' : 'not a valid integer', 
        'price' : 'not a valid integer either',   
    })
 
    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 7
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'retailer_location_id' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'uuid_parsing'
    assert error[0]['msg'] == 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `n` at 1'
 
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'product_id' in error['loc']] 
    assert len(error) == 1
    assert error[0]['type'] == 'uuid_parsing'
    assert error[0]['msg'] == 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `n` at 1'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'inventory_intake_job_id' in error['loc']] 
    assert len(error) == 1
    assert error[0]['type'] == 'uuid_parsing'    
    assert error[0]['msg'] == 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `n` at 1'

    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'snapshot_hour' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'datetime_from_date_parsing'
    assert error[0]['msg'] == 'Input should be a valid datetime or date, invalid character in year'

    error: list[Any] = [error for error in errors['detail'] if  'body' in error['loc'] and 'sku' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 255 characters'  
 
    error: list[Any] = [error for error in errors['detail'] if  'body' in error['loc'] and 'stock_on_hand' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'int_parsing'
    assert error[0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'

    error: list[Any] = [error for error in errors['detail'] if  'body' in error['loc'] and 'price' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'int_parsing'
    assert error[0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'
    
def test_posts_valid_inventory_product_snapshot() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    create_inventory_product_snapshot(context)  
  
def test_posts_valid_inventory_product_snapshot() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = create_inventory_product_snapshot(
        context, 
        InventoryProductSnapshotCreateModel( 
            create_inventory_intake_job_if_null= True,
            product= ProductCreateModel(
                create_vendor_if_null= True
            )
        ),
        request_operators=RequestOperators(
            hydration_properties=["retailer_location", "retailer", "inventory_intake_job", "product", "vendor"]
        )
    )
    
    inventory_product_snapshot_hydration_check(result)
 
 