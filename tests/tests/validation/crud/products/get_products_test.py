from time import sleep
from typing import Any

from tests.qdk.operators.products import ProductCreateModel, ProductModel, ProductSearchModel, create_product, get_product_by_id, get_products, product_hydration_check
from tests.qdk.qa_requests import qa_get, qa_post
from tests.qdk.types import PagedResponseItemList, RequestOperators, TestContext
from tests.qdk.utils import assert_objects_are_equal, generate_random_string
from urllib.parse import urlencode   
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_gets_product_by_id() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object = create_product(context)

    result = get_product_by_id(context, posted_object.id)

    assert result is not None
    assert result.id == posted_object.id
    
def test_gets_product_by_id_with_hydration() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object = create_product(context, ProductCreateModel(
        create_confirmed_core_product_if_null= True,
        create_referring_retailer_location_if_null= True,
        create_vendor_if_null= True 
    ))

    result = get_product_by_id(context, posted_object.id, request_operators = RequestOperators(hydration_properties=["referring_retailer", "referring_retailer_location", "vendor", "confirmed_core_product"]))

    assert result is not None
    assert result.id == posted_object.id
    
    product_hydration_check(result)

def test_gets_products_invalid_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)
     
    result = qa_get(f"{context.api_url}/products", query_params={
        'ids': 'not an id,also not an id',
        'referring_retailer_ids': 'not valid,at all,cmon man', 
        'referring_retailer_location_ids': 'invalid,id,jamboree',
        'vendor_ids': 'not valid either',
        'confirmed_core_product_ids': 'invalidids',
        'vendor_confirmation_status' : 'not a valid status',
        'page' : 'not a page num',
        'page_length' : 'not a length num',
        'is_sort_descending' : 'not a bool'
    })

    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 9
    
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: not an id,\n\t1: also not an id\n].'

    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'referring_retailer_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: not valid,\n\t1: at all,\n\t2: cmon man\n].'
     
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'referring_retailer_location_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: invalid,\n\t1: id,\n\t2: jamboree\n].'
    
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'vendor_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: not valid either\n].'
     
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'confirmed_core_product_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: invalidids\n].'
    
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'vendor_confirmation_status' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'enum'
    assert error[0]['msg'] =="Input should be 'Candidate', 'ConfirmedByVendor', 'DeniedByVendor', 'Discontinued' or 'Unknown'"
     
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'page' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'int_parsing'
    assert error[0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'
 
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'page_length' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'int_parsing'
    assert error[0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'

    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'is_sort_descending' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'bool_parsing'
    assert error[0]['msg'] == 'Input should be a valid boolean, unable to interpret input'

def test_gets_products_with_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: ProductModel = create_product(context)
    posted_object_2: ProductModel = create_product(context)
    posted_object_3: ProductModel = create_product(context)
    posted_object_4: ProductModel = create_product(context)

    filters: ProductSearchModel = ProductSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )
    
    result: PagedResponseItemList[ProductModel] = get_products(context, filters)

    assert result is not None
    assert result.items is not None
    
    assert result.paging is not None
    assert result.paging.page == 1
    assert result.paging.page_length == 25
    assert result.paging.sort_by == 'created_at'
    assert result.paging.is_sort_descending == False

    assert len(result.items) == 4 
    
    posted_item_1: list[ProductModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1, ["referring_retailer_id", "referring_retailer"])

    posted_item_2: list[ProductModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2, ["referring_retailer_id", "referring_retailer"])
  
    posted_item_3: list[ProductModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3, ["referring_retailer_id", "referring_retailer"])
  
    posted_item_4: list[ProductModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4, ["referring_retailer_id", "referring_retailer"])
    
def test_gets_products_with_ids_filter() -> None:
        
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: ProductModel = create_product(context, ProductCreateModel(
        create_confirmed_core_product_if_null= True,
        create_referring_retailer_location_if_null= True,
        create_vendor_if_null= True 
    ))
    posted_object_2: ProductModel = create_product(context, ProductCreateModel(
        create_confirmed_core_product_if_null= True,
        create_referring_retailer_location_if_null= True,
        create_vendor_if_null= True 
    ))
    posted_object_3: ProductModel = create_product(context, ProductCreateModel(
        create_confirmed_core_product_if_null= True,
        create_referring_retailer_location_if_null= True,
        create_vendor_if_null= True 
    ))
    posted_object_4: ProductModel = create_product(context, ProductCreateModel(
        create_confirmed_core_product_if_null= True,
        create_referring_retailer_location_if_null= True,
        create_vendor_if_null= True 
    ))

    filters: ProductSearchModel = ProductSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )
    
    result: PagedResponseItemList[ProductModel] = get_products(context, filters, request_operators = RequestOperators(hydration_properties=["referring_retailer", "referring_retailer_location", "vendor", "confirmed_core_product"]))

    assert result is not None
    assert result.items is not None
    
    assert result.paging is not None
    assert result.paging.page == 1
    assert result.paging.page_length == 25
    assert result.paging.sort_by == 'created_at'
    assert result.paging.is_sort_descending == False

    assert len(result.items) == 4 
    
    posted_item_1: list[ProductModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1, ["referring_retailer", "vendor", "confirmed_core_product", "referring_retailer_location"])
    
    product_hydration_check(posted_item_1[0])

    posted_item_2: list[ProductModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2, ["referring_retailer", "vendor", "confirmed_core_product", "referring_retailer_location"])
    
    product_hydration_check(posted_item_2[0])
  
    posted_item_3: list[ProductModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3, ["referring_retailer", "vendor", "confirmed_core_product", "referring_retailer_location"])
    
    product_hydration_check(posted_item_3[0])
  
    posted_item_4: list[ProductModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4, ["referring_retailer", "vendor", "confirmed_core_product", "referring_retailer_location"])
    
    product_hydration_check(posted_item_4[0])

