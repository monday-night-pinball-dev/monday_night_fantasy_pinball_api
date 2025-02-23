from typing import Any

from tests.qdk.operators.inventory_intake_jobs import InventoryIntakeJobCreateModel, InventoryIntakeJobModel, InventoryIntakeJobUpdateModel, create_inventory_intake_job, inventory_intake_job_hydration_check, update_inventory_intake_job
from tests.qdk.qa_requests import qa_patch, qa_post
from tests.qdk.types import RequestOperators, TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_patches_invalid_inventory_intake_job_bad_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object: InventoryIntakeJobModel = create_inventory_intake_job(context)

    result = qa_patch(f"{context.api_url}/inventory_intake_jobs/{posted_object.id}", {
       'status' : 'not a valid status',
       'status_details' : 'not a valid json object'
    })
 
    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 2
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'status' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'enum'        
    assert error[0]['msg'] == "Input should be 'Requested', 'Processing', 'Complete' or 'Failed'"
 
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'status_details' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'dict_type'
    assert error[0]['msg'] == 'Input should be a valid dictionary'
  
def test_patches_valid_inventory_intake_job() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    random_string = generate_random_string(14)

    posted_object: InventoryIntakeJobModel = create_inventory_intake_job(context)  
 
    update_object: InventoryIntakeJobUpdateModel = InventoryIntakeJobUpdateModel(
        status = "Complete",
        status_details = {
            "another_key": "another_value"
        }
    )

    update_inventory_intake_job(context, posted_object.id or "", update_object)
     
def test_patches_valid_inventory_intake_job_with_hydration() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)
    
    posted_object: InventoryIntakeJobModel = create_inventory_intake_job(
        context,   
        InventoryIntakeJobCreateModel(
            create_parent_batch_job_if_null = True,
            create_simulator_response_if_null = True
        )
    )
 
    update_object: InventoryIntakeJobUpdateModel = InventoryIntakeJobUpdateModel(
        status = "Complete",
        status_details = {
            "another_key": "another_value"
        }
    )

    result = update_inventory_intake_job(context, posted_object.id or "", update_object, request_operators = RequestOperators(hydration_properties=["retailer_location", "retailer", "parent_batch_job", "simulator_response"]))
    
    inventory_intake_job_hydration_check(result)