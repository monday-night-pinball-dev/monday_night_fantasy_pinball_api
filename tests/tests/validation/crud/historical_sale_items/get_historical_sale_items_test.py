from time import sleep
from typing import Any

from tests.qdk.operators.historical_sale_items import HistoricalSaleItemCreateModel, HistoricalSaleItemModel, HistoricalSaleItemSearchModel, create_historical_sale_item, get_historical_sale_item_by_id, get_historical_sale_items, historical_sale_item_hydration_check
from tests.qdk.operators.historical_sales import HistoricalSaleCreateModel
from tests.qdk.operators.products import ProductCreateModel
from tests.qdk.qa_requests import qa_get, qa_post
from tests.qdk.types import PagedResponseItemList, RequestOperators, TestContext
from tests.qdk.utils import assert_objects_are_equal, generate_random_string
from urllib.parse import urlencode   
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_gets_historical_sale_item_by_id() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object = create_historical_sale_item(context)

    result = get_historical_sale_item_by_id(context, posted_object.id)

    assert result is not None
    assert result.id == posted_object.id
    
def test_gets_historical_sale_item_by_id_with_hydration() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object = create_historical_sale_item(
        context, 
        overrides=HistoricalSaleItemCreateModel(
            product= ProductCreateModel(
                create_vendor_if_null= True, 
            ),
            historical_sale= HistoricalSaleCreateModel(
                create_sales_intake_job_if_null= True
            )
        )
    )
    
    result = get_historical_sale_item_by_id(
        context,
        posted_object.id,
        request_operators=RequestOperators(
            hydration_properties=["product", "product_vendor", "historical_sale", "retailer_location", "retailer", "sales_intake_job"]
        )
    )

    assert result is not None
    assert result.id == posted_object.id
    
    historical_sale_item_hydration_check(result)

def test_gets_historical_sale_items_invalid_inputs() -> None:
     
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)
     
    result = qa_get(f"{context.api_url}/historical_sale_items", query_params={
        'ids': 'not an id,also not an id', 
        'retailer_ids': 'not valid,at all,cmon man',   
        'sales_intake_job_ids': 'lolcmon',  
        'historical_sale_ids': 'really,hate,ids,dontcha',  
        'product_ids': 'also,not,valid',  
        'product_vendor_ids': 'are,you,trying?',
        'retailer_location_ids': 'invalid,id,jamboree', 
        'sale_timestamp_min' : 'not a valid datetime',
        'sale_timestamp_max' : 'also not a valid datetime',  
        'page' : 'not a page num',
        'page_length' : 'not a length num',
        'is_sort_descending' : 'not a bool'
    })

    assert result.status_code == 422

    errors = result.json()

    assert len(errors['detail']) == 12
    
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: not an id,\n\t1: also not an id\n].'
  
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'sales_intake_job_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'    
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: lolcmon\n].'
     
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'historical_sale_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'    
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: really,\n\t1: hate,\n\t2: ids,\n\t3: dontcha\n].'
     
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'product_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'    
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: also,\n\t1: not,\n\t2: valid\n].'
     
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'product_vendor_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'    
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: are,\n\t1: you,\n\t2: trying?\n].'
    
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'retailer_location_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'    
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: invalid,\n\t1: id,\n\t2: jamboree\n].'
        
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'retailer_ids' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'invalid_id_list'    
    assert error[0]['msg'] == 'Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: not valid,\n\t1: at all,\n\t2: cmon man\n].'
  
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'sale_timestamp_min' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'datetime_from_date_parsing'
    assert error[0]['msg'] == 'Input should be a valid datetime or date, invalid character in year'
    
    error: list[Any] = [error for error in errors['detail'] if 'query' in error['loc'] and 'sale_timestamp_max' in error['loc']]
    assert len(error) == 1
    assert error[0]['type'] == 'datetime_from_date_parsing'
    assert error[0]['msg'] == 'Input should be a valid datetime or date, invalid character in year'
    
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
    
    
def test_gets_historical_sale_items_with_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: HistoricalSaleItemModel = create_historical_sale_item(context)
    posted_object_2: HistoricalSaleItemModel = create_historical_sale_item(context)
    posted_object_3: HistoricalSaleItemModel = create_historical_sale_item(context)
    posted_object_4: HistoricalSaleItemModel = create_historical_sale_item(context)

    filters: HistoricalSaleItemSearchModel = HistoricalSaleItemSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )
    
    result: PagedResponseItemList[HistoricalSaleItemModel] = get_historical_sale_items(context, filters)

    assert result is not None
    assert result.items is not None
    
    assert result.paging is not None
    assert result.paging.page == 1
    assert result.paging.page_length == 25
    assert result.paging.sort_by == 'created_at'
    assert result.paging.is_sort_descending == False

    assert len(result.items) == 4 
    
    posted_item_1: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1)

    posted_item_2: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2)
  
    posted_item_3: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)
  
    posted_item_4: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)

