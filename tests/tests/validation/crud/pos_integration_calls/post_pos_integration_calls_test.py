from typing import Any

from tests.qdk.operators.pos_integration_calls import PosIntegrationCallCreateModel, create_pos_integration_call, pos_integration_call_hydration_check
from tests.qdk.operators.pos_integrations import PosIntegrationCreateModel, create_pos_integration
from tests.qdk.qa_requests import qa_post
from tests.qdk.types import RequestOperators, TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_posts_invalid_pos_integration_call_missing_fields() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/pos_integration_calls", {

    })

    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 4
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'request' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'response' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'response_status_code' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'pos_integration_id' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'

def test_posts_invalid_pos_integration_bad_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/pos_integration_calls", {
        'request' : "this is not json at all", 
        'response' : 'also very much not json',
        'response_status_code' : "not an integer",
        'pos_integration_id' : 'not an id' 
    })
 
    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 4
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'request' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'dict_type'
    assert error[0]['msg'] == 'Input should be a valid dictionary'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'response' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'dict_type'
    assert error[0]['msg'] == 'Input should be a valid dictionary'

    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'response_status_code' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'int_parsing'
    assert error[0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'pos_integration_id' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'uuid_parsing'
    assert error[0]['msg'] == 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `n` at 1'

def test_posts_valid_pos_integration_call() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    create_pos_integration_call(context)  
 
def test_posts_valid_pos_integration_call_with_hydration() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = create_pos_integration_call(
        context,
        None,
        request_operators = RequestOperators(hydration_properties=["retailer", "retailer_location", "pos_integration"]))
    
    pos_integration_call_hydration_check(result)
 

