import datetime
from typing import Self

from requests import Response   
from tests.qdk.operators.retailer_locations import RetailerLocationCreateModel, RetailerLocationModel, create_retailer_location
from tests.qdk.operators.retailers import RetailerModel
from tests.qdk.operators.vendors import VendorCreateModel, VendorModel, create_vendor
from tests.qdk.qa_requests import qa_get, qa_patch, qa_post
from tests.qdk.types import PagedResponseItemList, PagingRequestModel, PagingResponseModel, RequestOperators, TestContext
from tests.qdk.utils import assert_object_was_updated, assert_objects_are_equal, copy_object_when_appropriate, generate_random_string
  
class ProductCreateModel():  

    def __init__(self,
        referring_retailer_location_id: str | None = None,
        referring_retailer_location: RetailerLocationCreateModel | None = None,   
        create_referring_retailer_location_if_null: bool | None = False,
        vendor_id: str | None = None,
        vendor: VendorCreateModel | None = None,   
        create_vendor_if_null: bool | None = False,
        confirmed_core_product_id: str | None = None,
        confirmed_core_product: Self | None = None,   
        create_confirmed_core_product_if_null: bool | None = False,
            
        name: str | None = None,
        vendor_sku: str | None = None,
        vendor_confirmation_status: str | None = None,
                
    ) -> None:
         
        self.name = name
                
        self.vendor_sku = vendor_sku
        self.vendor_confirmation_status = vendor_confirmation_status
        self.confirmed_core_product_id = confirmed_core_product_id
        self.confirmed_core_product = confirmed_core_product
        self.create_confirmed_core_product_if_null = create_confirmed_core_product_if_null
        self.referring_retailer_location_id = referring_retailer_location_id
        self.referring_retailer_location = referring_retailer_location
        self.create_referring_retailer_location_if_null = create_referring_retailer_location_if_null
        self.vendor_id = vendor_id
        self.vendor = vendor
        self.create_vendor_if_null = create_vendor_if_null
        
class ProductModel():  

    def __init__(self, 
        id: str, 
        created_at: datetime.datetime, 
        referring_retailer_id: str | None = None,
        referring_retailer: RetailerModel | None = None,    
        referring_retailer_location_id: str | None = None,
        referring_retailer_location: RetailerLocationModel | None = None,    
        vendor_id: str | None = None,
        vendor: VendorModel | None = None,    
        confirmed_core_product_id: str | None = None,
        confirmed_core_product: Self | None = None,    
        name: str | None = None,
        vendor_sku: str | None = None,
        vendor_confirmation_status: str | None = None, 
        updated_at: datetime.datetime | None = None
    ) -> None:
                
        self.id = id
        self.referring_retailer_id = referring_retailer_id
        self.referring_retailer = RetailerModel(**referring_retailer) if referring_retailer is not None else None
        self.referring_retailer_location_id = referring_retailer_location_id
        self.referring_retailer_location = RetailerLocationModel(**referring_retailer_location) if referring_retailer_location is not None else None
        self.vendor_id = vendor_id
        self.vendor = VendorModel(**vendor) if vendor is not None else None
        self.confirmed_core_product_id = confirmed_core_product_id
        self.confirmed_core_product = ProductModel(**confirmed_core_product) if confirmed_core_product is not None else None
        self.vendor_sku = vendor_sku
        self.name = name
        self.vendor_confirmation_status = vendor_confirmation_status
        self.created_at = created_at
        self.updated_at = updated_at
          
class ProductSearchModel(PagingRequestModel):  

    def __init__(self, 
        ids: str | None = None,  
        referring_retailer_ids: str | None = None, 
        referring_retailer_location_ids: str | None = None, 
        vendor_ids: str | None = None, 
        confirmed_core_product_ids: str | None = None,
        name: str | None = None,
        name_like: str | None = None,  
        vendor_sku: str | None = None,
        vendor_confirmation_status: str | None = None,
        page: int | None = None,
        page_length: int | None = None,
        is_sort_descending: bool | None = None,
        sort_by: str | None = None
    ) -> None:
        
        super().__init__(
            page = page,
            page_length = page_length,
            is_sort_descending = is_sort_descending,
            sort_by = sort_by
        )
        
        self.ids = ids 
        self.referring_retailer_ids = referring_retailer_ids  
        self.referring_retailer_location_ids = referring_retailer_location_ids 
        self.vendor_ids = vendor_ids 
        self.confirmed_core_product_ids = confirmed_core_product_ids
        self.vendor_sku = vendor_sku
        self.vendor_confirmation_status = vendor_confirmation_status
        self.name = name
        self.name_like = name_like
        
class ProductUpdateModel():  

    def __init__(self,    
        vendor_id: str | None = None,  
        confirmed_core_product_id: str | None = None,  
            
        name: str | None = None,
        vendor_sku: str | None = None,
        vendor_confirmation_status: str | None = None
    ) -> None: 
          
        self.name = name 
        self.vendor_sku = vendor_sku
        self.vendor_confirmation_status = vendor_confirmation_status
        self.confirmed_core_product_id = confirmed_core_product_id
        self.vendor_id = vendor_id
        
 
