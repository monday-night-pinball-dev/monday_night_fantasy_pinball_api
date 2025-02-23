from typing import Any

from tests.qdk.operators.pos_simulator_responses import create_pos_simulator_response 
from tests.qdk.qa_requests import qa_post
from tests.qdk.types import TestContext 
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_posts_invalid_pos_simulator_response_missing_fields() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/pos_simulator_responses", {

    })

    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 3
 
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'response_body' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'response_status_code' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'action_type' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'

def test_posts_invalid_pos_integration_bad_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/pos_simulator_responses", { 
        'response_body' : 'also very much not json',
        'response_status_code' : "not an integer",
        'action_type' : 'not a valid action type',
    })
 
    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 3
 
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'response_body' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'dict_type'
    assert error[0]['msg'] == 'Input should be a valid dictionary'

    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'response_status_code' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'int_parsing'
    assert error[0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'action_type' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'enum'
    assert error[0]['msg'] == "Input should be 'GetHistoricalSales' or 'GetInventorySnapshots'"
    
def test_posts_valid_pos_simulator_response() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    create_pos_simulator_response(context) 