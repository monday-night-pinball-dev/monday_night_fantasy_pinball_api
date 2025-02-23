
from uuid import UUID

from models.historical_sale_model import HistoricalSaleModel, HistoricalSaleSearchModel
from models.inventory_product_snapshot_model import InventoryProductSnapshotModel, InventoryProductSnapshotSearchModel
from util.common import RequestOperators 
import managers.managers as managers 

class ProcessException(Exception):
    def __init__(
        self, 
        process_name, 
        process_id, 
        step, 
        message: str
    ):
        concatenated_message = f"Exception occured in process {process_name} with id {process_id} in Step {step}: {message}"
        
        self.process_name = process_name
        self.process_id = process_id
        self.step = step
        
        super().__init__(concatenated_message)
        
class CommonProcessUtilities:
    
    def __init__(
        self,
        manager: managers.Manager = managers.Manager()
    ):
        self.manager = manager
        
    
    def retrieve_existing_snapshot_or_sale(
        self,
        retailer_location_id: UUID,
        sku: str
    ) -> InventoryProductSnapshotModel | HistoricalSaleModel | None:
        existing_snapshot_item_search_model = InventoryProductSnapshotSearchModel(
            retailer_location_ids = [retailer_location_id],
            sku = sku,
        )
        
        requestOperators = RequestOperators(
            hydration=['product']
        )
   
        existing_snapshot = self.manager.search_inventory_product_snapshots(existing_snapshot_item_search_model, None, requestOperators)
        
        if(existing_snapshot is not None and len(existing_snapshot.items) > 0):
            return existing_snapshot.items[0] 
        
        else:
            existing_sales = self.manager.search_historical_sales(HistoricalSaleSearchModel(
                retailer_location_ids = [retailer_location_id],
                sku = sku,
            ))
            
            return existing_sales.items[0] if existing_sales is not None and len(existing_sales.items) > 0 else None
            
     