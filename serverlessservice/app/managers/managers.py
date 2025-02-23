import json
from typing import Any 
 
from uuid import UUID 

from data_accessors.historical_sale_accessor import HistoricalSaleDataAccessor 
from data_accessors.historical_sale_item_accessor import HistoricalSaleItemDataAccessor
from data_accessors.inventory_intake_batch_job_accessor import InventoryIntakeBatchJobDataAccessor
from data_accessors.inventory_intake_job_accessor import InventoryIntakeJobDataAccessor
from data_accessors.inventory_product_snapshot_accessor import InventoryProductSnapshotDataAccessor
from data_accessors.pos_integration_accessor import PosIntegrationDataAccessor
from data_accessors.pos_integration_call_accessor import PosIntegrationCallDataAccessor
from data_accessors.pos_simulator_response_accessor import PosSimulatorResponseDataAccessor
from data_accessors.product_accessor import ProductDataAccessor
from data_accessors.retailer_accessor import RetailerDataAccessor
from data_accessors.retailer_location_accessor import RetailerLocationDataAccessor
from data_accessors.sales_intake_batch_job_accessor import SalesIntakeBatchJobDataAccessor
from data_accessors.sales_intake_job_accessor import SalesIntakeJobDataAccessor   
from data_accessors.vendor_accessor import VendorDataAccessor   
from data_accessors.user_accessor import UserDataAccessor 

from models.historical_sale_item_model import (
    HistoricalSaleItemCreateModel,
    HistoricalSaleItemModel,
    HistoricalSaleItemSearchModel, 
)

from models.common_model import ItemList

from models.inventory_intake_batch_job_model import (   
    InventoryIntakeBatchJobCreateModel, 
    InventoryIntakeBatchJobModel, 
    InventoryIntakeBatchJobSearchModel, 
    InventoryIntakeBatchJobStatuses, 
    InventoryIntakeBatchJobUpdateModel
)
from models.inventory_intake_job_model import (   
    InventoryIntakeJobCreateModel, 
    InventoryIntakeJobModel, 
    InventoryIntakeJobSearchModel, 
    InventoryIntakeJobStatuses, 
    InventoryIntakeJobUpdateModel
)
from models.inventory_product_snapshot_model import (   
    InventoryProductSnapshotCreateModel, 
    InventoryProductSnapshotModel, 
    InventoryProductSnapshotSearchModel
)
from models.pos_integration_call_model import (   
    PosIntegrationCallCreateModel, 
    PosIntegrationCallModel, 
    PosIntegrationCallSearchModel
)            
from models.pos_integration_model import (   
    PosIntegrationCreateModel, 
    PosIntegrationModel, 
    PosIntegrationSearchModel, 
    PosIntegrationUpdateModel, 
    PosPlatforms
)
from models.pos_simulator_response_model import PosSimulatorResponseCreateModel, PosSimulatorResponseModel, PosSimulatorResponseSearchModel
from models.product_model import (   
    ProductCreateModel, 
    ProductModel, 
    ProductSearchModel, 
    ProductUpdateModel
)
from models.sales_intake_batch_job_model import (   
    SalesIntakeBatchJobCreateModel, 
    SalesIntakeBatchJobModel, 
    SalesIntakeBatchJobSearchModel, 
    SalesIntakeBatchJobStatuses, 
    SalesIntakeBatchJobUpdateModel
)
from models.sales_intake_job_model import (   
    SalesIntakeJobCreateModel, 
    SalesIntakeJobModel, 
    SalesIntakeJobSearchModel, 
    SalesIntakeJobStatuses, 
    SalesIntakeJobUpdateModel
)
from models.historical_sale_model import (   
    HistoricalSaleCreateModel, 
    HistoricalSaleModel, 
    HistoricalSaleSearchModel
)
from models.user_model import (   
    UserCreateModel, 
    UserModel, 
    UserSearchModel, 
    UserUpdateModel
)
from models.vendor_model import (   
    VendorCreateModel, 
    VendorModel, 
    VendorSearchModel, 
    VendorUpdateModel
)
from models.retailer_location_model import (   
    RetailerLocationCreateModel, 
    RetailerLocationModel, 
    RetailerLocationSearchModel, 
    RetailerLocationUpdateModel
)
from models.retailer_model import (   
    RetailerCreateModel, 
    RetailerModel, 
    RetailerSearchModel, 
    RetailerUpdateModel
)
from models.sales_intake_batch_job_model import (   
    SalesIntakeBatchJobCreateModel, 
    SalesIntakeBatchJobModel, 
    SalesIntakeBatchJobSearchModel, 
    SalesIntakeBatchJobStatuses, 
    SalesIntakeBatchJobUpdateModel
)
from models.sales_intake_job_model import (   
    SalesIntakeJobCreateModel, 
    SalesIntakeJobModel, 
    SalesIntakeJobSearchModel, 
    SalesIntakeJobStatuses, 
    SalesIntakeJobUpdateModel
)
from models.user_model import (   
    UserCreateModel, 
    UserModel, 
    UserSearchModel, 
    UserUpdateModel
)
from models.vendor_model import (   
    VendorCreateModel, 
    VendorModel, 
    VendorSearchModel, 
    VendorUpdateModel
)

from util.database import PagingModel  
from util.common import RequestOperators
from util.hydration import Hydrator 
 
 
 
