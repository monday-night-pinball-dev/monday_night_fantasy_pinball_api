from typing import Any

from tests.qdk.operators.users import UserCreateModel, UserModel, UserUpdateModel, create_user, update_user
from tests.qdk.qa_requests import qa_patch, qa_post
from tests.qdk.types import TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_patches_invalid_user_bad_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object: UserModel = create_user(context)

    result = qa_patch(f"{context.api_url}/users/{posted_object.id}", {
        'first_name' : generate_random_string(256),
        'last_name':  generate_random_string(256),
        'role' : "not a role"
    }) 
 
    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 3
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'first_name' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 255 characters' 

    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'last_name' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 255 characters' 
      
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'role' in error['loc']]
    assert len(error) == 1    
    assert error[0]['type'] == 'enum'
    assert error[0]['msg'] == "Input should be 'SamsonAdmin', 'SamsonUser', 'RetailerAdmin', 'RetailerUser', 'RetailerManager', 'VendorAdmin' or 'VendorUser'"
  
def test_patches_valid_user() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    random_string = generate_random_string(14)

    posted_object: UserModel = create_user(context)  
 
    update_object: UserUpdateModel = UserUpdateModel(
        first_name = random_string + "_new_first_name",
        last_name = random_string + "_new_last_name",
        role = 'VendorUser',  
    )

    update_user(context, posted_object.id or "", update_object)
 