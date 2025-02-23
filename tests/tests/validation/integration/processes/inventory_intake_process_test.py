from typing import Any

from tests.qdk.operators.inventory_intake_jobs import InventoryIntakeJobCreateModel, create_inventory_intake_job, get_inventory_intake_job_by_id, run_inventory_intake_job 
from tests.qdk.operators.inventory_product_snapshots import InventoryProductSnapshotCreateModel, InventoryProductSnapshotModel, InventoryProductSnapshotSearchModel, create_inventory_product_snapshot, get_inventory_product_snapshots
from tests.qdk.operators.pos_integrations import PosIntegrationCreateModel, create_pos_integration
from tests.qdk.operators.pos_simulator_responses import PosSimulatorResponseCreateModel
from tests.qdk.operators.products import ProductCreateModel, ProductSearchModel, get_products
from tests.qdk.types import RequestOperators, TestContext 
from tests.qdk.utils import generate_random_string
from util.configuration import get_global_configuration, populate_configuration_if_not_exists 

def test_intakes_new_products_when_not_recognized() -> None:
     
    populate_configuration_if_not_exists() 
     
    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    random_marker = generate_random_string(12, charset="abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    
    ######################################################
    ### Arrange
    ######################################################
    
    created_job = create_inventory_intake_job(
        context,
        overrides=InventoryIntakeJobCreateModel( 
            create_simulator_response_if_null=True,
            simulator_response=PosSimulatorResponseCreateModel(
                action_type="GetInventorySnapshots",
                response_body=get_new_products_test_json(random_marker)
            )
        ),
        request_operators=RequestOperators(hydration_properties=["simulator_response"])
    )
    
    create_pos_integration(
        context,
        PosIntegrationCreateModel(
            name=f"{random_marker} - Integration Name",
            pos_platform="Posabit",
            retailer_location_id=created_job.retailer_location_id
        )
    )
    
    ######################################################
    ### Act
    ######################################################
            
    job_run_result = run_inventory_intake_job(
        context,
        id=created_job.id
    )
    
    ######################################################
    ### Assert
    ######################################################
    
    # Assert Job was run
    
    run_job = get_inventory_intake_job_by_id(
        context,
        id=created_job.id,
        request_operators=RequestOperators(hydration_properties=["simulator_response"])
    )
    
    assert run_job.status == "Complete"
    
    # Assert three new products were created
    
    product_search_model_1 = ProductSearchModel(
        name=f"{random_marker} - Product Name 1"
    )
    
    product_1 = get_products(context, product_search_model_1)
    
    assert product_1.items is not None
    assert len(product_1.items) == 1
    assert product_1.items[0].name == f"{random_marker} - Product Name 1"
    assert product_1.items[0].id is not None 
    assert product_1.items[0].referring_retailer_location_id == created_job.retailer_location_id
    assert product_1.items[0].referring_retailer_id == created_job.retailer_id
    assert product_1.items[0].vendor_confirmation_status == "Candidate"
    
    product_search_model_2 = ProductSearchModel(
        name=f"{random_marker} - Product Name 2"
    )
    
    product_2 = get_products(context, product_search_model_2)
    
    assert product_2.items is not None
    assert len(product_2.items) == 1
    assert product_2.items[0].name == f"{random_marker} - Product Name 2"
    assert product_2.items[0].id is not None 
    assert product_2.items[0].referring_retailer_location_id == created_job.retailer_location_id
    assert product_2.items[0].referring_retailer_id == created_job.retailer_id
    assert product_2.items[0].vendor_confirmation_status == "Candidate"
    
    product_search_model_3 = ProductSearchModel(
        name=f"{random_marker} - Product Name 3"
    )
    
    product_3 = get_products(context, product_search_model_3)
    
    assert product_3.items is not None
    assert len(product_3.items) == 1    
    assert product_3.items[0].name == f"{random_marker} - Product Name 3"
    assert product_3.items[0].id is not None 
    assert product_3.items[0].referring_retailer_location_id == created_job.retailer_location_id
    assert product_3.items[0].referring_retailer_id == created_job.retailer_id
    assert product_3.items[0].vendor_confirmation_status == "Candidate"

    # Assert three new inventory snapshot items were created
        
    inventory_product_snapshot_search_model_1 = InventoryProductSnapshotSearchModel(
        product_ids=f"{product_1.items[0].id}"
    )
    
    inventory_product_snapshot_1 = get_inventory_product_snapshots(context, inventory_product_snapshot_search_model_1)
    
    assert inventory_product_snapshot_1.items is not None
    assert len(inventory_product_snapshot_1.items) == 1
    assert inventory_product_snapshot_1.items[0].id is not None 
    assert inventory_product_snapshot_1.items[0].inventory_intake_job_id == run_job.id 
    assert inventory_product_snapshot_1.items[0].product_id == product_1.items[0].id 
    assert inventory_product_snapshot_1.items[0].sku == f"{random_marker}-1111-1111"
    assert inventory_product_snapshot_1.items[0].price == 1000
    assert inventory_product_snapshot_1.items[0].retailer_id == run_job.retailer_id
    assert inventory_product_snapshot_1.items[0].retailer_location_id == run_job.retailer_location_id 
    assert inventory_product_snapshot_1.items[0].snapshot_hour == run_job.snapshot_hour 
    assert inventory_product_snapshot_1.items[0].stock_on_hand == 11.0
    
    inventory_product_snapshot_search_model_2 = InventoryProductSnapshotSearchModel(
        product_ids=f"{product_2.items[0].id}"
    )
    
    inventory_product_snapshot_2 = get_inventory_product_snapshots(context, inventory_product_snapshot_search_model_2)
    
    assert inventory_product_snapshot_2.items is not None
    assert len(inventory_product_snapshot_2.items) == 1
    assert inventory_product_snapshot_2.items[0].id is not None 
    assert inventory_product_snapshot_2.items[0].inventory_intake_job_id == run_job.id 
    assert inventory_product_snapshot_2.items[0].product_id == product_2.items[0].id 
    assert inventory_product_snapshot_2.items[0].sku == f"{random_marker}-2222-2222"
    assert inventory_product_snapshot_2.items[0].price == 2000
    assert inventory_product_snapshot_2.items[0].retailer_id == run_job.retailer_id
    assert inventory_product_snapshot_2.items[0].retailer_location_id == run_job.retailer_location_id 
    assert inventory_product_snapshot_2.items[0].snapshot_hour == run_job.snapshot_hour 
    assert inventory_product_snapshot_2.items[0].stock_on_hand == 22.0
    
    inventory_product_snapshot_search_model_3 = InventoryProductSnapshotSearchModel(
        product_ids=f"{product_3.items[0].id}"
    )
    
    inventory_product_snapshot_3 = get_inventory_product_snapshots(context, inventory_product_snapshot_search_model_3)
    
    assert inventory_product_snapshot_3.items is not None
    assert len(inventory_product_snapshot_3.items) == 1
    assert inventory_product_snapshot_3.items[0].id is not None 
    assert inventory_product_snapshot_3.items[0].inventory_intake_job_id == run_job.id 
    assert inventory_product_snapshot_3.items[0].product_id == product_3.items[0].id 
    assert inventory_product_snapshot_3.items[0].sku == f"{random_marker}-3333-3333"
    assert inventory_product_snapshot_3.items[0].price == 3000
    assert inventory_product_snapshot_3.items[0].retailer_id == run_job.retailer_id
    assert inventory_product_snapshot_3.items[0].retailer_location_id == run_job.retailer_location_id 
    assert inventory_product_snapshot_3.items[0].snapshot_hour == run_job.snapshot_hour 
    assert inventory_product_snapshot_3.items[0].stock_on_hand == 33.0
    

def test_intakes_and_links_to_existing_products_when_recognized() -> None:
     
    populate_configuration_if_not_exists() 
     
    context: TestContext = TestContext(api_url = get_global_configuration().API_URL)

    random_marker = generate_random_string(12, charset="abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    
    ######################################################
    ### Arrange
    ######################################################
     
    created_job = create_inventory_intake_job(
        context,
        overrides=InventoryIntakeJobCreateModel( 
            create_simulator_response_if_null=True,
            simulator_response=PosSimulatorResponseCreateModel(
                action_type="GetInventorySnapshots",
                response_body=get_new_products_test_json(random_marker)
            )
        ),
        request_operators=RequestOperators(hydration_properties=["simulator_response"])
    )
    
    retailer_location_id_to_use = created_job.retailer_location_id
 
    created_inventory_product_snapshot_1 = create_inventory_product_snapshot(
        context,
        InventoryProductSnapshotCreateModel(
            retailer_location_id=retailer_location_id_to_use,
            snapshot_hour=created_job.snapshot_hour,
            sku=f"{random_marker}-1111-1111",
            stock_on_hand=11.0,
            price=1000,
            product=ProductCreateModel(
                vendor_confirmation_status="ConfirmedByVendor",
                referring_retailer_location_id=retailer_location_id_to_use
            )
        )
    )
    
    created_inventory_product_snapshot_2 = create_inventory_product_snapshot(
        context,
        InventoryProductSnapshotCreateModel(
            retailer_location_id=retailer_location_id_to_use,
            snapshot_hour=created_job.snapshot_hour,
            sku=f"{random_marker}-2222-2222",
            stock_on_hand=22.0,
            price=2000,
            product=ProductCreateModel(
                vendor_confirmation_status="ConfirmedByVendor",
                referring_retailer_location_id=retailer_location_id_to_use
            )
        )
    )
     
    created_inventory_product_snapshot_3 = create_inventory_product_snapshot(
        context,
        InventoryProductSnapshotCreateModel(
            retailer_location_id=retailer_location_id_to_use,
            snapshot_hour=created_job.snapshot_hour,
            sku=f"{random_marker}-3333-3333",
            stock_on_hand=33.0,
            price=3000,
            product=ProductCreateModel(
                vendor_confirmation_status="ConfirmedByVendor",
                referring_retailer_location_id=retailer_location_id_to_use
            )
        )
    )
     
    create_pos_integration(
        context,
        PosIntegrationCreateModel(
            name=f"{random_marker} - Integration Name",
            pos_platform="Posabit",
            retailer_location_id=retailer_location_id_to_use
        )
    )
    
    ######################################################
    ### Act
    ######################################################
            
    job_run_result = run_inventory_intake_job(
        context,
        id=created_job.id
    )
    
    ######################################################
    ### Assert
    ######################################################
    
    # Assert Job was run
    
    run_job = get_inventory_intake_job_by_id(
        context,
        id=created_job.id,
        request_operators=RequestOperators(hydration_properties=["simulator_response"])
    )
    
    assert run_job.status == "Complete"
    
    # Assert NO new products were created, and only the ones we created beforehand exist.
    
    products_search_model = ProductSearchModel(
        referring_retailer_location_ids=f"{created_job.retailer_location_id}",
    )
    
    products = get_products(context, products_search_model)
    
    assert products.items is not None
    assert len(products.items) == 3
    
    # Assert new snapshots match old ones
    
    snapshot_search_model = InventoryProductSnapshotSearchModel(
        inventory_intake_job_ids=f"{created_job.id}"
    )
    
    snapshots_from_job = get_inventory_product_snapshots(context, snapshot_search_model)
    
    assert snapshots_from_job.items is not None
    assert len(snapshots_from_job.items) == 3
    
    snapshot_1: list[InventoryProductSnapshotModel] = [item for item in snapshots_from_job.items if item.product_id == products.items[0].id]
    assert len(snapshot_1) == 1
    
    snapshot_2: list[InventoryProductSnapshotModel] = [item for item in snapshots_from_job.items if item.product_id == products.items[1].id]
    assert len(snapshot_2) == 1
    
    snapshot_3: list[InventoryProductSnapshotModel] = [item for item in snapshots_from_job.items if item.product_id == products.items[2].id]
    assert len(snapshot_3) == 1
    
    
    
    
     
    # Assert our three snapshots were created and link to the products they match with
    # 
     
def get_new_products_test_json(marker: str) -> dict[str, Any]:

    return {
        "total_records": 3,
        "current_page": 1,
        "total_pages": 1,
        "per_page": 1000,
        "inventory": [
        { 
            "name": f"{marker} - Product Name 1", 
            "price": 1000, 
            "quantity_on_hand": "11.0", 
            "vendor": "Vendor 1", 
            "brand": "Test Brand 1",
            "category": "Test Category 1", 
            "sku": f"{marker}-1111-1111",
        },
        {
            "name": f"{marker} - Product Name 2", 
            "price": 2000, 
            "quantity_on_hand": "22.0", 
            "vendor": "Vendor 2", 
            "brand": "Test Brand 2",
            "category": "Test Category 2", 
            "sku": f"{marker}-2222-2222",
        },
        {
            "name": f"{marker} - Product Name 3", 
            "price": 3000, 
            "quantity_on_hand": "33.0", 
            "vendor": "Vendor 3", 
            "brand": "Test Brand 3",
            "category": "Test Category 3", 
            "sku": f"{marker}-3333-3333",
        }]
    }