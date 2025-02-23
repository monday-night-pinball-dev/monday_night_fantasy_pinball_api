from typing import Any
 
from tests.qdk.qa_requests import qa_post
from tests.qdk.types import TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 
from tests.qdk.operators.sales_intake_batch_jobs import SalesIntakeBatchJobCreateModel, create_sales_intake_batch_job

def test_posts_invalid_sales_intake_batch_job_bad_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/sales_intake_batch_jobs", {
         
        'status_details' : 'not a valid json object',
        'status' : 'not a valid status', 
        'restricted_retailer_location_ids' : 'not an id,also not an id',
    })
 
    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 3
  
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'restricted_retailer_location_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'
    assert error[0]['msg'] == f"Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: not an id,\n\t1: also not an id\n]."
 

    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'status_details' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'dict_type'
    assert error[0]['msg'] == 'Input should be a valid dictionary'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'status' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'enum'
    assert error[0]['msg'] == "Input should be 'Requested', 'Processing', 'Complete' or 'Failed'"
    
def test_posts_invalid_sales_intake_batch_job_bad_inputs_list_ids() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/sales_intake_batch_jobs", { 
        'restricted_retailer_location_ids' : ['not an id','also not an id'],
    })
 
    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 1

    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'restricted_retailer_location_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'
    assert error[0]['msg'] == f"Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: not an id,\n\t1: also not an id\n]."
   
def test_posts_valid_sales_intake_batch_job() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    create_sales_intake_batch_job(context)  
    
def test_posts_valid_sales_intake_batch_job_defaulted_values() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    create_sales_intake_batch_job(
        context,
        SalesIntakeBatchJobCreateModel(status=None, status_details=None)
    )  
 
 