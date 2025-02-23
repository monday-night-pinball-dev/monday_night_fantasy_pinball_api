import datetime

from requests import Response 
from tests.qdk.operators.historical_sales import HistoricalSaleCreateModel, HistoricalSaleModel, create_historical_sale
from tests.qdk.operators.sales_intake_jobs import SalesIntakeJobModel
from tests.qdk.operators.products import ProductCreateModel, ProductModel, create_product
from tests.qdk.operators.retailer_locations import RetailerLocationCreateModel, RetailerLocationModel, create_retailer_location
from tests.qdk.operators.retailers import RetailerModel
from tests.qdk.operators.sales_intake_jobs import SalesIntakeJobModel
from tests.qdk.operators.vendors import VendorModel
from tests.qdk.qa_requests import qa_get, qa_patch, qa_post
from tests.qdk.types import PagedResponseItemList, PagingResponseModel, PagingRequestModel, RequestOperators, TestContext
from tests.qdk.utils import assert_object_was_updated, assert_objects_are_equal, copy_object_when_appropriate, generate_random_string
 
class HistoricalSaleItemCreateModel():  

    def __init__(
        self,  
        
        product_id: str | None = None,
        product: ProductCreateModel | None = None,
        
        historical_sale_id: str | None = None,
        historical_sale: HistoricalSaleCreateModel | None = None,
 
        sku: str | None = None,
        sale_timestamp: str | None = None,
        pos_sale_id: str | None = None,  
        pos_product_id: str | None = None,  
        lot_identifier: str | None = None,  
        sale_count: float | None = None,
        unit_of_weight: str | None = None,
        weight_in_units: float | None = None,
        sale_item_name: str | None = None,
        total: int | None = None,
        sub_total: int | None = None,
        discount: int | None = None,
        tax: int | None = None,
        cost : int | None = None,   
    ) -> None:
          
        self.sale_timestamp = sale_timestamp
        self.pos_sale_id = pos_sale_id
        self.total = total
        self.sub_total = sub_total
        self.discount = discount
        self.tax = tax
        self.cost = cost
        
        self.product_id = product_id
        self.product = product
        
        self.historical_sale_id = historical_sale_id
        self.historical_sale = historical_sale
        
        self.sku = sku
        self.sale_timestamp = sale_timestamp
        self.pos_sale_id = pos_sale_id
        self.pos_product_id = pos_product_id
        self.lot_identifier = lot_identifier
        self.sale_count = sale_count
        self.unit_of_weight = unit_of_weight
        self.weight_in_units = weight_in_units
        self.sale_item_name = sale_item_name 
          
class HistoricalSaleItemModel():  

    def __init__(self, 
        id: str, 
        product_id: str,  
        retailer_id: str, 
        retailer_location_id: str,  
        historical_sale_id: str,
        sku: str,
        sale_count: float,
        total: int,
        sale_timestamp: str, 
        created_at: str,   
        pos_sale_id: str | None = None,
        pos_product_id: str | None = None,
        lot_identifier: str | None = None,
        unit_of_weight: str | None = None,
        weight_in_units: float | None = None,
        sale_item_name: str | None = None,
        sub_total: int | None = None,
        discount: int | None = None,
        tax: int | None = None,
        cost : int | None = None,
        sales_intake_job_id: str | None = None, 
        sales_intake_job: SalesIntakeJobModel | None = None,
        product: ProductModel | None = None,
        product_vendor_id: str | None = None,
        product_vendor: VendorModel | None = None, 
        historical_sale: HistoricalSaleModel | None = None,
        retailer_location: RetailerLocationModel | None = None,
        retailer: RetailerModel | None = None, 
        updated_at: str | None = None,
    ) -> None:
        
            self.id = id
            self.retailer_location_id = retailer_location_id
            self.retailer_location = RetailerLocationModel(**retailer_location) if retailer_location is not None else None
            self.retailer_id = retailer_id
            self.retailer = RetailerModel(**retailer) if retailer is not None else None
            self.sales_intake_job_id = sales_intake_job_id
            self.sales_intake_job = SalesIntakeJobModel(**sales_intake_job) if sales_intake_job is not None else None
            self.product_id = product_id
            self.product = ProductModel(**product) if product is not None else None
            self.product_vendor_id = product_vendor_id
            self.product_vendor = VendorModel(**product_vendor) if product_vendor is not None else None
            self.historical_sale_id = historical_sale_id
            self.historical_sale = HistoricalSaleModel(**historical_sale) if historical_sale is not None else None
            
            self.sale_timestamp = sale_timestamp
            self.created_at = created_at
            
            self.pos_sale_id = pos_sale_id
            self.pos_product_id = pos_product_id
            self.lot_identifier = lot_identifier
            self.unit_of_weight = unit_of_weight
            self.weight_in_units = weight_in_units
            self.sale_item_name = sale_item_name
            self.sku = sku
            self.sale_coount = sale_count
            self.sub_total = sub_total
            self.total = total 
            
            self.discount = discount
            self.tax = tax
            self.cost = cost
            self.updated_at = updated_at

