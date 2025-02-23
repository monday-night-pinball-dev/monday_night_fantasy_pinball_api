from typing import Any

from tests.qdk.operators.sales_intake_jobs import SalesIntakeJobCreateModel, create_sales_intake_job, sales_intake_job_hydration_check
from tests.qdk.qa_requests import qa_post
from tests.qdk.types import RequestOperators, TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_posts_invalid_sales_intake_job_missing_fields() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/sales_intake_jobs", { 
    })

    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 1
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'retailer_location_id' in error['loc']]       
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
 

def test_posts_invalid_sales_intake_job_bad_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/sales_intake_jobs", {
        'retailer_location_id' : "not an id", 
        'status_details' : 'not a valid json object',
        'status' : 'not a valid status'
    })
 
    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 3
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'retailer_location_id' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'uuid_parsing'
    assert error[0]['msg'] == 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `n` at 1'
  
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'status_details' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'dict_type'
    assert error[0]['msg'] == 'Input should be a valid dictionary'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'status' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'enum'
    assert error[0]['msg'] == "Input should be 'Requested', 'Processing', 'Complete' or 'Failed'"
    
def test_posts_valid_sales_intake_job() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    create_sales_intake_job(context)  
    
def test_posts_valid_sales_intake_job_defaulted_values() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    create_sales_intake_job(
        context,
        SalesIntakeJobCreateModel(status=None, status_details=None)
    )  
  
def test_posts_valid_sales_intake_job_with_hydration() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL) 
 
    created_sales_intake_job = create_sales_intake_job(
        context,
        SalesIntakeJobCreateModel(
            create_parent_batch_job_if_null=True
        ),
        request_operators=RequestOperators(hydration_properties=["retailer", "retailer_location", "parent_batch_job"])
    )
 
    assert created_sales_intake_job.retailer is not None
    assert created_sales_intake_job.retailer.id is not None
    assert created_sales_intake_job.retailer.id == created_sales_intake_job.retailer_id
    
    sales_intake_job_hydration_check(created_sales_intake_job)