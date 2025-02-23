from typing import Any

from tests.qdk.operators.vendors import VendorCreateModel, create_vendor
from tests.qdk.qa_requests import qa_post
from tests.qdk.types import TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_posts_invalid_vendor_missing_fields() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/vendors", {})

    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 1
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'name' in error['loc']]

    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'

def test_posts_invalid_vendor_bad_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/vendors", {
        'name' : generate_random_string(256),
        'is_registered': 'not a bool',
        'unregistered_vendor_referring_retailer_location_id': 'not a valid id', 
        'hq_city' : generate_random_string(256),
        'hq_state' : generate_random_string(256),
        'hq_country' : generate_random_string(3),
        'account_status' : 'not an account status value',
        'contact_email' : 'this is obviously not an email man',
        'contact_phone' : 'ET phone home'
    })
 
    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 9
    
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
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'contact_phone' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'value_error'
    assert error[0]['msg'] == 'value is not a valid phone number'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'unregistered_vendor_referring_retailer_location_id' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'uuid_parsing'
    assert error[0]['msg'] == 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `n` at 1'
 
     
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'is_registered' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'bool_parsing'
    assert error[0]['msg'] == 'Input should be a valid boolean, unable to interpret input'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'account_status' in error['loc']]
    assert len(error) == 1    
    assert error[0]['type'] == 'enum'
    assert error[0]['msg'] == "Input should be 'Unregistered', 'RegisteredInactive', 'RegisteredActive', 'PausedByRequest', 'PausedByBilling' or 'Deactivated'"

def test_posts_valid_vendor() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    create_vendor(context, VendorCreateModel( 
        create_unregistered_vendor_referring_retailer_location_if_null= True
    ))  
 
 