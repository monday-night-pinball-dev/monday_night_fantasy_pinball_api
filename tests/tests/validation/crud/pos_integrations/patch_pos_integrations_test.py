from typing import Any

from tests.qdk.operators.pos_integrations import PosIntegrationCreateModel, PosIntegrationModel, PosIntegrationUpdateModel, create_pos_integration, pos_integration_hydration_check, update_pos_integration
from tests.qdk.qa_requests import qa_patch, qa_post
from tests.qdk.types import RequestOperators, TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_patches_invalid_pos_integration_bad_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object: PosIntegrationModel = create_pos_integration(context)

    result = qa_patch(f"{context.api_url}/pos_integrations/{posted_object.id}", {
        'name' : generate_random_string(256),
        'pos_platform' : "another invalid pos platform",
        'key' : generate_random_string(256), 
    })
 
    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 3
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'name' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 255 characters' 

    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'pos_platform' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'enum'
    assert error[0]['msg'] == "Input should be 'Posabit', 'Flowhub', 'Dutchie', 'KlickTrack', 'Cova', 'Meadow', 'GrowFlow' or 'Unknown'"
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'key' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 255 characters'  
  
def test_patches_valid_pos_integration() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    random_string = generate_random_string(14)

    posted_object: PosIntegrationModel = create_pos_integration(context)  
 
    update_object: PosIntegrationUpdateModel = PosIntegrationUpdateModel(
        name = random_string + "_name",
        description = "describe away my main man",
        pos_platform = "Posabit",
        key = "09876543212qwertyuiop",
        url = "nowhere.example.net"
    )

    update_pos_integration(context, posted_object.id or "", update_object) 
    
def test_patches_valid_pos_integration_with_hydration() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    random_string = generate_random_string(14)

    posted_object: PosIntegrationModel = create_pos_integration(context)  
 
    update_object: PosIntegrationUpdateModel = PosIntegrationUpdateModel(
        name = random_string + "_name",
        description = "describe away my main man",
        pos_platform = "Posabit",
        key = "09876543212qwertyuiop",
        url = "nowhere.example.net"
    )

    result = update_pos_integration(
        context, 
        posted_object.id or "", 
        update_object,
        request_operators=RequestOperators(hydration_properties=["retailer,retailer_location,retailer_location.retailer"])
    )
    
    pos_integration_hydration_check(result)
 