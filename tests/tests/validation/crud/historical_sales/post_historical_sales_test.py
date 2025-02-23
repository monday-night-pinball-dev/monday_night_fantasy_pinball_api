from typing import Any

from tests.qdk.operators.historical_sales import HistoricalSaleCreateModel, create_historical_sale, historical_sale_hydration_check
from tests.qdk.qa_requests import qa_post
from tests.qdk.types import RequestOperators, TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_posts_invalid_historical_sale_missing_fields() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/historical_sales", {
 
    })

    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 4
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'retailer_location_id' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
     
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'sale_timestamp' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'pos_sale_id' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
  
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'total' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'missing'
    assert error[0]['msg'] == 'Field required'
 

def test_posts_invalid_historical_sale_bad_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/historical_sales", {
        'retailer_location_id' : "not an id",  
        'sales_intake_job_id' : "never an id",
        'sale_timestamp' : 'not a valid datetime',
        'pos_sale_id' : generate_random_string(256), 
        'total' : 'not a valid integer', 
        'sub_total' : 'not a valid integer either',
        'discount' : 'also not a valid integer',
        'tax' : 'still not a valid integer',
        'cost' : 'will it ever be a valid integer',
        
    })
 
    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 9
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'retailer_location_id' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'uuid_parsing'
    assert error[0]['msg'] == 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `n` at 1'

    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'sales_intake_job_id' in error['loc']] 
    assert len(error) == 1
    assert error[0]['type'] == 'uuid_parsing'    
    assert error[0]['msg'] == 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `n` at 1'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'sale_timestamp' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'datetime_from_date_parsing' 
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'pos_sale_id' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 255 characters'  
  
    error: list[Any] = [error for error in errors['detail'] if  'body' in error['loc'] and 'total' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'int_parsing'
    assert error[0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'
    
    error: list[Any] = [error for error in errors['detail'] if  'body' in error['loc'] and 'sub_total' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'int_parsing'
    assert error[0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'

    error: list[Any] = [error for error in errors['detail'] if  'body' in error['loc'] and 'discount' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'int_parsing'
    assert error[0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'

    error: list[Any] = [error for error in errors['detail'] if  'body' in error['loc'] and 'tax' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'int_parsing'
    assert error[0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'
    
    error: list[Any] = [error for error in errors['detail'] if  'body' in error['loc'] and 'cost' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'int_parsing'
    assert error[0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'
    
def test_posts_valid_historical_sale() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    create_historical_sale(
        context=context, 
        overrides = HistoricalSaleCreateModel(
            create_sales_intake_job_if_null=True
        )
    )

def test_posts_valid_historical_sale_with_hydration() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    result = create_historical_sale(
        context=context, 
        overrides = HistoricalSaleCreateModel(
            create_sales_intake_job_if_null=True
        ), 
        request_operators=RequestOperators(
            hydration_properties=["retailer_location", "retailer", "sales_intake_job"]
        )
    )
    
    historical_sale_hydration_check(result)
 
 