def test_gets_historical_sale_items_with_ids_filter_with_hydration() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: HistoricalSaleItemModel = create_historical_sale_item(
        context, 
        overrides=HistoricalSaleItemCreateModel(
            product= ProductCreateModel(
                create_vendor_if_null= True, 
            ),
            historical_sale= HistoricalSaleCreateModel(
                create_sales_intake_job_if_null= True
            )
        )
    )
        
    posted_object_2: HistoricalSaleItemModel = create_historical_sale_item(
        context, 
        overrides=HistoricalSaleItemCreateModel(
            product= ProductCreateModel(
                create_vendor_if_null= True, 
            ),
            historical_sale= HistoricalSaleCreateModel(
                create_sales_intake_job_if_null= True
            )
        )
    )
    posted_object_3: HistoricalSaleItemModel = create_historical_sale_item(
        context, 
        overrides=HistoricalSaleItemCreateModel(
            product= ProductCreateModel(
                create_vendor_if_null= True, 
            ),
            historical_sale= HistoricalSaleCreateModel(
                create_sales_intake_job_if_null= True
            )
        )
    )
    
    posted_object_4: HistoricalSaleItemModel = create_historical_sale_item(
        context, 
        overrides=HistoricalSaleItemCreateModel(
            product= ProductCreateModel(
                create_vendor_if_null= True, 
            ),
            historical_sale= HistoricalSaleCreateModel(
                create_sales_intake_job_if_null= True
            )
        )
    )

    filters: HistoricalSaleItemSearchModel = HistoricalSaleItemSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )
    
    result: PagedResponseItemList[HistoricalSaleItemModel] = get_historical_sale_items(context, filters, request_operators=RequestOperators(hydration_properties=["product", "product_vendor", "historical_sale", "retailer_location", "retailer", "sales_intake_job"]))

    assert result is not None
    assert result.items is not None
    
    assert result.paging is not None
    assert result.paging.page == 1
    assert result.paging.page_length == 25
    assert result.paging.sort_by == 'created_at'
    assert result.paging.is_sort_descending == False

    assert len(result.items) == 4 
    
    posted_item_1: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1, exempt_properties=["product", "product_vendor", "historical_sale", "retailer_location", "retailer", "sales_intake_job"])

    historical_sale_item_hydration_check(posted_item_1[0])

    posted_item_2: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2, exempt_properties=["product", "product_vendor", "historical_sale", "retailer_location", "retailer", "sales_intake_job"])
    
    historical_sale_item_hydration_check(posted_item_2[0])
  
    posted_item_3: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3, exempt_properties=["product", "product_vendor", "historical_sale", "retailer_location", "retailer", "sales_intake_job"])
    
    historical_sale_item_hydration_check(posted_item_3[0])
  
    posted_item_4: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4, exempt_properties=["product", "product_vendor", "historical_sale", "retailer_location", "retailer", "sales_intake_job"])
    
    historical_sale_item_hydration_check(posted_item_4[0])
      
