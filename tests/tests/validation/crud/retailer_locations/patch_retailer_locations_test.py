from typing import Any

from tests.qdk.operators.pos_integrations import PosIntegrationCreateModel, create_pos_integration
from tests.qdk.operators.retailer_locations import RetailerLocationCreateModel, RetailerLocationModel, RetailerLocationUpdateModel, create_retailer_location, retailer_location_hydration_check, update_retailer_location
from tests.qdk.qa_requests import qa_patch, qa_post
from tests.qdk.types import RequestOperators, TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_posts_invalid_retailer_location_bad_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object: RetailerLocationModel = create_retailer_location(context)

    result = qa_patch(f"{context.api_url}/retailer_locations/{posted_object.id}", {
        'name' : generate_random_string(256),
        'retailer_id' : "patching not an id", 
        'contact_email' : "patching not an email", 
        'contact_phone' : "patching not a phone", 
        'location_city' : generate_random_string(256),
        'location_state' : generate_random_string(256),
        'location_country' : generate_random_string(3),
        'account_status' : 'patch it up with invalid garbage'
    })
 
    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 7
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'name' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 255 characters'   
 
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
 
def test_patches_valid_retailer_location() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    random_string = generate_random_string(14)

    posted_object: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel())
       
    update_object: RetailerLocationUpdateModel = RetailerLocationUpdateModel( 
        name = random_string + '_name', 
        location_city = 'patchville',
        location_state = 'north new patchplace',
        location_country = 'PP',
        contact_email = 'madeupemailaddrepatchyss@example.com', 
        contact_phone = '+12345612345',
        account_status = 'Deactivated'
    )

    update_retailer_location(context, posted_object.id or "", update_object)
    
def test_patches_valid_retailer_location_with_hydration() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    random_string = generate_random_string(14)

    posted_object: RetailerLocationModel = create_retailer_location(context, RetailerLocationCreateModel())
       
    update_object: RetailerLocationUpdateModel = RetailerLocationUpdateModel( 
        name = random_string + '_name', 
        location_city = 'patchville',
        location_state = 'north new patchplace',
        location_country = 'PP',
        contact_email = 'madeupemailaddrepatchyss@example.com', 
        contact_phone = '+12345612345',
        account_status = 'Deactivated'
    )
 
    updated_retailer_location = update_retailer_location(
        context, 
        posted_object.id or "", 
        update_object, 
        request_operators=RequestOperators(hydration_properties=["retailer"]))
     
    retailer_location_hydration_check(updated_retailer_location)
 