from typing import Any

from tests.qdk.operators.pos_integrations import PosIntegrationCreateModel, create_pos_integration
from tests.qdk.operators.products import ProductCreateModel, ProductModel, ProductUpdateModel, create_product, product_hydration_check, update_product
from tests.qdk.operators.vendors import VendorModel, create_vendor
from tests.qdk.qa_requests import qa_patch, qa_post
from tests.qdk.types import RequestOperators, TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_posts_invalid_product_bad_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object: ProductModel = create_product(context)

    result = qa_patch(f"{context.api_url}/products/{posted_object.id}", {
        'name' : generate_random_string(256),
        'vendor_sku'   : generate_random_string(256), 
        'vendor_id' : "not an id either",
        'confirmed_core_product_id' : "not an id at all",
        'vendor_confirmation_status' : "not a status" 
    })
 
    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 5
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'name' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 255 characters'   
  
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'vendor_sku' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'string_too_long'
    assert error[0]['msg'] == 'String should have at most 255 characters' 

    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'vendor_id' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'uuid_parsing'
    assert error[0]['msg'] == 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `n` at 1'

    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'confirmed_core_product_id' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'uuid_parsing'
    assert error[0]['msg'] == 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `n` at 1'
    
    error: list[Any] = [error for error in errors['detail'] if 'body' in error['loc'] and 'vendor_confirmation_status' in error['loc']]
    assert len(error) == 1    
    assert error[0]['type'] == 'enum'
    assert error[0]['msg'] == "Input should be 'Candidate', 'ConfirmedByVendor', 'DeniedByVendor', 'Discontinued' or 'Unknown'"
 
def test_patches_valid_product() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    random_string = generate_random_string(14)

    posted_object: ProductModel = create_product(context, ProductCreateModel(
        create_confirmed_core_product_if_null= True,
        create_referring_retailer_location_if_null= True,
        create_vendor_if_null= True
    
    ))
    
    # new vendor id
    posted_vendor: VendorModel = create_vendor(context)
    
    # new confirmed_product id
    posted_product: ProductModel = create_product(context) 
       
    update_object: ProductUpdateModel = ProductUpdateModel( 
        name = random_string + '_name', 
        vendor_sku = random_string + '_vendor_sku',
        vendor_confirmation_status = 'ConfirmedByVendor',
        confirmed_core_product_id = posted_product.id,
        vendor_id = posted_vendor.id
    )

    update_product(context, posted_object.id or "", update_object)
 
 
def test_patches_valid_product_with_hydration() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    random_string = generate_random_string(14)

    posted_object: ProductModel = create_product(context, ProductCreateModel(
        create_confirmed_core_product_if_null= True,
        create_referring_retailer_location_if_null= True,
        create_vendor_if_null= True 
    ))
    
    # new vendor id
    posted_vendor: VendorModel = create_vendor(context)
    
    # new confirmed_product id
    posted_product: ProductModel = create_product(context, ProductCreateModel(
        create_confirmed_core_product_if_null= True,
        create_referring_retailer_location_if_null= True,
        create_vendor_if_null= True 
    ))
       
    update_object: ProductUpdateModel = ProductUpdateModel( 
        name = random_string + '_name', 
        vendor_sku = random_string + '_vendor_sku',
        vendor_confirmation_status = 'ConfirmedByVendor',
        confirmed_core_product_id = posted_product.id,
        vendor_id = posted_vendor.id
    )

    updated_object = update_product(context, posted_object.id or "", update_object, request_operators=RequestOperators(hydration_properties=["referring_retailer", "referring_retailer_location", "vendor", "confirmed_core_product"]))
    
    product_hydration_check(updated_object)
 