class HistoricalSaleItemSearchModel(PagingRequestModel):  

    def __init__(self, 
                ids: str | None = None,  
                retailer_ids: str | None = None,  
                retailer_location_ids: str | None = None,   
                sales_intake_job_ids: str | None = None,  
                product_ids: str | None = None,
                product_vendor_ids: str | None = None, 
                historical_sale_ids: str | None = None,
                skus: str | None = None,
                lot_identifiers: str | None = None,
                sale_item_name : str | None = None,
                sale_timestamp_min: str | None = None,
                sale_timestamp_max: str | None = None, 
                pos_sale_ids: str | None = None,
                pos_product_ids: str | None = None,
                page: int | None = None,
                page_length: int | None = None,
                is_sort_descending: bool | None = None,
                sort_by: str | None = None) -> None:
        super().__init__(
            page = page,
            page_length = page_length,
            is_sort_descending = is_sort_descending,
            sort_by = sort_by
        )
        
        self.ids = ids 
        self.retailer_ids = retailer_ids 
        self.retailer_location_ids = retailer_location_ids 
        self.sales_intake_job_ids = sales_intake_job_ids 
        self.sale_timestamp_min = sale_timestamp_min
        self.sale_timestamp_max = sale_timestamp_max
        self.pos_sale_ids = pos_sale_ids
        self.pos_product_ids = pos_product_ids
        self.product_ids = product_ids
        self.product_vendor_ids = product_vendor_ids
        self.historical_sale_ids = historical_sale_ids
        self.skus = skus
        self.lot_identifiers = lot_identifiers
        self.sale_item_name = sale_item_name
 
 
def mint_default_historical_sale_item(
    context: TestContext, 
    overrides: HistoricalSaleItemCreateModel | None = None, 
    request_operators: RequestOperators | None = None
) -> HistoricalSaleItemCreateModel: 
    random_string = generate_random_string()

    overrides = overrides or HistoricalSaleItemCreateModel()
    
    if(overrides.product_id is None):

        new_product = create_product(context, overrides.product, request_operators = request_operators)
        overrides.product_id = new_product.id

        del overrides.product 
    
    if(overrides.historical_sale_id is None):

        new_historical_sale = create_historical_sale(context, overrides.historical_sale, request_operators = request_operators)
        overrides.historical_sale_id = new_historical_sale.id

        del overrides.historical_sale
  
    default_historical_sale_item: HistoricalSaleItemCreateModel = HistoricalSaleItemCreateModel(
        sale_timestamp= "2024-11-01T11:00:00.000Z",
        pos_sale_id = "1234567890", 
        total = 333,
        sub_total = 444,
        discount = 222,
        tax = 111,
        cost = 999,
        sale_item_name= random_string + "_sale_item_name",
        lot_identifier= random_string + "_lot_identifier",
        unit_of_weight= "Grams",
        sale_count=333.333,
        weight_in_units=222.222,
        sku= random_string + "_sku" 
    )

    copy_object_when_appropriate(default_historical_sale_item, overrides)
     
    return default_historical_sale_item

