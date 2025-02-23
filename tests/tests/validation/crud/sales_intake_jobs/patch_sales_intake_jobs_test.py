from typing import Any

from tests.qdk.operators.sales_intake_jobs import SalesIntakeJobCreateModel, SalesIntakeJobModel, SalesIntakeJobUpdateModel, create_sales_intake_job, sales_intake_job_hydration_check, update_sales_intake_job
from tests.qdk.qa_requests import qa_patch, qa_post
from tests.qdk.types import RequestOperators, TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_patches_invalid_sales_intake_job_bad_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object: SalesIntakeJobModel = create_sales_intake_job(context)

    result = qa_patch(f"{context.api_url}/sales_intake_jobs/{posted_object.id}", {
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
  
def test_patches_valid_sales_intake_job() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    random_string = generate_random_string(14)

    posted_object: SalesIntakeJobModel = create_sales_intake_job(context)  
 
    update_object: SalesIntakeJobUpdateModel = SalesIntakeJobUpdateModel(
        status = "Complete",
        status_details = {
            "another_key": "another_value"
        }
    )

    update_sales_intake_job(context, posted_object.id or "", update_object)
    
def test_patches_valid_sales_intake_job_with_hydration() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    random_string = generate_random_string(14)

    posted_object: SalesIntakeJobModel = create_sales_intake_job(context, SalesIntakeJobCreateModel(create_parent_batch_job_if_null= True))
 
    update_object: SalesIntakeJobUpdateModel = SalesIntakeJobUpdateModel(
        status = "Complete",
        status_details = {
            "another_key": "another_value"
        }
    )

    updated = update_sales_intake_job(context, posted_object.id or "", update_object, request_operators=RequestOperators(hydration_properties=["retailer", "retailer_location", "parent_batch_job"]))
    
    sales_intake_job_hydration_check(updated)
 