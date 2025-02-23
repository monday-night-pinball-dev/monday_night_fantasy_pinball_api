from typing import Any

from tests.qdk.operators.vendors import VendorCreateModel, VendorModel, VendorUpdateModel, create_vendor, update_vendor
from tests.qdk.qa_requests import qa_patch, qa_post
from tests.qdk.types import TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_patches_invalid_vendor_bad_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object: VendorModel = create_vendor(context)

    result = qa_patch(f"{context.api_url}/vendors/{posted_object.id}", {
        'name' : generate_random_string(256),
        'is_registered': 'this is also not a boolean',  
        'contact_email' : "stillclearlynotavalidemaileventhoughithasan@init",
        'contact_phone' : "Then who was phone?",
        'hq_city' : generate_random_string(256),
        'hq_state' : generate_random_string(256),
        'hq_country' : generate_random_string(3), 
        'account_status' : 'random_invalid_value'
    }) 
 
    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 8
    
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
    assert error[0]['msg'] == 'value is not a valid email address: The part after the @-sign is not valid. It should have a period.'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'contact_phone' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'value_error'
    assert error[0]['msg'] == 'value is not a valid phone number'
     
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'is_registered' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'bool_parsing'
    assert error[0]['msg'] == 'Input should be a valid boolean, unable to interpret input'
      
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'account_status' in error['loc']]
    assert len(error) == 1    
    assert error[0]['type'] == 'enum'
    assert error[0]['msg'] == "Input should be 'Unregistered', 'RegisteredInactive', 'RegisteredActive', 'PausedByRequest', 'PausedByBilling' or 'Deactivated'"
  
def test_patches_valid_vendor() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    random_string = generate_random_string(14)

    posted_object: VendorModel = create_vendor(context)  
 
    update_object: VendorUpdateModel = VendorUpdateModel(
        name = random_string + "_name",
        is_registered = True, 
        hq_city = "new city",
        hq_state = "new state",
        hq_country = "NC",
        contact_email = "anotheraddress@example.com",
        contact_phone = '+12312312312',
        account_status='Deactivated'
    )

    update_vendor(context, posted_object.id or "", update_object)
 