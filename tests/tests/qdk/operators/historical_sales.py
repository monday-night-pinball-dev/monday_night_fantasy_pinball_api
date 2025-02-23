import datetime

from requests import Response 
from tests.qdk.operators.sales_intake_jobs import SalesIntakeJobModel, create_sales_intake_job
from tests.qdk.operators.products import create_product
from tests.qdk.operators.retailer_locations import RetailerLocationCreateModel, RetailerLocationModel, create_retailer_location
from tests.qdk.operators.retailers import RetailerModel
from tests.qdk.operators.sales_intake_jobs import SalesIntakeJobModel
from tests.qdk.operators.vendors import VendorModel
from tests.qdk.qa_requests import qa_get, qa_patch, qa_post
from tests.qdk.types import PagedResponseItemList, PagingResponseModel, PagingRequestModel, RequestOperators, TestContext
from tests.qdk.utils import assert_object_was_updated, assert_objects_are_equal, copy_object_when_appropriate, generate_random_string
 
class HistoricalSaleCreateModel():  

    def __init__(
        self, 
        retailer_location_id: str | None = None,
        retailer_location: RetailerLocationCreateModel | None = None,
        sales_intake_job_id: str | None = None, 
        sales_intake_job: SalesIntakeJobModel | None = None,
        create_sales_intake_job_if_null: bool | None = False,
        sale_timestamp: str | None = None,
        pos_sale_id:    str | None = None,  
        total: int | None = None,
        sub_total: int | None = None,
        discount: int | None = None,
        tax: int | None = None,
        cost : int | None = None,   
    ) -> None:
         
        self.retailer_location_id = retailer_location_id
        self.sales_intake_job_id = sales_intake_job_id
        self.retailer_location = retailer_location
        self.sales_intake_job = sales_intake_job
        self.create_sales_intake_job_if_null = create_sales_intake_job_if_null
        self.sale_timestamp = sale_timestamp
        self.pos_sale_id = pos_sale_id
        self.total = total
        self.sub_total = sub_total
        self.discount = discount
        self.tax = tax
        self.cost = cost
        
          
class HistoricalSaleModel():  

    def __init__(self, 
        id: str, 
        retailer_id: str, 
        retailer_location_id: str,  
        pos_sale_id: str,
        sale_timestamp: str,
        total: int,
        created_at: str,  
        sub_total: int | None = None,
        discount: int | None = None,
        tax: int | None = None,
        cost : int | None = None,
        sales_intake_job_id: str | None = None, 
        sales_intake_job: SalesIntakeJobModel | None = None,
        retailer_location: RetailerLocationModel | None = None,
        retailer: RetailerModel | None = None, 
        updated_at: str | None = None,
    ) -> None:
        
            self.id = id
            self.retailer_location_id = retailer_location_id
            self.retailer_id = retailer_id
            self.pos_sale_id = pos_sale_id
            self.sale_timestamp = sale_timestamp
            self.total = total
            self.created_at = created_at
            self.sub_total = sub_total
            self.discount = discount
            self.tax = tax
            self.cost = cost
            self.sales_intake_job_id = sales_intake_job_id
            self.retailer_location = RetailerLocationModel(**retailer_location) if retailer_location is not None else None
            self.retailer = RetailerModel(**retailer) if retailer is not None else None
            self.sales_intake_job = SalesIntakeJobModel(**sales_intake_job) if sales_intake_job is not None else None
            self.updated_at = updated_at

class HistoricalSaleSearchModel(PagingRequestModel):  

    def __init__(self, 
                ids: str | None = None,  
                retailer_ids: str | None = None,  
                retailer_location_ids: str | None = None,   
                sales_intake_job_ids: str | None = None,  
                sale_timestamp_min: str | None = None,
                sale_timestamp_max: str | None = None, 
                pos_sale_ids: str | None = None,
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
 
 
def mint_default_historical_sale(
    context: TestContext, 
    overrides: HistoricalSaleCreateModel | None = None, 
    request_operators: RequestOperators | None = None
) -> HistoricalSaleCreateModel: 
    random_string = generate_random_string()

    overrides = overrides or HistoricalSaleCreateModel()
    
    if(overrides.retailer_location_id is None):

        new_retailer_location = create_retailer_location(context, overrides.retailer_location, request_operators = request_operators)
        overrides.retailer_location_id = new_retailer_location.id

        del overrides.retailer_location 
    
    if(overrides.sales_intake_job_id is None and overrides.create_sales_intake_job_if_null is True):

        new_sales_intake_job = create_sales_intake_job(context, overrides.sales_intake_job, request_operators = request_operators)
        overrides.sales_intake_job_id = new_sales_intake_job.id

        del overrides.sales_intake_job
  
    default_historical_sale: HistoricalSaleCreateModel = HistoricalSaleCreateModel(
        sale_timestamp= "2024-11-01T11:00:00.000Z",
        pos_sale_id = "1234567890", 
        total = 333,
        sub_total = 444,
        discount = 222,
        tax = 111,
        cost = 999,
        
    )

    copy_object_when_appropriate(default_historical_sale, overrides)
     
    return default_historical_sale

def create_historical_sale(
        context: TestContext,
        overrides: HistoricalSaleCreateModel | None = None, 
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ) -> HistoricalSaleModel:
    
    post_object: HistoricalSaleCreateModel = mint_default_historical_sale(context = context, overrides = overrides, request_operators = request_operators)

    result: Response = qa_post(context.api_url + "/historical_sales", post_object, request_operators)

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
                "sales_intake_job"
            ]
        )

        assert result_dict['id'] is not None
        assert result_dict['created_at'] is not None
        assert result_dict['updated_at'] is None
    
    return_object = HistoricalSaleModel(**result.json())
    
    return return_object 
 
def get_historical_sale_by_id(
        context: TestContext, 
        id: str,
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ) -> HistoricalSaleModel:

    url: str = f"{context.api_url}/historical_sales/{id}"
    
    result: Response = qa_get(url, request_operators=request_operators)
     
    return_object = HistoricalSaleModel(**result.json())
    
    return return_object 

def get_historical_sales(
        context: TestContext, 
        search_model: HistoricalSaleSearchModel | None,
        request_operators: RequestOperators | None = None 
    ) -> PagedResponseItemList[HistoricalSaleModel]: 

    url: str = f"{context.api_url}/historical_sales"
    
    result: Response = qa_get(
        url = url, 
        query_params = search_model if search_model is not None else {},
        request_operators = request_operators
    )
    
    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict['paging'])
     
    return_items: list[HistoricalSaleModel] = [HistoricalSaleModel(**obj) for obj in result_dict['items']]

    return_object = PagedResponseItemList[HistoricalSaleModel](
        items = return_items, paging = return_paging_object
    )
    
    return return_object 
 
def historical_sale_hydration_check(historical_sale: HistoricalSaleModel) -> None:
  
    assert historical_sale.retailer_location is not None
    assert historical_sale.retailer_location.id is not None
    assert historical_sale.retailer_location.id == historical_sale.retailer_location_id
    
    assert historical_sale.retailer is not None
    assert historical_sale.retailer.id is not None
    assert historical_sale.retailer.id == historical_sale.retailer_id
    
    assert historical_sale.sales_intake_job is not None
    assert historical_sale.sales_intake_job.id is not None 
    assert historical_sale.sales_intake_job.id == historical_sale.sales_intake_job_id         