def test_gets_historical_sale_items_with_retailer_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: HistoricalSaleItemModel = create_historical_sale_item(context)
    posted_object_2: HistoricalSaleItemModel = create_historical_sale_item(context)
    posted_object_3: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(historical_sale_id= posted_object_1.historical_sale_id))
    posted_object_4: HistoricalSaleItemModel = create_historical_sale_item(context)

    filters: HistoricalSaleItemSearchModel = HistoricalSaleItemSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        retailer_ids = f"{posted_object_1.retailer_id},{posted_object_4.retailer_id}"
    )
    
    result: PagedResponseItemList[HistoricalSaleItemModel] = get_historical_sale_items(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1)  
  
    posted_item_3: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3) 

    posted_item_4: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4) 
    
def test_gets_historical_sale_items_with_retailer_location_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: HistoricalSaleItemModel = create_historical_sale_item(context)
    posted_object_2: HistoricalSaleItemModel = create_historical_sale_item(context)
    posted_object_3: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(historical_sale_id= posted_object_1.historical_sale_id))
    posted_object_4: HistoricalSaleItemModel = create_historical_sale_item(context)

    filters: HistoricalSaleItemSearchModel = HistoricalSaleItemSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        retailer_location_ids = f"{posted_object_1.retailer_location_id},{posted_object_4.retailer_location_id}"
    )
    
    result: PagedResponseItemList[HistoricalSaleItemModel] = get_historical_sale_items(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)  
     
def test_gets_historical_sale_items_with_sales_intake_job_ids_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(
        historical_sale= HistoricalSaleCreateModel(create_sales_intake_job_if_null= True)
    ))
    posted_object_2: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(
        historical_sale= HistoricalSaleCreateModel(create_sales_intake_job_if_null= True)
    ))
    posted_object_3: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(historical_sale_id= posted_object_1.historical_sale_id))
    posted_object_4: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(
        historical_sale= HistoricalSaleCreateModel(create_sales_intake_job_if_null= True)
    ))

    filters: HistoricalSaleItemSearchModel = HistoricalSaleItemSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        sales_intake_job_ids = f"{posted_object_1.sales_intake_job_id},{posted_object_4.sales_intake_job_id}"
    )
    
    result: PagedResponseItemList[HistoricalSaleItemModel] = get_historical_sale_items(context, filters)
    
    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)


def test_gets_historical_sale_items_with_product_ids_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: HistoricalSaleItemModel = create_historical_sale_item(context)
    posted_object_2: HistoricalSaleItemModel = create_historical_sale_item(context)   
    posted_object_3: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(product_id= posted_object_1.product_id))
    posted_object_4: HistoricalSaleItemModel = create_historical_sale_item(context)

    filters: HistoricalSaleItemSearchModel = HistoricalSaleItemSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        product_ids = f"{posted_object_1.product_id},{posted_object_4.product_id}"
    )
    
    result: PagedResponseItemList[HistoricalSaleItemModel] = get_historical_sale_items(context, filters)
    
    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)
     
def test_gets_historical_sale_items_with_product_vendor_ids_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(
        product= ProductCreateModel(create_vendor_if_null= True)
    ))
    posted_object_2: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(
        product= ProductCreateModel(create_vendor_if_null= True)
    ))
    posted_object_3: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(product_id= posted_object_1.product_id))
    posted_object_4: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(
        product= ProductCreateModel(create_vendor_if_null= True)
    ))

    filters: HistoricalSaleItemSearchModel = HistoricalSaleItemSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        product_vendor_ids = f"{posted_object_1.product_vendor_id},{posted_object_4.product_vendor_id}"
    )
    
    result: PagedResponseItemList[HistoricalSaleItemModel] = get_historical_sale_items(context, filters)
    
    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)
    
      