def test_gets_products_with_paging() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: ProductModel = create_product(context)
    posted_object_2: ProductModel = create_product(context)
    
    sleep(1)
    
    posted_object_3: ProductModel = create_product(context)
    posted_object_4: ProductModel = create_product(context)

    filters_1: ProductSearchModel = ProductSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page = 1,
        page_length = 2
    )

    filters_2: ProductSearchModel = ProductSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page = 2,
        page_length = 2
    )
    
    result_page_1: PagedResponseItemList[ProductModel] = get_products(context, filters_1)
    result_page_2: PagedResponseItemList[ProductModel] = get_products(context, filters_2)

    ## Page 1

    assert result_page_1 is not None
    assert result_page_1.items is not None
    
    assert result_page_1.paging is not None
    assert result_page_1.paging.page == 1
    assert result_page_1.paging.page_length == 2
    assert result_page_1.paging.sort_by == 'created_at'
    assert result_page_1.paging.is_sort_descending == False

    posted_item_page_1_item_1: list[ProductModel] = [item for item in result_page_1.items if item.id == posted_object_1.id]
    assert len(posted_item_page_1_item_1) == 1  
    assert_objects_are_equal(posted_item_page_1_item_1[0], posted_object_1)

    posted_item_page_1_item_2: list[ProductModel] = [item for item in result_page_1.items if item.id == posted_object_2.id]
    assert len(posted_item_page_1_item_2) == 1  
    assert_objects_are_equal(posted_item_page_1_item_2[0], posted_object_2)
   
    ## Page 2

    assert result_page_2 is not None
    assert result_page_2.items is not None
    
    assert result_page_2.paging is not None
    assert result_page_2.paging.page == 2
    assert result_page_2.paging.page_length == 2
    assert result_page_2.paging.sort_by == 'created_at'
    assert result_page_2.paging.is_sort_descending == False

    assert len(result_page_1.items) == 2
     
    posted_item_page_2_item_1: list[ProductModel] = [item for item in result_page_2.items if item.id == posted_object_3.id]
    assert len(posted_item_page_2_item_1) == 1  
    assert_objects_are_equal(posted_item_page_2_item_1[0], posted_object_3)

    posted_item_page_2_item_2: list[ProductModel] = [item for item in result_page_2.items if item.id == posted_object_4.id]
    assert len(posted_item_page_2_item_2) == 1  
    assert_objects_are_equal(posted_item_page_2_item_2[0], posted_object_4)
  
