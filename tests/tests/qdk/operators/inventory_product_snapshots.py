import datetime

from requests import Response 
from tests.qdk.operators.inventory_intake_jobs import InventoryIntakeJobCreateModel, InventoryIntakeJobModel, create_inventory_intake_job
from tests.qdk.operators.products import ProductModel, create_product
from tests.qdk.operators.retailer_locations import RetailerLocationCreateModel, RetailerLocationModel, create_retailer_location
from tests.qdk.operators.retailers import RetailerModel
from tests.qdk.operators.vendors import VendorModel
from tests.qdk.qa_requests import qa_get, qa_patch, qa_post
from tests.qdk.types import PagedResponseItemList, PagingResponseModel, PagingRequestModel, RequestOperators, TestContext
from tests.qdk.utils import assert_object_was_updated, assert_objects_are_equal, copy_object_when_appropriate, generate_random_string
 
class InventoryProductSnapshotCreateModel():  

    def __init__(
        self, 
        retailer_location_id: str | None = None,
        retailer_location: RetailerLocationCreateModel | None = None,
        product_id: str | None = None,
        product: RetailerLocationCreateModel | None = None,
        inventory_intake_job_id: str | None = None,
        inventory_intake_job: InventoryIntakeJobCreateModel | None = None,
        create_inventory_intake_job_if_null: bool | None = False, 
        snapshot_hour: str | None = None,
        sku: str | None = None,
        stock_on_hand: int | None = None,
        price: int | None = None, 
    ) -> None:
         
        self.retailer_location_id = retailer_location_id
        self.retailer_location = retailer_location
        self.product_id = product_id
        self.product = product
        self.inventory_intake_job_id = inventory_intake_job_id
        self.inventory_intake_job = inventory_intake_job
        self.create_inventory_intake_job_if_null = create_inventory_intake_job_if_null
        self.snapshot_hour = snapshot_hour
        self.sku = sku
        self.stock_on_hand = stock_on_hand
        self.price = price 
          
class InventoryProductSnapshotModel():  

    def __init__(self, 
        id: str, 
        retailer_location_id: str,
        retailer_id: str,
        product_id: str,
        snapshot_hour: str ,
        sku: str ,
        stock_on_hand: int ,
        price: int ,
        created_at: datetime.datetime,
        retailer_location: RetailerLocationModel | None = None,
        retailer: RetailerModel | None = None,
        vendor_id: str | None = None,
        vendor: VendorModel | None = None, 
        product: RetailerLocationModel | None = None,
        inventory_intake_job_id: str | None = None,
        inventory_intake_job: InventoryIntakeJobModel | None = None,   
        updated_at: datetime.datetime | None = None,
    ) -> None:
        
            self.id = id
            self.retailer_location_id = retailer_location_id
            self.retailer_id = retailer_id
            self.product_id = product_id
            self.snapshot_hour = snapshot_hour
            self.sku = sku
            self.stock_on_hand = stock_on_hand
            self.price = price
            self.created_at = created_at
            self.retailer_location = RetailerLocationModel(**retailer_location) if retailer_location is not None else None
            self.retailer = RetailerModel(**retailer) if retailer is not None else None
            self.vendor_id = vendor_id
            self.vendor = VendorModel(**vendor) if vendor is not None else None
            self.product = ProductModel(**product) if product is not None else None
            self.inventory_intake_job_id = inventory_intake_job_id
            self.inventory_intake_job = InventoryIntakeJobModel(**inventory_intake_job) if inventory_intake_job is not None else None
            self.updated_at = updated_at
 
        