def create_historical_sale_item(
        context: TestContext,
        overrides: HistoricalSaleItemCreateModel | None = None, 
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ) -> HistoricalSaleItemModel:
    
    post_object: HistoricalSaleItemCreateModel = mint_default_historical_sale_item(context = context, overrides = overrides, request_operators = request_operators)

    result: Response = qa_post(context.api_url + "/historical_sale_items", post_object, request_operators)

    if(allow_failures == False):
        assert result.status_code == 201
 
        result_dict = result.json()

        assert_objects_are_equal(result_dict, post_object.__dict__, 
            [
                "id",
                "created_at", 
                "updated_at", 
                "retailer_id",
                "retailer",
                "retailer_location_id", 
                "retailer_location", 
                "sales_intake_job_id",
                "sales_intake_job",
                "product_id",
                "product",
                "product_vendor_id",
                "product_vendor",
                "historical_sale_id",
                "historical_sale",
            ]
        )

        assert result_dict['id'] is not None
        assert result_dict['created_at'] is not None
        assert result_dict['updated_at'] is None
    
    return_object = HistoricalSaleItemModel(**result.json())
    
    return return_object 
 
def get_historical_sale_item_by_id(
        context: TestContext, 
        id: str,
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ) -> HistoricalSaleItemModel:

    url: str = f"{context.api_url}/historical_sale_items/{id}"
    
    result: Response = qa_get(url, request_operators = request_operators)
     
    return_object = HistoricalSaleItemModel(**result.json())
    
    return return_object 

def get_historical_sale_items(
        context: TestContext, 
        search_model: HistoricalSaleItemSearchModel | None,
        request_operators: RequestOperators | None = None 
    ) -> PagedResponseItemList[HistoricalSaleItemModel]: 

    url: str = f"{context.api_url}/historical_sale_items"
    
    result: Response = qa_get(
        url = url, 
        query_params = search_model if search_model is not None else {},
        request_operators = request_operators
    )
    
    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict['paging'])
     
    return_items: list[HistoricalSaleItemModel] = [HistoricalSaleItemModel(**obj) for obj in result_dict['items']]

    return_object = PagedResponseItemList[HistoricalSaleItemModel](
        items = return_items, paging = return_paging_object
    )
    
    return return_object 

def historical_sale_item_hydration_check(historical_sale_item: HistoricalSaleItemModel) -> None:
    assert historical_sale_item.product is not None
    assert historical_sale_item.product.id is not None
    assert historical_sale_item.product.id == historical_sale_item.product_id
    
    assert historical_sale_item.product_vendor is not None
    assert historical_sale_item.product_vendor.id is not None
    assert historical_sale_item.product_vendor.id == historical_sale_item.product_vendor_id
    
    assert historical_sale_item.historical_sale is not None
    assert historical_sale_item.historical_sale.id is not None
    assert historical_sale_item.historical_sale.id == historical_sale_item.historical_sale_id
    
    assert historical_sale_item.retailer_location is not None
    assert historical_sale_item.retailer_location.id is not None
    assert historical_sale_item.retailer_location.id == historical_sale_item.retailer_location_id
    
    assert historical_sale_item.retailer is not None
    assert historical_sale_item.retailer.id is not None
    assert historical_sale_item.retailer.id == historical_sale_item.retailer_id
    
    assert historical_sale_item.sales_intake_job is not None
    assert historical_sale_item.sales_intake_job.id is not None 
    assert historical_sale_item.sales_intake_job.id == historical_sale_item.sales_intake_job_id         
    
    