def test_gets_products_with_name_exact_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)
    
    matching_random_string = generate_random_string(16)

    posted_object_1: ProductModel = create_product(context, ProductCreateModel(name = f"prefix-{matching_random_string}-matches"))
    posted_object_2: ProductModel = create_product(context, ProductCreateModel(name = f"{matching_random_string}-matches"))
    posted_object_3: ProductModel = create_product(context, ProductCreateModel(name = f"{matching_random_string}-matches-suffix"))
    posted_object_4: ProductModel = create_product(context, ProductCreateModel(name = f"prefix-{matching_random_string}-matches-suffix"))

    filters: ProductSearchModel = ProductSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        name = f"{matching_random_string}-matches"
    )
    
    result: PagedResponseItemList[ProductModel] = get_products(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 1
     
    posted_item_2: list[ProductModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2) 
    
def test_gets_products_with_vendor_ids_filter() -> None:    
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: ProductModel = create_product(context, ProductCreateModel(create_vendor_if_null=True))
    posted_object_2: ProductModel = create_product(context, ProductCreateModel(create_vendor_if_null=True))
    posted_object_3: ProductModel = create_product(context, ProductCreateModel(vendor_id = posted_object_1.vendor_id))
    posted_object_4: ProductModel = create_product(context, ProductCreateModel(create_vendor_if_null=True))

    filters: ProductSearchModel = ProductSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        vendor_ids = f"{posted_object_1.vendor_id},{posted_object_4.vendor_id}"
    )
    
    result: PagedResponseItemList[ProductModel] = get_products(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[ProductModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[ProductModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[ProductModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)
    
def test_gets_products_with_confirmed_core_product_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: ProductModel = create_product(context, ProductCreateModel(create_confirmed_core_product_if_null=True))
    posted_object_2: ProductModel = create_product(context, ProductCreateModel(create_confirmed_core_product_if_null=True))
    posted_object_3: ProductModel = create_product(context, ProductCreateModel(confirmed_core_product_id = posted_object_1.confirmed_core_product_id))
    posted_object_4: ProductModel = create_product(context, ProductCreateModel(create_confirmed_core_product_if_null=True))

    filters: ProductSearchModel = ProductSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        confirmed_core_product_ids = f"{posted_object_1.confirmed_core_product_id},{posted_object_4.confirmed_core_product_id}"
    )
    
    result: PagedResponseItemList[ProductModel] = get_products(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[ProductModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[ProductModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[ProductModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)
    
def test_gets_products_with_vendor_confirmation_status_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: ProductModel = create_product(context, ProductCreateModel(vendor_confirmation_status = "Candidate"))
    posted_object_2: ProductModel = create_product(context, ProductCreateModel(vendor_confirmation_status = "ConfirmedByVendor"))
    posted_object_3: ProductModel = create_product(context, ProductCreateModel(vendor_confirmation_status = "Candidate"))
    posted_object_4: ProductModel = create_product(context, ProductCreateModel(vendor_confirmation_status = "Discontinued")) 
    
    filters: ProductSearchModel = ProductSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        vendor_confirmation_status = "Candidate"
    )
    
    result: PagedResponseItemList[ProductModel] = get_products(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 2
    
    posted_item_1: list[ProductModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[ProductModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)
    
    
def test_gets_products_with_name_like_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)
    
    matching_random_string = generate_random_string(16).upper()
    non_matching_random_string = generate_random_string(16)

    posted_object_1: ProductModel = create_product(context, ProductCreateModel(name = f"prefix-{matching_random_string}-suffix"))
    posted_object_2: ProductModel = create_product(context, ProductCreateModel(name = f"{matching_random_string}-suffix"))
    posted_object_3: ProductModel = create_product(context, ProductCreateModel(name = f"not a match-{non_matching_random_string}"))
    posted_object_4: ProductModel = create_product(context, ProductCreateModel(name = f"prefix-{matching_random_string}"))

    filters: ProductSearchModel = ProductSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        name_like = f"{matching_random_string.lower()}"
    )
    
    result: PagedResponseItemList[ProductModel] = get_products(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3 
    
    posted_item_1: list[ProductModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1)

    posted_item_2: list[ProductModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2)
  
    posted_item_4: list[ProductModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)


def test_gets_products_with_referring_retailer_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: ProductModel = create_product(context, ProductCreateModel(create_referring_retailer_location_if_null=True))
    posted_object_2: ProductModel = create_product(context, ProductCreateModel(create_referring_retailer_location_if_null=True))
    posted_object_3: ProductModel = create_product(context, ProductCreateModel(referring_retailer_location_id = posted_object_1.referring_retailer_location_id))
    posted_object_4: ProductModel = create_product(context, ProductCreateModel(create_referring_retailer_location_if_null=True))

    filters: ProductSearchModel = ProductSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        referring_retailer_ids = f"{posted_object_1.referring_retailer_id},{posted_object_4.referring_retailer_id}"
    )
    
    result: PagedResponseItemList[ProductModel] = get_products(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[ProductModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[ProductModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[ProductModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4) 

def test_gets_products_with_referring_retailer_location_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: ProductModel = create_product(context, ProductCreateModel(create_referring_retailer_location_if_null=True))
    posted_object_2: ProductModel = create_product(context, ProductCreateModel(create_referring_retailer_location_if_null=True))
    posted_object_3: ProductModel = create_product(context, ProductCreateModel(referring_retailer_location_id = posted_object_1.referring_retailer_location_id))
    posted_object_4: ProductModel = create_product(context, ProductCreateModel(create_referring_retailer_location_if_null=True))

    filters: ProductSearchModel = ProductSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        referring_retailer_location_ids = f"{posted_object_1.referring_retailer_location_id},{posted_object_4.referring_retailer_location_id}"
    )
    
    result: PagedResponseItemList[ProductModel] = get_products(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[ProductModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[ProductModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[ProductModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)
     

 