class Manager:

    def __init__(
        self,  
        hydrator: Hydrator = Hydrator(),
        historical_sale_item_accessor: HistoricalSaleItemDataAccessor = HistoricalSaleItemDataAccessor(),
        historical_sale_accessor: HistoricalSaleDataAccessor = HistoricalSaleDataAccessor(),
        retailer_location_accessor: RetailerLocationDataAccessor = RetailerLocationDataAccessor(),
        retailer_accessor: RetailerDataAccessor = RetailerDataAccessor(),
        product_accessor: ProductDataAccessor = ProductDataAccessor(), 
        historical_sales_accessor: HistoricalSaleDataAccessor = HistoricalSaleDataAccessor(),   
        pos_integration_accessor: PosIntegrationDataAccessor = PosIntegrationDataAccessor(),
        pos_integration_call_accessor: PosIntegrationCallDataAccessor = PosIntegrationCallDataAccessor(),
        pos_simulator_response_accessor: PosSimulatorResponseDataAccessor = PosSimulatorResponseDataAccessor(), 
        inventory_intake_batch_job_accessor: InventoryIntakeBatchJobDataAccessor = InventoryIntakeBatchJobDataAccessor(),
        inventory_intake_job_accessor: InventoryIntakeJobDataAccessor = InventoryIntakeJobDataAccessor(),
        sales_intake_job_accessor: SalesIntakeJobDataAccessor = SalesIntakeJobDataAccessor(),
        sales_intake_batch_job_accessor: SalesIntakeBatchJobDataAccessor = SalesIntakeBatchJobDataAccessor(),
        inventory_product_snapshot_accessor: InventoryProductSnapshotDataAccessor = InventoryProductSnapshotDataAccessor(), 
        user_accessor: UserDataAccessor = UserDataAccessor(),
        vendor_accessor: VendorDataAccessor = VendorDataAccessor(), 
        
    ) -> None: 
        
        self.hydrator = hydrator

        self.historical_sale_item_accessor = historical_sale_item_accessor
        self.historical_sale_accessor = historical_sale_accessor
        self.retailer_location_accessor = retailer_location_accessor
        self.retailer_accessor = retailer_accessor
        self.product_accessor = product_accessor
        self.historical_sales_accessor = historical_sales_accessor
        self.pos_integration_accessor = pos_integration_accessor
        self.pos_integration_call_accessor = pos_integration_call_accessor
        self.pos_simulator_response_accessor = pos_simulator_response_accessor 
        self.inventory_intake_batch_job_accessor = inventory_intake_batch_job_accessor
        self.inventory_intake_job_accessor = inventory_intake_job_accessor
        self.sales_intake_job_accessor = sales_intake_job_accessor
        self.sales_intake_batch_job_accessor = sales_intake_batch_job_accessor
        self.inventory_product_snapshot_accessor = inventory_product_snapshot_accessor
        self.user_accessor = user_accessor
        self.vendor_accessor = vendor_accessor 
         
        
    def create_historical_sale_item(
        self, 
        inbound_model: HistoricalSaleItemCreateModel,
        request_operators: RequestOperators | None = None
    ) -> HistoricalSaleItemModel | None:
 
        # Denormalize product_vendor_id
        
        referenced_product = self.get_product_by_id(
            inbound_model.product_id,
            request_operators=request_operators
        )
        
        inbound_model.product_vendor_id = referenced_product.vendor_id
        
        # Denormalize intake_job_id, retailer_location_id, and retailer_id

        referenced_historical_sale = self.get_historical_sale_by_id(inbound_model.historical_sale_id)
        
        inbound_model.retailer_id = referenced_historical_sale.retailer_id
        inbound_model.retailer_location_id = referenced_historical_sale.retailer_location_id
        inbound_model.sales_intake_job_id = referenced_historical_sale.sales_intake_job_id
        
        result = self.historical_sale_item_accessor.insert(
            model = inbound_model,
            request_operators = request_operators
        )
        
        self.hydrate_historical_sale_items([result], request_operators)
        
        return result

    def get_historical_sale_item_by_id(
        self, 
        id: UUID, 
        request_operators: RequestOperators | None = None
    ) -> HistoricalSaleItemModel | None:

        result = self.historical_sale_item_accessor.select_by_id(
            id = id,
            request_operators = request_operators
        )

        self.hydrate_historical_sale_items([result], request_operators)
        
        return result

    def search_historical_sale_items(
        self,
        model: HistoricalSaleItemSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None
    ) -> ItemList[HistoricalSaleItemModel]:

        result = self.historical_sale_item_accessor.select(
            model = model,
            paging_model = paging_model,
            request_operators = request_operators
        )
        
        self.hydrate_historical_sale_items(result.items, request_operators)
        
        return result
 

    def delete_historical_sale_item(
        self, 
        id: UUID, 
        request_operators: RequestOperators | None = None
    ) -> HistoricalSaleItemModel | None:

        result: None | HistoricalSaleItemModel = self.historical_sale_item_accessor.delete(
            id = id,
            request_operators = request_operators
        )

        return result

    def hydrate_historical_sale_items(
        self,
        result_list: list[HistoricalSaleItemModel],
        request_operators: RequestOperators | None = None
    ): 
        # Hydrate retailer 
        self.hydrator.hydrate_target(
            "retailer", 
            result_list, 
            RetailerSearchModel(),
            self.search_retailers,
            request_operators.hydration if request_operators is not None else None
        )
        
        # hydrate retailer location
        self.hydrator.hydrate_target(
            "retailer_location", 
            result_list, 
            RetailerLocationSearchModel(),
            self.search_retailer_locations,
            request_operators.hydration if request_operators is not None else None
        )
        
        # hydrate pos integration
        self.hydrator.hydrate_target(
            "product", 
            result_list, 
            ProductSearchModel(),
            self.search_products,
            request_operators.hydration if request_operators is not None else None
        )
        
        # hydrate historical sale
        self.hydrator.hydrate_target(
            "historical_sale", 
            result_list, 
            HistoricalSaleSearchModel(),
            self.search_historical_sales,
            request_operators.hydration if request_operators is not None else None
        )
        
        # hydrate sales intake job
        self.hydrator.hydrate_target(
            "sales_intake_job", 
            result_list, 
            SalesIntakeJobSearchModel(),
            self.search_sales_intake_jobs,
            request_operators.hydration if request_operators is not None else None
        )
        
        # hydrate vendor
        self.hydrator.hydrate_target(
            "product_vendor", 
            result_list, 
            VendorSearchModel(),
            self.search_vendors,
            request_operators.hydration if request_operators is not None else None
        ) 
 
    def create_historical_sale(
        self, 
        inbound_model: HistoricalSaleCreateModel,
        request_operators: RequestOperators | None = None
    ) -> HistoricalSaleModel | None:

        # Denormalize retailer_id
        
        referenced_retailer_location = self.retailer_location_accessor.select_by_id(inbound_model.retailer_location_id)
        
        inbound_model.retailer_id = referenced_retailer_location.retailer_id
         
        result = self.historical_sale_accessor.insert(
            model = inbound_model,
            request_operators = request_operators
        )
        
        self.hydrate_historical_sales([result], request_operators)
        
        return result

    def get_historical_sale_by_id(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> HistoricalSaleModel | None:

        result = self.historical_sale_accessor.select_by_id(
            id = id,
            request_operators = request_operators
        )

        self.hydrate_historical_sales([result], request_operators)
        
        return result

    def search_historical_sales(
        self,
        model: HistoricalSaleSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None
    ) -> ItemList[HistoricalSaleModel]:

        result = self.historical_sale_accessor.select(
            model = model,
            paging_model = paging_model,
            request_operators = request_operators
       )

        self.hydrate_historical_sales(result.items, request_operators)
        
        return result 

    def delete_historical_sale(
        self, 
        id: UUID,        
        request_operators: RequestOperators | None = None
    ) -> HistoricalSaleModel | None:

        result: None | HistoricalSaleModel = self.historical_sale_accessor.delete(
            id = id,
            request_operators = request_operators
        )
 
        return result
 
    def hydrate_historical_sales(
        self,
        result_list: list[HistoricalSaleModel],
        request_operators: RequestOperators | None = None
    ):
        
        # Hydrate retailer 
        self.hydrator.hydrate_target(
            "retailer", 
            result_list, 
            RetailerSearchModel(),
            self.search_retailers,
            request_operators.hydration if request_operators is not None else None
        )
        
        # hydrate retailer location
        self.hydrator.hydrate_target(
            "retailer_location", 
            result_list, 
            RetailerLocationSearchModel(),
            self.search_retailer_locations,
            request_operators.hydration if request_operators is not None else None
        )
 
        # hydrate sales intake job
        self.hydrator.hydrate_target(
            "sales_intake_job", 
            result_list, 
            SalesIntakeJobSearchModel(),
            self.search_sales_intake_jobs,
            request_operators.hydration if request_operators is not None else None
        ) 
 
    def create_inventory_intake_batch_job(
        self, 
        inbound_model: InventoryIntakeBatchJobCreateModel,
        request_operators: RequestOperators | None = None
    ) -> InventoryIntakeBatchJobModel | None:
 
        result = self.inventory_intake_batch_job_accessor.insert(
            model = inbound_model,
            request_operators = request_operators
        )

        self.hydrate_inventory_intake_batch_jobs([result], request_operators)
        
        return result

    def get_inventory_intake_batch_job_by_id(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> InventoryIntakeBatchJobModel | None:

        result = self.inventory_intake_batch_job_accessor.select_by_id(
            id = id,
            request_operators = request_operators
        )

        self.hydrate_inventory_intake_batch_jobs([result], request_operators)
        
        return result

    def search_inventory_intake_batch_jobs(
        self,
        model: InventoryIntakeBatchJobSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None
    ) -> ItemList[InventoryIntakeBatchJobModel]:

        result = self.inventory_intake_batch_job_accessor.select(
            model = model,
            paging_model = paging_model,
            request_operators = request_operators
       )

        self.hydrate_inventory_intake_batch_jobs(result.items, request_operators)
        
        return result

    def update_inventory_intake_batch_job(
        self,
        id: UUID,
        model: InventoryIntakeBatchJobUpdateModel, 
        request_operators: RequestOperators | None = None
    ) -> InventoryIntakeBatchJobModel | None: 

        result = self.inventory_intake_batch_job_accessor.update(id, model,request_operators=request_operators)

        self.hydrate_inventory_intake_batch_jobs([result], request_operators)
        
        return result

    def delete_inventory_intake_batch_job(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> InventoryIntakeBatchJobModel | None:

        result: None | InventoryIntakeBatchJobModel = self.inventory_intake_batch_job_accessor.delete(
            id = id,
            request_operators = request_operators
        )

        return result
     
    def hydrate_inventory_intake_batch_jobs(
        self,
        result_list: list[InventoryIntakeBatchJobModel],
        request_operators: RequestOperators | None = None
    ): 
        return
 
    def create_inventory_intake_job(
            self, 
            inbound_model: InventoryIntakeJobCreateModel,
            request_operators: RequestOperators | None = None
    ) -> InventoryIntakeJobModel | None:

        # Denormalize retailer_id
        
        referenced_retailer_location = self.get_retailer_location_by_id(inbound_model.retailer_location_id)
        
        if(referenced_retailer_location is None):
            raise Exception(f"Retailer Location with id {inbound_model.retailer_location_id} not found.")
        
        inbound_model.retailer_id = referenced_retailer_location.retailer_id

        result = self.inventory_intake_job_accessor.insert(
            model = inbound_model,
            request_operators = request_operators
        )
        
        self.hydrate_inventory_intake_job([result], request_operators)

        return result

    def get_inventory_intake_job_by_id(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> InventoryIntakeJobModel | None:

        result = self.inventory_intake_job_accessor.select_by_id(
            id = id,
            request_operators = request_operators
        )

        self.hydrate_inventory_intake_job([result], request_operators)
        
        return result

    def search_inventory_intake_jobs(
        self,
        model: InventoryIntakeJobSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None
    ) -> ItemList[InventoryIntakeJobModel]:

        result = self.inventory_intake_job_accessor.select(
            model = model,
            paging_model = paging_model,
            request_operators = request_operators
        )

        self.hydrate_inventory_intake_job(result.items, request_operators)

        return result

    def update_inventory_intake_job(
        self,
        id: UUID,
        model: InventoryIntakeJobUpdateModel, 
        request_operators: RequestOperators | None = None
    ) -> InventoryIntakeJobModel | None:
 
        result = self.inventory_intake_job_accessor.update(
            id = id,
            model = model, 
            request_operators = request_operators
        )
        
        self.hydrate_inventory_intake_job([result], request_operators)

        return result

    def delete_inventory_intake_job(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> InventoryIntakeJobModel | None:

        result: None | InventoryIntakeJobModel = self.inventory_intake_job_accessor.delete(
            id = id,
            request_operators = request_operators
        )

        return result
     
    def hydrate_inventory_intake_job(
        self,
        result_list: list[InventoryIntakeJobModel],
        request_operators: RequestOperators | None = None
    ):
        
        # Hydrate retailer 
        self.hydrator.hydrate_target(
            "retailer", 
            result_list, 
            RetailerSearchModel(),
            self.search_retailers,
            request_operators.hydration if request_operators is not None else None
        )
        
        # hydrate retailer location
        self.hydrator.hydrate_target(
            "retailer_location", 
            result_list, 
            RetailerLocationSearchModel(),
            self.search_retailer_locations,
            request_operators.hydration if request_operators is not None else None
        )
 
        # hydrate parent batch job
        self.hydrator.hydrate_target(
            "parent_batch_job",
            result_list, 
            InventoryIntakeBatchJobSearchModel(),
            self.search_inventory_intake_batch_jobs,
            request_operators.hydration if request_operators is not None else None
        ) 
 
  
        # hydrate parent batch job
        self.hydrator.hydrate_target(
            "simulator_response",
            result_list, 
            PosSimulatorResponseSearchModel(),
            self.search_pos_simulator_responses,
            request_operators.hydration if request_operators is not None else None
        ) 
 
    def create_inventory_product_snapshot(
        
        self, 
        inbound_model: InventoryProductSnapshotCreateModel,
        request_operators: RequestOperators | None = None
    ) -> InventoryProductSnapshotModel | None:

        # Denormalize retailer_id
        
        referenced_retailer_location = self.get_retailer_location_by_id(inbound_model.retailer_location_id)
        
        inbound_model.retailer_id = referenced_retailer_location.retailer_id
        
        # Denormalize product_id
        
        referenced_product = self.get_product_by_id(inbound_model.product_id)
        
        inbound_model.vendor_id = referenced_product.vendor_id

        result = self.inventory_product_snapshot_accessor.insert(
            model = inbound_model,
            request_operators = request_operators
        )
        
        self.hydrate_inventory_product_snapshots([result], request_operators)

        return result

    def get_inventory_product_snapshot_by_id(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> InventoryProductSnapshotModel | None:

        result = self.inventory_product_snapshot_accessor.select_by_id(
            id = id,
            request_operators = request_operators
        )

        self.hydrate_inventory_product_snapshots([result], request_operators)
        
        return result

    def search_inventory_product_snapshots(
        self,
        model: InventoryProductSnapshotSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None
    ) -> ItemList[InventoryProductSnapshotModel]:

        result = self.inventory_product_snapshot_accessor.select(
            model = model,
            paging_model = paging_model,
            request_operators = request_operators
       )

        self.hydrate_inventory_product_snapshots(result.items, request_operators)
        
        return result
 

    def delete_inventory_product_snapshot(
        self, 
        id: UUID, 
        request_operators: RequestOperators | None = None
    ) -> InventoryProductSnapshotModel | None:

        result: None | InventoryProductSnapshotModel = self.inventory_product_snapshot_accessor.delete(
            id = id,
            request_operators = request_operators
        )

        return result

    def hydrate_inventory_product_snapshots(
        self,
        result_list: list[InventoryProductSnapshotSearchModel],
        request_operators: RequestOperators | None = None
    ):
        
        # Hydrate retailer 
        self.hydrator.hydrate_target(
            "retailer", 
            result_list, 
            RetailerSearchModel(),
            self.search_retailers,
            request_operators.hydration if request_operators is not None else None
        )
        
        # hydrate retailer location
        self.hydrator.hydrate_target(
            "retailer_location", 
            result_list, 
            RetailerLocationSearchModel(),
            self.search_retailer_locations,
            request_operators.hydration if request_operators is not None else None
        )
 
        # hydrate sales intake job
        self.hydrator.hydrate_target(
            "inventory_intake_job",
            result_list, 
            InventoryIntakeJobSearchModel(),
            self.search_inventory_intake_jobs,
            request_operators.hydration if request_operators is not None else None
        ) 
        
        # hydrate sales intake job
        self.hydrator.hydrate_target(
            "product",
            result_list, 
            ProductSearchModel(),
            self.search_products,
            request_operators.hydration if request_operators is not None else None
        ) 
        
        # hydrate sales intake job
        self.hydrator.hydrate_target(
            "vendor",
            result_list, 
            VendorSearchModel(),
            self.search_vendors,
            request_operators.hydration if request_operators is not None else None
        ) 

 
    def create_pos_integration_call(
        self, 
        inbound_model: PosIntegrationCallCreateModel,
        request_operators: RequestOperators | None = None
    ) -> PosIntegrationCallModel | None:

        # Denormalize retailer_id
        
        pos_integration = self.get_pos_integration_by_id(inbound_model.pos_integration_id)
        
        inbound_model.retailer_id = pos_integration.retailer_id
        inbound_model.retailer_location_id = pos_integration.retailer_location_id

        result = self.pos_integration_call_accessor.insert(
            model = inbound_model,
            request_operators = request_operators
        )
        
        self.hydrate_pos_integration_calls([result], request_operators)

        return result

    def get_pos_integration_call_by_id(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> PosIntegrationCallModel | None:

        result = self.pos_integration_call_accessor.select_by_id(
            id = id,
            request_operators = request_operators
        )

        self.hydrate_pos_integration_calls([result], request_operators)
        
        return result

    def search_pos_integration_calls(
        self,
        model: PosIntegrationCallSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None
    ) -> ItemList[PosIntegrationCallModel]:

        result = self.pos_integration_call_accessor.select(
            model = model,
            paging_model = paging_model,
            request_operators = request_operators
        )
        
        self.hydrate_pos_integration_calls(result.items, request_operators)
        
        return result

    def delete_pos_integration_call(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> PosIntegrationCallModel | None:

        result: None | PosIntegrationCallModel = self.pos_integration_call_accessor.delete(
            id = id,
            request_operators = request_operators
        )

        return result

    def hydrate_pos_integration_calls(
        self,
        result_list: list[PosIntegrationCallModel],
        request_operators: RequestOperators | None = None
    ) -> None:
        
        # Hydrate retailer 
        self.hydrator.hydrate_target(
            "retailer", 
            result_list, 
            RetailerSearchModel(),
            self.search_retailers,
            request_operators.hydration if request_operators is not None else None
        )
        
        # hydrate retailer location
        self.hydrator.hydrate_target(
            "retailer_location", 
            result_list, 
            RetailerLocationSearchModel(),
            self.search_retailer_locations,
            request_operators.hydration if request_operators is not None else None
        )
        
        # hydrate pos integration
        self.hydrator.hydrate_target(
            "pos_integration", 
            result_list, 
            PosIntegrationSearchModel(),
            self.search_pos_integrations,
            request_operators.hydration if request_operators is not None else None
        )
    
    def create_pos_integration(
        self, 
        inbound_model: PosIntegrationCreateModel,
        request_operators: RequestOperators | None = None
    ) -> PosIntegrationModel | None:

        # Denormalize retailer_id
        
        referenced_retailer_location = self.get_retailer_location_by_id(inbound_model.retailer_location_id)
        
        inbound_model.retailer_id = referenced_retailer_location.retailer_id

        result = self.pos_integration_accessor.insert(
            model = inbound_model,
            request_operators = request_operators
        ) 
        
        self.hydrate_pos_integrations([result], request_operators)
        
        return result 
        
    def get_pos_integration_by_id(
        self, 
        id: UUID, 
        request_operators: RequestOperators | None = None
    ) -> PosIntegrationModel | None:

        result = self.pos_integration_accessor.select_by_id(
            id = id,
            request_operators = request_operators
        )
        
        self.hydrate_pos_integrations([result], request_operators)
   
        return result

    def search_pos_integrations(
        self,
        model: PosIntegrationSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None
    ) -> ItemList[PosIntegrationModel]:

        result = self.pos_integration_accessor.select(
            model = model,
            paging_model = paging_model,
            request_operators = request_operators
        ) 
        
        self.hydrate_pos_integrations(result.items, request_operators)
        
        return result

    def update_pos_integration(
        self,
        id: UUID,
        model: PosIntegrationUpdateModel, 
        request_operators: RequestOperators | None = None
    ): 
        result = self.pos_integration_accessor.update(
            id, 
            model,  
            request_operators = request_operators
        )
         
        self.hydrate_pos_integrations([result], request_operators)
        
        return result

    def delete_pos_integration(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> PosIntegrationModel | None:

        result: None | PosIntegrationModel = self.pos_integration_accessor.delete(
            id = id,
            request_operators = request_operators
        )

        return result

    def hydrate_pos_integrations(
        self,
        result_list: list[PosIntegrationModel],
        request_operators: RequestOperators | None = None
    ) -> None:
        
        # Hydrate retailer 
        self.hydrator.hydrate_target(
            "retailer", 
            result_list, 
            RetailerSearchModel(),
            self.search_retailers,
            request_operators.hydration if request_operators is not None else None
        )
        
        # hydrate retailer location
        self.hydrator.hydrate_target(
            "retailer_location", 
            result_list, 
            RetailerLocationSearchModel(),
            self.search_retailer_locations,
            request_operators.hydration if request_operators is not None else None
        )
     
    def create_pos_simulator_response(
        self, 
        inbound_model: PosSimulatorResponseCreateModel,
        request_operators: RequestOperators | None = None
    ) -> PosSimulatorResponseModel | None:
  
        result = self.pos_simulator_response_accessor.insert(
            model = inbound_model,
            request_operators = request_operators
        )
        
        self.hydrate_pos_simulator_responses([result], request_operators)

        return result

    def get_pos_simulator_response_by_id(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> PosSimulatorResponseModel | None:

        result = self.pos_simulator_response_accessor.select_by_id(
            id = id,
            request_operators = request_operators
        )

        self.hydrate_pos_simulator_responses([result], request_operators)
        
        return result
    
    def call_pos_simulator_response(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> dict[str, Any | None]:

        result = self.pos_simulator_response_accessor.select_by_id(
            id = id,
            request_operators = request_operators
        )
     
        return result.response_body
    
    def search_pos_simulator_responses(
        self,
        model: PosSimulatorResponseSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None
    ) -> ItemList[PosSimulatorResponseModel]:

        result = self.pos_simulator_response_accessor.select(
            model = model,
            paging_model = paging_model,
            request_operators = request_operators
        )
        
        self.hydrate_pos_simulator_responses(result.items, request_operators)
        
        return result

    def delete_pos_simulator_response(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> PosSimulatorResponseModel | None:

        result: None | PosSimulatorResponseModel = self.pos_simulator_response_accessor.delete(
            id = id,
            request_operators = request_operators
        )

        return result

    def hydrate_pos_simulator_responses(
        self,
        result_list: list[PosSimulatorResponseModel],
        request_operators: RequestOperators | None = None
    ) -> None:
        pass
    
    def create_product(
        self, 
        inbound_model: ProductCreateModel, 
        request_operators: RequestOperators | None = None
    ) -> ProductModel | None:
        
        # Denormalize retailer_id
        
        if(inbound_model.referring_retailer_location_id):
            referenced_retailer_location = self.get_retailer_location_by_id(inbound_model.referring_retailer_location_id)
            inbound_model.referring_retailer_id = referenced_retailer_location.retailer_id

        result = self.product_accessor.insert(
            model = inbound_model,
            request_operators = request_operators
        )

        self.hydrate_products([result], request_operators)
        
        return result

    def get_product_by_id(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ):

        result = self.product_accessor.select_by_id(
            id = id,
            request_operators = request_operators
        )

        self.hydrate_products([result], request_operators)
        
        return result

    def search_products(
        self,
        model: ProductSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None
    ) -> ItemList[ProductModel]:
    
        result = self.product_accessor.select(
            model = model,
            paging_model = paging_model,
            request_operators = request_operators
        )
        
        self.hydrate_products(result.items, request_operators)

        return result

    def update_product(
        self,
        id: UUID,
        model: ProductUpdateModel, 
        request_operators: RequestOperators | None = None
    ) -> ProductModel | None: 

        result = self.product_accessor.update(id, model, request_operators=request_operators)

        self.hydrate_products([result], request_operators)
        
        return result

    def delete_product(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> ProductModel | None:

        result: None | ProductModel = self.product_accessor.delete(
            id = id,
            request_operators = request_operators
        )

        return result

    def hydrate_products(
        self,
        result_list: list[ProductModel],
        request_operators: RequestOperators | None = None
    ):
        
        # Hydrate referring retailer 
        self.hydrator.hydrate_target(
            "referring_retailer", 
            result_list, 
            RetailerSearchModel(),
            self.search_retailers,
            request_operators.hydration if request_operators is not None else None
        )
        
        # hydrate referring retailer location
        self.hydrator.hydrate_target(
            "referring_retailer_location", 
            result_list, 
            RetailerLocationSearchModel(),
            self.search_retailer_locations,
            request_operators.hydration if request_operators is not None else None
        )
        
        # hydrate vendor
        self.hydrator.hydrate_target(
            "vendor", 
            result_list, 
            VendorSearchModel(),
            self.search_vendors,
            request_operators.hydration if request_operators is not None else None
        )
        
        # hydrate confirmed_core_product
        self.hydrator.hydrate_target(
            "confirmed_core_product", 
            result_list, 
            ProductSearchModel(),
            self.search_products,
            request_operators.hydration if request_operators is not None else None
        )
 
 
        
    def create_retailer_location(
        self, 
        inbound_model: RetailerLocationCreateModel, 
        request_operators: RequestOperators | None = None
    ) -> RetailerLocationModel | None:

        result =  self.retailer_location_accessor.insert(
            model = inbound_model,
            request_operators = request_operators
        )

        self.hydrate_retailer_locations([result], request_operators)

        return result

    def get_retailer_location_by_id(
        self, 
        id: UUID, 
        request_operators: RequestOperators | None = None
    ) -> RetailerLocationModel | None:

        result =  self.retailer_location_accessor.select_by_id(
            id = id,
            request_operators = request_operators
        )
        
        self.hydrate_retailer_locations([result], request_operators)
        
        return result

    def search_retailer_locations(
        self,
        model: RetailerLocationSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None
    ) -> ItemList[RetailerLocationModel]:

        result =  self.retailer_location_accessor.select(
            model = model,
            paging_model = paging_model,
            request_operators = request_operators
       )
        
        self.hydrate_retailer_locations(result.items, request_operators)
        
        return result

    def update_retailer_location(
        self,
        id: UUID,
        model: RetailerLocationUpdateModel, 
        request_operators: RequestOperators | None = None
    ) -> RetailerLocationModel | None:
  
        result = self.retailer_location_accessor.update(
            id, 
            model,  
            request_operators
        )
        
        self.hydrate_retailer_locations([result], request_operators)
        
        return result

    def delete_retailer_location(
        self,
        id: UUID,       
        request_operators: RequestOperators | None = None
    ) -> RetailerLocationModel | None:

        result: None | RetailerLocationModel =  self.retailer_location_accessor.delete(
            id = id,
            request_operators = request_operators
        )

        return result

    def hydrate_retailer_locations(
        self,
        result_list: list[RetailerLocationModel],
        request_operators: RequestOperators | None = None
    ):
        
        # Hydrate retailer 
        self.hydrator.hydrate_target(
            "retailer", 
            result_list, 
            RetailerSearchModel(),
            self.search_retailers,
            request_operators.hydration if request_operators is not None else None
        )
         
    def create_retailer(
        self,
        inbound_model: RetailerCreateModel,
        request_operators: RequestOperators | None = None
    ) -> RetailerModel | None:

        result = self.retailer_accessor.insert(
            model = inbound_model,
            request_operators = request_operators
        )

        self.hydrate_retailers([result], request_operators)
        
        return result

    def get_retailer_by_id(
        self, 
        id: UUID, 
        request_operators: RequestOperators | None = None
    ) -> RetailerModel | None:
 
        result = self.retailer_accessor.select_by_id(
            id = id,
            request_operators = request_operators
        )

        self.hydrate_retailers([result], request_operators)
        
        return result

    def search_retailers(
        self,
        model: RetailerSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None
    ) -> ItemList[RetailerModel]:

        result = self.retailer_accessor.select(
            model = model,
            paging_model = paging_model,
            request_operators = request_operators
       )

        self.hydrate_retailers(result.items, request_operators)
        
        return result

    def update_retailer(
        self,
        id: UUID,
        model: RetailerUpdateModel, 
        request_operators: RequestOperators | None = None
    ) -> RetailerModel | None: 

        result = self.retailer_accessor.update(
            id, 
            model, 
            request_operators = request_operators
        )
        
        self.hydrate_retailers([result], request_operators)

        return result

    def delete_retailer(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> RetailerModel | None:

        result: None | RetailerModel = self.retailer_accessor.delete(
            id = id,
            request_operators = request_operators
        )

        return result

    def hydrate_retailers(
        self,
        result_list: list[RetailerModel],
        request_operators: RequestOperators | None = None
    ):
        
        return
     
        
    def create_sales_intake_batch_job(
        self, 
        inbound_model: SalesIntakeBatchJobCreateModel,
        request_operators: RequestOperators | None = None
    ) -> SalesIntakeBatchJobModel | None:
 
        result = self.sales_intake_batch_job_accessor.insert(
            model = inbound_model,
            request_operators = request_operators
        )
        
        self.hydrate_sales_intake_batch_jobs(result_list = [result], request_operators = request_operators)

        return result

    def get_sales_intake_batch_job_by_id(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> SalesIntakeBatchJobModel | None:

        result = self.sales_intake_batch_job_accessor.select_by_id(
            id = id,
            request_operators = request_operators
        )
        
        self.hydrate_sales_intake_batch_jobs(result_list = [result], request_operators = request_operators)

        return result

    def search_sales_intake_batch_jobs(
        self,
        model: SalesIntakeBatchJobSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None
    ) -> ItemList[SalesIntakeBatchJobModel]:

        result = self.sales_intake_batch_job_accessor.select(
            model = model,
            paging_model = paging_model,
            request_operators = request_operators
        )

        self.hydrate_sales_intake_batch_jobs(result.items, request_operators)
 
        return result

    def update_sales_intake_batch_job(
        self,
        id: UUID,
        model: SalesIntakeBatchJobUpdateModel, 
        request_operators: RequestOperators | None = None
    ) -> SalesIntakeBatchJobModel | None: 
        
        result = self.sales_intake_batch_job_accessor.update(id, model,request_operators=request_operators)

        self.hydrate_sales_intake_batch_jobs([result], request_operators = request_operators)

        return result

    def delete_sales_intake_batch_job(
        self,
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> None:

        result: None | SalesIntakeBatchJobModel = self.sales_intake_batch_job_accessor.delete(
            id = id,
            request_operators = request_operators
        )

        return result
     
    def hydrate_sales_intake_batch_jobs(
        self,
        result_list: list[SalesIntakeBatchJobModel],
        request_operators: RequestOperators | None = None
    ) -> SalesIntakeBatchJobModel | None:
        
        return
 
    def create_sales_intake_job(
        self, 
        inbound_model: SalesIntakeJobCreateModel,
        request_operators: RequestOperators | None = None
    ) -> SalesIntakeJobModel | None:

        # Denormalize retailer_id
        
        referenced_retailer_location = self.get_retailer_location_by_id(inbound_model.retailer_location_id)
        
        inbound_model.retailer_id = referenced_retailer_location.retailer_id

        result = self.sales_intake_job_accessor.insert(
            model = inbound_model,
            request_operators = request_operators
        )
        
        self.hydrate_sales_intake_jobs([result], request_operators)
         
        return result

    def get_sales_intake_job_by_id(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> SalesIntakeJobModel | None:

        result = self.sales_intake_job_accessor.select_by_id(
            id = id,
            request_operators = request_operators
        )
        
        self.hydrate_sales_intake_jobs([result], request_operators)
        
        return result

    def search_sales_intake_jobs(
        self,
        model: SalesIntakeJobSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None
    ) -> ItemList[SalesIntakeJobModel]:

        result = self.sales_intake_job_accessor.select(
            model = model,
            paging_model = paging_model,
            request_operators = request_operators
        )

        self.hydrate_sales_intake_jobs(result.items, request_operators)
         
        return result

    def update_sales_intake_job(
        self,
        id: UUID,
        model: SalesIntakeJobUpdateModel, 
        request_operators: RequestOperators | None = None
    ) -> SalesIntakeJobModel | None:
 
        result = self.sales_intake_job_accessor.update(id, model, request_operators=request_operators)

        self.hydrate_sales_intake_jobs([result], request_operators)
         
        return result

    def delete_sales_intake_job(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> SalesIntakeJobModel | None:

        result: None | SalesIntakeJobModel = self.sales_intake_job_accessor.delete(
            id = id,
            request_operators = request_operators
        )

        return result
     

    def hydrate_sales_intake_jobs(
        self,
        result_list: list[SalesIntakeJobModel],
        request_operators: RequestOperators | None = None
    ):
        
        # Hydrate retailer 
        self.hydrator.hydrate_target(
            "retailer", 
            result_list, 
            RetailerSearchModel(),
            self.search_retailers,
            request_operators.hydration if request_operators is not None else None
        )
        
        # hydrate retailer location
        self.hydrator.hydrate_target(
            "retailer_location", 
            result_list, 
            RetailerLocationSearchModel(),
            self.search_retailer_locations,
            request_operators.hydration if request_operators is not None else None
        )
 
        # hydrate parent batch job
        self.hydrator.hydrate_target(
            "parent_batch_job",
            result_list, 
            SalesIntakeBatchJobSearchModel(),
            self.search_sales_intake_batch_jobs,
            request_operators.hydration if request_operators is not None else None
        ) 
        
    def create_user(
        self, 
        inbound_model: UserCreateModel,
        request_operators: RequestOperators | None = None
    ) -> UserModel | None:

        # Denormalize retailer_id
        if(inbound_model.retailer_location_id): 
            referenced_retailer_location = self.get_retailer_location_by_id(inbound_model.retailer_location_id) 
            inbound_model.retailer_id = referenced_retailer_location.retailer_id
        
        result = self.user_accessor.insert(
            model = inbound_model,
            request_operators = request_operators
        )

        self.hydrate_users([result], request_operators)
        
        return result

    def get_user_by_id(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> UserModel | None:

        result = self.user_accessor.select_by_id(
            id = id,
            request_operators = request_operators
        )
        
        self.hydrate_users([result], request_operators)

        return result

    def search_users(
        self,
        model: UserSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None
    ) -> ItemList[UserModel]:

        result = self.user_accessor.select(
            model = model,
            paging_model = paging_model,
            request_operators = request_operators
        )
        
        self.hydrate_users(result.items, request_operators)

        return result

    def update_user(
        self,
        id: UUID,
        model: UserUpdateModel, 
        request_operators: RequestOperators | None = None
    ) -> UserModel | None: 
        
        result = self.user_accessor.update(id, model, request_operators=request_operators)
        
        self.hydrate_users([result], request_operators)

        return result

    def delete_user(
        self, 
        id: UUID, 
        request_operators: RequestOperators | None = None
    ) -> UserModel | None:

        result: None | UserModel = self.user_accessor.delete(
            id = id,
            request_operators = request_operators
        )

        return result

    def hydrate_users(
        self,
        result_list: list[UserModel],
        request_operators: RequestOperators | None = None
    ):
        
        # Hydrate retailer 
        self.hydrator.hydrate_target(
            "retailer", 
            result_list, 
            RetailerSearchModel(),
            self.search_retailers,
            request_operators.hydration if request_operators is not None else None
        )
        
        # hydrate retailer location
        self.hydrator.hydrate_target(
            "retailer_location", 
            result_list, 
            RetailerLocationSearchModel(),
            self.search_retailer_locations,
            request_operators.hydration if request_operators is not None else None
        )
 
        # hydrate vendor
        self.hydrator.hydrate_target(
            "vendor",
            result_list, 
            VendorSearchModel(),
            self.search_vendors,
            request_operators.hydration if request_operators is not None else None
        )
        
  
        
    def create_vendor(
        self, 
        inbound_model: VendorCreateModel,
        request_operators: RequestOperators | None = None
    ) -> VendorModel | None:

        result = self.vendor_accessor.insert(
            model = inbound_model,
            request_operators = request_operators
        )

        self.hydrate_vendors([result], request_operators)
        
        return result

    def get_vendor_by_id(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> VendorModel | None:

        result = self.vendor_accessor.select_by_id(
            id = id,
            request_operators = request_operators
        )

        self.hydrate_vendors([result], request_operators)
        
        return result

    def search_vendors(
        self,
        model: VendorSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None
    ) -> ItemList[VendorModel]:

        result = self.vendor_accessor.select(
            model = model,
            paging_model = paging_model,
            request_operators = request_operators
       )

        self.hydrate_vendors(result.items, request_operators)
        
        return result

    def update_vendor(
        self,
        id: UUID,
        model: VendorUpdateModel, 
        request_operators: RequestOperators | None = None
    ) -> VendorModel | None: 

        result = self.vendor_accessor.update(id, model, request_operators=request_operators)

        self.hydrate_vendors([result], request_operators)
        
        return result

    def delete_vendor(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> VendorModel | None:

        result: None | VendorModel = self.vendor_accessor.delete(
            id = id,
            request_operators = request_operators
        )

        return result

    def hydrate_vendors(
        self,
        result_list: list[VendorModel],
        request_operators: RequestOperators | None = None
    ): 
        return
