from typing import Any

from tests.qdk.operators.retailers import RetailerCreateModel, create_retailer
from tests.qdk.qa_requests import qa_post
from tests.qdk.types import TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_posts_invalid_retailer_missing_fields() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/retailers", {})

    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 1
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'name' in error['loc']]

    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'

def test_posts_invalid_retailer_bad_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/retailers", {
        'name' : generate_random_string(256),
        'hq_city' : generate_random_string(256),
        'hq_state' : generate_random_string(256),
        'hq_country' : generate_random_string(3),
        'contact_email' : 'this is obviously not an email man',
        'account_status' : 'a very invalid status'
    })
 
    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 6
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'name' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 255 characters' 

    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'hq_city' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 255 characters' 

    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'hq_state' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 255 characters' 

    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'hq_country' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 2 characters' 

    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'contact_email' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'value_error'
    assert error[0]['msg'] == 'value is not a valid email address: An email address must have an @-sign.'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'account_status' in error['loc']]
    assert len(error) == 1    
    assert error[0]['type'] == 'enum'
    assert error[0]['msg'] == "Input should be 'Unregistered', 'RegisteredInactive', 'RegisteredActive', 'PausedByRequest', 'PausedByBilling' or 'Deactivated'"

def test_posts_valid_retailer() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    create_retailer(context)  
 
 