def test_gets_historical_sale_items_with_pos_sale_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(pos_sale_id = '1234567890'))
    posted_object_2: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(pos_sale_id = '1111111111'))
    posted_object_3: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(pos_sale_id = '1234567890'))
    posted_object_4: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(pos_sale_id = '2222222222'))

    filters: HistoricalSaleItemSearchModel = HistoricalSaleItemSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        pos_sale_ids = f"{posted_object_1.pos_sale_id},{posted_object_4.pos_sale_id}"
    )
    
    result: PagedResponseItemList[HistoricalSaleItemModel] = get_historical_sale_items(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)  
     
def test_gets_historical_sale_items_with_pos_product_ids_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(pos_product_id = '1234567890'))
    posted_object_2: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(pos_product_id = '1111111111'))
    posted_object_3: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(pos_product_id = '1234567890'))
    posted_object_4: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(pos_product_id = '2222222222'))

    filters: HistoricalSaleItemSearchModel = HistoricalSaleItemSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        pos_product_ids = f"{posted_object_1.pos_product_id},{posted_object_4.pos_product_id}"
    )
    
    result: PagedResponseItemList[HistoricalSaleItemModel] = get_historical_sale_items(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)  
    
    
def test_gets_historical_sale_items_with_skus_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(sku = '1234567890'))
    posted_object_2: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(sku = '1111111111'))
    posted_object_3: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(sku = '1234567890'))
    posted_object_4: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(sku = '2222222222'))

    filters: HistoricalSaleItemSearchModel = HistoricalSaleItemSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        skus = f"{posted_object_1.sku},{posted_object_4.sku}"
    )
    
    result: PagedResponseItemList[HistoricalSaleItemModel] = get_historical_sale_items(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)  
    
    
def test_gets_historical_sale_items_with_lot_identifiers_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(lot_identifier = '1234567890'))
    posted_object_2: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(lot_identifier = '1111111111'))
    posted_object_3: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(lot_identifier = '1234567890'))
    posted_object_4: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(lot_identifier = '2222222222'))

    filters: HistoricalSaleItemSearchModel = HistoricalSaleItemSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        lot_identifiers = f"{posted_object_1.lot_identifier},{posted_object_4.lot_identifier}"
    )
    
    result: PagedResponseItemList[HistoricalSaleItemModel] = get_historical_sale_items(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 3
    
    posted_item_1: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)  
      
def test_gets_historical_sale_items_with_sale_item_name_filter() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(sale_item_name = 'BOOF'))
    posted_object_2: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(sale_item_name = 'BEEF'))
    posted_object_3: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(sale_item_name = 'BOOF'))
    posted_object_4: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(sale_item_name = 'BLARB'))

    filters: HistoricalSaleItemSearchModel = HistoricalSaleItemSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        sale_item_name = "BOOF"
    )
    
    result: PagedResponseItemList[HistoricalSaleItemModel] = get_historical_sale_items(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 2
    
    posted_item_1: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_1.id]
    assert len(posted_item_1) == 1  
    assert_objects_are_equal(posted_item_1[0], posted_object_1) 
  
    posted_item_3: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3)
    
def test_getshistorical_sale_items_with_sale_timestamp_min_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(sale_timestamp = "2021-01-01T01:00:00.000Z"))
    posted_object_2: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(sale_timestamp = "2024-04-04T04:00:00.000Z"))
    posted_object_3: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(sale_timestamp = "2022-02-02T02:00:00.000Z"))
    posted_object_4: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(sale_timestamp = "2023-03-03T03:00:00.000Z"))

    filters: HistoricalSaleItemSearchModel = HistoricalSaleItemSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        sale_timestamp_min = "2023-03-03T03:00:00.000Z"
    )
    
    result: PagedResponseItemList[HistoricalSaleItemModel] = get_historical_sale_items(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 2
 
  
    posted_item_2: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_2.id]
    assert len(posted_item_2) == 1 
    assert_objects_are_equal(posted_item_2[0], posted_object_2)

    posted_item_4: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)
    
