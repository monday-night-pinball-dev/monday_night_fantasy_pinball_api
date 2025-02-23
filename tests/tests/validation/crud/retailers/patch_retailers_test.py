from typing import Any

from tests.qdk.operators.retailers import RetailerCreateModel, RetailerModel, RetailerUpdateModel, create_retailer, update_retailer
from tests.qdk.qa_requests import qa_patch, qa_post
from tests.qdk.types import TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_patches_invalid_retailer_bad_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object: RetailerModel = create_retailer(context)

    result = qa_patch(f"{context.api_url}/retailers/{posted_object.id}", {
        'name' : generate_random_string(256),
        'contact_email' : "stillclearlynotavalidemaileventhoughithasan@init",
        'hq_city' : generate_random_string(256),
        'hq_state' : generate_random_string(256),
        'hq_country' : generate_random_string(3), 
        'account_status' : 'this is not a valid account status'
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
    assert error[0]['msg'] == 'value is not a valid email address: The part after the @-sign is not valid. It should have a period.'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'account_status' in error['loc']]
    assert len(error) == 1    
    assert error[0]['type'] == 'enum'
    assert error[0]['msg'] == "Input should be 'Unregistered', 'RegisteredInactive', 'RegisteredActive', 'PausedByRequest', 'PausedByBilling' or 'Deactivated'"
  
def test_patches_valid_retailer() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    random_string = generate_random_string(14)

    posted_object: RetailerModel = create_retailer(context)  
 
    update_object: RetailerUpdateModel = RetailerUpdateModel(
        name = random_string + "_name",
        hq_city = "new city",
        hq_state = "new state",
        hq_country = "NC",
        contact_email = "anotheraddress@example.com",
        account_status= "Deactivated"
    )

    update_retailer(context, posted_object.id or "", update_object)
 