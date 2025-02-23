from typing import Any

from tests.qdk.operators.retailer_locations import RetailerLocationCreateModel, create_retailer_location, retailer_location_hydration_check 
from tests.qdk.qa_requests import qa_post
from tests.qdk.types import RequestOperators, TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_posts_invalid_retailer_location_missing_fields() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/retailer_locations", {})

    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 2
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'name' in error['loc']]

    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'

    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'retailer_id' in error['loc']]

    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'

def test_posts_invalid_retailer_location_bad_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/retailer_locations", {
        'name' : generate_random_string(256),
        'retailer_id' : "not an id",  
        'contact_email' : "not an email", 
        'contact_phone' : "not a phone", 
        'location_city' : generate_random_string(256),
        'location_state' : generate_random_string(256),
        'location_country' : generate_random_string(3),
        'account_status' : "invalid statoos"
    })
 
    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 8
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'name' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 255 characters'   

    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'retailer_id' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'uuid_parsing'
    assert error[0]['msg'] == 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `n` at 1'
 
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'contact_email' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'value_error'
    assert error[0]['msg'] == 'value is not a valid email address: An email address must have an @-sign.'
 
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'contact_phone' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'value_error'
    assert error[0]['msg'] == 'value is not a valid phone number'

    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'location_city' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 255 characters' 

    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'location_state' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 255 characters' 

    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'location_country' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 2 characters' 
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'account_status' in error['loc']]
    assert len(error) == 1    
    assert error[0]['type'] == 'enum'
    assert error[0]['msg'] == "Input should be 'Unregistered', 'RegisteredInactive', 'RegisteredActive', 'PausedByRequest', 'PausedByBilling' or 'Deactivated'"
 
    
def test_posts_valid_retailer_location() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)
 
    create_retailer_location(context)
  
def test_posts_valid_retailer_location_with_hydration() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL) 
 
    created_retailer_location = create_retailer_location(
        context,
        None,
        request_operators=RequestOperators(hydration_properties=["retailer"])
    )
 
    assert created_retailer_location.retailer is not None
    assert created_retailer_location.retailer.id is not None
    assert created_retailer_location.retailer.id == created_retailer_location.retailer_id
    
    retailer_location_hydration_check(created_retailer_location)