def test_getshistorical_sale_items_with_sale_timestamp_min_and_max_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(sale_timestamp = "2021-01-01T01:00:00.000Z"))
    posted_object_2: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(sale_timestamp = "2024-04-04T04:00:00.000Z"))
    posted_object_3: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(sale_timestamp = "2022-02-02T02:00:00.000Z"))
    posted_object_4: HistoricalSaleItemModel = create_historical_sale_item(context, HistoricalSaleItemCreateModel(sale_timestamp = "2023-03-03T03:00:00.000Z"))

    filters: HistoricalSaleItemSearchModel = HistoricalSaleItemSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        sale_timestamp_max = "2023-03-03T03:00:00.000Z",
        sale_timestamp_min = "2022-02-02T02:00:00.000Z",
    )
    
    result: PagedResponseItemList[HistoricalSaleItemModel] = get_historical_sale_items(context, filters)

    assert result is not None
    assert result.items is not None 

    assert len(result.items) == 2
 
    posted_item_3: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_3.id]
    assert len(posted_item_3) == 1 
    assert_objects_are_equal(posted_item_3[0], posted_object_3) 

    posted_item_4: list[HistoricalSaleItemModel] = [item for item in result.items if item.id == posted_object_4.id]
    assert len(posted_item_4) == 1 
    assert_objects_are_equal(posted_item_4[0], posted_object_4)


def test_gets_historical_sale_items_with_paging() -> None:
    populate_configuration_if_not_exists() 

    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    posted_object_1: HistoricalSaleItemModel = create_historical_sale_item(context)
    posted_object_2: HistoricalSaleItemModel = create_historical_sale_item(context)
    
    sleep(1)
    
    posted_object_3: HistoricalSaleItemModel = create_historical_sale_item(context)
    posted_object_4: HistoricalSaleItemModel = create_historical_sale_item(context)

    filters_1: HistoricalSaleItemSearchModel = HistoricalSaleItemSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page = 1,
        page_length = 2
    )

    filters_2: HistoricalSaleItemSearchModel = HistoricalSaleItemSearchModel(
        ids = f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page = 2,
        page_length = 2
    )
    
    result_page_1: PagedResponseItemList[HistoricalSaleItemModel] = get_historical_sale_items(context, filters_1)
    result_page_2: PagedResponseItemList[HistoricalSaleItemModel] = get_historical_sale_items(context, filters_2)

    ## Page 1

    assert result_page_1 is not None
    assert result_page_1.items is not None
    
    assert result_page_1.paging is not None
    assert result_page_1.paging.page == 1
    assert result_page_1.paging.page_length == 2
    assert result_page_1.paging.sort_by == 'created_at'
    assert result_page_1.paging.is_sort_descending == False

    posted_item_page_1_item_1: list[HistoricalSaleItemModel] = [item for item in result_page_1.items if item.id == posted_object_1.id]
    assert len(posted_item_page_1_item_1) == 1  
    assert_objects_are_equal(posted_item_page_1_item_1[0], posted_object_1)

    posted_item_page_1_item_2: list[HistoricalSaleItemModel] = [item for item in result_page_1.items if item.id == posted_object_2.id]
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
     
    posted_item_page_2_item_1: list[HistoricalSaleItemModel] = [item for item in result_page_2.items if item.id == posted_object_3.id]
    assert len(posted_item_page_2_item_1) == 1  
    assert_objects_are_equal(posted_item_page_2_item_1[0], posted_object_3)

    posted_item_page_2_item_2: list[HistoricalSaleItemModel] = [item for item in result_page_2.items if item.id == posted_object_4.id]
    assert len(posted_item_page_2_item_2) == 1  
    assert_objects_are_equal(posted_item_page_2_item_2[0], posted_object_4)
    