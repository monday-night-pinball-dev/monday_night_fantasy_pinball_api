from typing import Any

from tests.qdk.operators.inventory_intake_jobs import InventoryIntakeJobCreateModel, create_inventory_intake_job, inventory_intake_job_hydration_check
from tests.qdk.qa_requests import qa_post
from tests.qdk.types import RequestOperators, TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_posts_invalid_inventory_intake_job_missing_fields() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/inventory_intake_jobs", {
 
    })

    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 2
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'retailer_location_id' in error['loc']]       
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'snapshot_hour' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
  

def test_posts_invalid_inventory_intake_job_bad_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/inventory_intake_jobs", {
        'retailer_location_id' : "not an id", 
        'snapshot_hour' : 'not a valid time', 
        'status_details' : 'not a valid json object',
        'status' : 'not a valid status'
    })
 
    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 4
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'retailer_location_id' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'uuid_parsing'
    assert error[0]['msg'] == 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `n` at 1'
 
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'snapshot_hour' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'datetime_from_date_parsing'
    assert error[0]['msg'] == 'Input should be a valid datetime or date, invalid character in year'

    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'status_details' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'dict_type'
    assert error[0]['msg'] == 'Input should be a valid dictionary'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'status' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'enum'
    assert error[0]['msg'] == "Input should be 'Requested', 'Processing', 'Complete' or 'Failed'"
    
def test_posts_valid_inventory_intake_job() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    create_inventory_intake_job(context)  

def test_posts_valid_inventory_intake_job_with_hydration() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = create_inventory_intake_job(
        context,
        InventoryIntakeJobCreateModel(
            create_parent_batch_job_if_null=True,
            create_simulator_response_if_null=True
        ),
        request_operators=RequestOperators(
            hydration_properties=["retailer_location", "retailer", "parent_batch_job", "simulator_response"]
        )
    )  
    
    inventory_intake_job_hydration_check(result)
    
def test_posts_valid_inventory_intake_job_defaulted_values() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    create_inventory_intake_job(
        context,
        InventoryIntakeJobCreateModel(status=None, status_details=None)
    )  
 
 