class InventoryProductSnapshotSearchModel(PagingRequestModel):  

    def __init__(self, 
                ids: str | None = None,  
                retailer_ids: str | None = None,  
                retailer_location_ids: str | None = None,  
                product_ids: str | None = None,  
                vendor_ids: str | None = None,  
                inventory_intake_job_ids: str | None = None,  
                snapshot_hour_min: str | None = None,
                snapshot_hour_max: str | None = None,
                sku: str | None = None, 
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
        self.product_ids = product_ids 
        self.vendor_ids = vendor_ids 
        self.inventory_intake_job_ids = inventory_intake_job_ids 
        self.snapshot_hour_min = snapshot_hour_min
        self.snapshot_hour_max = snapshot_hour_max
        self.sku = sku 
 
 
def mint_default_inventory_product_snapshot(
    context: TestContext, 
    overrides: InventoryProductSnapshotCreateModel | None = None, 
    request_operators: RequestOperators | None = None
) -> InventoryProductSnapshotCreateModel: 
    random_string = generate_random_string()

    overrides = overrides or InventoryProductSnapshotCreateModel()
    
    if(overrides.retailer_location_id is None):

        new_retailer_location = create_retailer_location(context, overrides.retailer_location, request_operators = request_operators)
        overrides.retailer_location_id = new_retailer_location.id

        del overrides.retailer_location
        
    if(overrides.product_id is None):

        new_product = create_product(context, overrides.product, request_operators = request_operators)
        overrides.product_id = new_product.id

        del overrides.product
    
    if(overrides.inventory_intake_job_id is None and overrides.create_inventory_intake_job_if_null is True):

        new_inventory_intake_job = create_inventory_intake_job(context, overrides.inventory_intake_job, request_operators = request_operators)
        overrides.inventory_intake_job_id = new_inventory_intake_job.id

        del overrides.inventory_intake_job
 
        
    default_inventory_product_snapshot: InventoryProductSnapshotCreateModel = InventoryProductSnapshotCreateModel(
        snapshot_hour = "2021-01-01T01:01:01.000Z",
        sku = "abcdefghijklmonpqrstuvwxyz1234567890",
        stock_on_hand = 44,
        price = 1234, 
    )

    copy_object_when_appropriate(default_inventory_product_snapshot, overrides)
     
    return default_inventory_product_snapshot

def create_inventory_product_snapshot(
        context: TestContext,
        overrides: InventoryProductSnapshotCreateModel | None = None, 
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ) -> InventoryProductSnapshotModel:
    
    post_object: InventoryProductSnapshotCreateModel = mint_default_inventory_product_snapshot(context = context, overrides = overrides, request_operators = request_operators)

    result: Response = qa_post(context.api_url + "/inventory_product_snapshots", post_object, request_operators)

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
                "product_id",
                "product",
                "inventory_intake_job_id",
                "inventory_intake_job",
                "vendor_id",
                "vendor",  
            ]
        )

        assert result_dict['id'] is not None
        assert result_dict['created_at'] is not None
        assert result_dict['updated_at'] is None
    
    return_object = InventoryProductSnapshotModel(**result.json())
    
    return return_object 
 
def get_inventory_product_snapshot_by_id(
        context: TestContext, 
        id: str,
        request_operators: RequestOperators | None = None,
        allow_failures: bool = False
        ) -> InventoryProductSnapshotModel:

    url: str = f"{context.api_url}/inventory_product_snapshots/{id}"
    
    result: Response = qa_get(url, request_operators = request_operators)
     
    return_object = InventoryProductSnapshotModel(**result.json())
    
    return return_object 

def get_inventory_product_snapshots(
        context: TestContext, 
        search_model: InventoryProductSnapshotSearchModel | None,
        request_operators: RequestOperators | None = None 
    ) -> PagedResponseItemList[InventoryProductSnapshotModel]: 

    url: str = f"{context.api_url}/inventory_product_snapshots"
    
    result: Response = qa_get(
        url = url, 
        query_params = search_model if search_model is not None else {},
        request_operators = request_operators
    )
    
    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict['paging'])
     
    return_items: list[InventoryProductSnapshotModel] = [InventoryProductSnapshotModel(**obj) for obj in result_dict['items']]

    return_object = PagedResponseItemList[InventoryProductSnapshotModel](
        items = return_items, paging = return_paging_object
    )
    
    return return_object 
 
def inventory_product_snapshot_hydration_check(snapshot: InventoryProductSnapshotModel) -> None:
    assert snapshot.retailer is not None
    assert snapshot.retailer.id is not None
    assert snapshot.retailer.id == snapshot.retailer_id
     
    assert snapshot.retailer_location is not None
    assert snapshot.retailer_location.id is not None
    assert snapshot.retailer_location.id == snapshot.retailer_location_id
     
    assert snapshot.inventory_intake_job is not None
    assert snapshot.inventory_intake_job.id is not None
    assert snapshot.inventory_intake_job.id == snapshot.inventory_intake_job_id
     
    assert snapshot.vendor is not None
    assert snapshot.vendor.id is not None
    assert snapshot.vendor.id == snapshot.vendor_id

    assert snapshot.product is not None
    assert snapshot.product.id is not None
    assert snapshot.product.id == snapshot.product_id
 