def mint_default_product(
    context: TestContext, 
    overrides: ProductCreateModel | None = None, 
    request_operators: RequestOperators | None = None
) -> ProductCreateModel: 
    
    overrides = overrides or ProductCreateModel()

    if(overrides.referring_retailer_location_id is None and overrides.create_referring_retailer_location_if_null):

        new_retailer_location = create_retailer_location(context, overrides.referring_retailer_location, request_operators = request_operators)
        overrides.referring_retailer_location_id = new_retailer_location.id

        del overrides.referring_retailer_location
        del overrides.create_referring_retailer_location_if_null
    
    if(overrides.vendor_id is None and overrides.create_vendor_if_null):

        new_vendor = create_vendor(context, overrides.vendor, request_operators = request_operators)
        overrides.vendor_id = new_vendor.id

        del overrides.vendor
        del overrides.create_vendor_if_null
     
    if(overrides.confirmed_core_product_id is None and overrides.create_confirmed_core_product_if_null):

        new_confirmed_core_product = create_product(context, overrides.confirmed_core_product, request_operators = request_operators)
        overrides.confirmed_core_product_id = new_confirmed_core_product.id

        del overrides.confirmed_core_product
        del overrides.create_confirmed_core_product_if_null
         
    random_string = generate_random_string()
    
    default_product: ProductCreateModel = ProductCreateModel(
        name = random_string + '_name', 
        vendor_sku = random_string + '_vendor_sku',
        vendor_confirmation_status = 'Candidate', 
    )

    copy_object_when_appropriate(default_product, overrides)
     
    return default_product

def create_product(
        context: TestContext,
        overrides: ProductCreateModel | None = None, 
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ):
    
    post_object = mint_default_product(context = context, overrides = overrides, request_operators = request_operators)

    result = qa_post(context.api_url + "/products", post_object, request_operators)

    if(allow_failures == False):
        assert result.status_code == 201
 
        result_dict = result.json()

        assert_objects_are_equal(result_dict, post_object.__dict__, ["id", "created_at", "updated_at", "referring_retailer_id", "referring_retailer", "referring_retailer_location_id", "referring_retailer_location", "vendor_id", "vendor", "confirmed_core_product_id", "confirmed_core_product"])

        assert result_dict['id'] is not None
        assert result_dict['created_at'] is not None
        assert result_dict['updated_at'] is None
     
    return_object = ProductModel(**result.json())
    
    return return_object 

def get_product_by_id(
        context: TestContext, 
        id: str,
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ):

    url = f"{context.api_url}/products/{id}"
    
    result = qa_get(url, request_operators = request_operators)
 
    return_object = ProductModel(**result.json())
    
    return return_object 

def get_products(
        context: TestContext, 
        search_model: ProductSearchModel | None,
        request_operators: RequestOperators | None = None 
    ) -> PagedResponseItemList[ProductModel]: 

    url: str = f"{context.api_url}/products"
    
    result: Response = qa_get(
        url = url, 
        query_params = search_model if search_model is not None else {},
        request_operators = request_operators
    )
    
    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict['paging'])
     
    return_items: list[ProductModel] = [ProductModel(**obj) for obj in result_dict['items']]

    return_object = PagedResponseItemList[ProductModel](
        items = return_items, paging = return_paging_object
    )
    
    return return_object 


def update_product(
        context: TestContext,
        id: str,
        update_model: ProductUpdateModel | None = None, 
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ):
    
    original_object: ProductModel = get_product_by_id(context, id, request_operators)

    result = qa_patch(f"{context.api_url}/products/{id}", update_model, request_operators)

    if(allow_failures == False):
        assert result.status_code == 200
 
        result_dict = result.json()

        assert_object_was_updated(original_object.__dict__, update_model.__dict__, result_dict, ["updated_at", "referring_retailer", "referring_retailer_location", "vendor", "confirmed_core_product"])
 
        assert result_dict['updated_at'] is not None
    
    return_object = ProductModel(**result.json())
    
    return return_object 

def product_hydration_check(product: ProductModel) -> None:
  
    assert product.referring_retailer_location is not None
    assert product.referring_retailer_location.id is not None
    assert product.referring_retailer_location.id == product.referring_retailer_location_id
  
    assert product.referring_retailer is not None
    assert product.referring_retailer.id is not None
    assert product.referring_retailer.id == product.referring_retailer_id 
    
    assert product.confirmed_core_product is not None
    assert product.confirmed_core_product.id is not None
    assert product.confirmed_core_product.id == product.confirmed_core_product_id
    
    assert product.vendor is not None
    assert product.vendor.id is not None
    assert product.vendor.id == product.vendor_id 