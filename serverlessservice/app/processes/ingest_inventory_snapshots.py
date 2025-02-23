    
from uuid import UUID
from integrations.posabit_integration import PosabitIntegration
from integrations.types import GenericInventoryObject
from models.historical_sale_model import HistoricalSaleModel, HistoricalSaleSearchModel
from models.inventory_intake_job_model import InventoryIntakeJobModel, InventoryIntakeJobStatuses, InventoryIntakeJobUpdateModel
from models.inventory_product_snapshot_model import InventoryProductSnapshotModel, InventoryProductSnapshotSearchModel, InventoryProductSnapshotCreateModel
from models.pos_integration_model import PosIntegrationModel, PosIntegrationSearchModel, PosPlatforms
from models.product_model import ProductCreateModel, ProductVendorConfirmationStatuses, ProductModel
from processes.common import CommonProcessUtilities, ProcessException
from util.common import RequestOperators
from util.database import PagingModel 
import managers.managers as managers 


class IngestInventorySnapshotsProcess:
    
    def __init__(
        self, 
        posabit_integration: PosabitIntegration = PosabitIntegration(),
        manager: managers.Manager = managers.Manager(),
        common_process_utilities: CommonProcessUtilities = CommonProcessUtilities(),
    ) -> None:  
        self.posabit_integration = posabit_integration
        self.manager = manager 
    
        self.common_process_utilities = common_process_utilities
        self.process_name = "Ingest Inventory Snapshots"
        self.product_inactivity_threshold_in_days = 180
    
    def run_process(
        self,
        job_id: UUID,
        process_trace_id: str
    ) -> None: 
        
        try:
                
            integration: PosIntegrationModel | None = None
            inventory_snapshot_items: list[GenericInventoryObject] | None = None
            inventory_product_snapshots_to_insert: list[InventoryProductSnapshotCreateModel] = []
            job: InventoryIntakeJobModel | None = None
            
            # Step: UpdateJobStatusToProcessing 
            try:
                job = self.manager.update_inventory_intake_job(
                    job_id, 
                    InventoryIntakeJobUpdateModel(
                        status=InventoryIntakeJobStatuses.Processing
                    )
                )
                    
                if(job is None):
                    raise Exception(f"Inventory Intake Job with id {job_id} not found.")
                        
                print(f"Found inventory intake job {job.id} for retailer location {job.retailer_location_id} and snapshot_hour {job.snapshot_hour}")
                    
            except Exception as e:
                if(isinstance(e, ProcessException)):
                    raise e
                else:
                    raise ProcessException(self.process_name, process_trace_id, "Arrange", f"Unhandled Exception occured: {e}")
            
            # Step: Arrange 
            try: 
                        
                integration = self.get_pos_integration_and_retailer_info(job.retailer_location_id)
                
                if(integration is None):
                    raise Exception(f"No POS Integration found for Retailer Location ID: {job.retailer_location_id}")
                
                print(f"Found {integration.pos_platform} POS Integration {integration.id} for Retailer Location ID: {job.retailer_location_id}")
                
            except Exception as e:
                if(isinstance(e, ProcessException)):
                    raise e
                else:
                    raise ProcessException(self.process_name, process_trace_id, "Arrange", f"Unhandled Exception occured: {e}")

            # Step: RetrieveInventorySnapshots   
            
            try:
                inventory_snapshot_items = self.retrieve_inventory_snapshots(
                    job=job,
                    integration=integration
                )

            except Exception as e: 
                if(isinstance(e, ProcessException)):
                    raise e
                else:
                    raise ProcessException(self.process_name, process_trace_id, "RetrieveInventorySnapshots", f"Unhandled Exception occured: {e}")
                
            # Step: ProcessInventorySnapshots
            
            try:
                for inventory_snapshot_item in inventory_snapshot_items:
                    
                    try:
                        
                        existing_snapshot = self.common_process_utilities.retrieve_existing_snapshot_or_sale(integration.retailer_location_id, inventory_snapshot_item.sku)

                        product: ProductModel | None = None
                         
                        if(existing_snapshot is None):
                            
                            # Create Candidate Product
                            
                            new_product_to_create = ProductCreateModel(
                                vendor_id = None,
                                vendor_confirmation_status = ProductVendorConfirmationStatuses.Candidate, 
                                referring_retailer_location_id = job.retailer_location_id,
                                confirmed_core_product_id = None,
                                name = inventory_snapshot_item.product_name,
                            )
                            
                            product = self.manager.create_product(
                                new_product_to_create
                            )
                            
                            print(f"Created new candidate product {product.id}")
                        
                        else:
                            product = self.manager.get_product_by_id(existing_snapshot.product_id)
                            
                            print(f"Found existing product {product.id}")
                            
                        new_snapshot_to_create = InventoryProductSnapshotCreateModel(
                            product_id = product.id,
                            inventory_intake_job_id = job.id,
                            retailer_location_id = integration.retailer_location_id,
                            snapshot_hour = job.snapshot_hour,
                            sku = inventory_snapshot_item.sku,
                            stock_on_hand = inventory_snapshot_item.stock_on_hand,
                            price = inventory_snapshot_item.price,
                        )
                            
                        inventory_product_snapshots_to_insert.append(new_snapshot_to_create)
                        
                        print(f"Resolved inventory snapshot for retailer location {new_snapshot_to_create.retailer_location_id} and product {new_snapshot_to_create.product_id} and sku {new_snapshot_to_create.sku}")
                        
                    except Exception as e:
                        print(f"Failed to resolve inventory snapshot for sku {inventory_snapshot_item.sku} at retailer_location {integration.retailer_location_id} - {e}")
                        
            except Exception as e: 
                if(isinstance(e, ProcessException)):
                    raise e
                else:
                    raise ProcessException(self.process_name, self.process_trace_id, "ProcessInventorySnapshots", f"Unhandled Exception occured: {e}")

            # Step: InsertInventoryProductSnapshots
            
            try:
                for inventory_product_snapshot_to_insert in inventory_product_snapshots_to_insert:
                    try:
                        
                        inserted_snapshot = self.manager.create_inventory_product_snapshot(inventory_product_snapshot_to_insert)
                        
                        print(f"Created new inventory snapshot {inserted_snapshot.id} for retailer location {inserted_snapshot.retailer_location_id} and product {inserted_snapshot.product_id} and sku {inserted_snapshot.sku}")
                    
                    except Exception as e:
                        print(f"Failed to insert inventory snapshot for sku {inventory_product_snapshot_to_insert.sku} at retailer_location {inventory_product_snapshot_to_insert.retailer_location_id} - {e}")
            
            except Exception as e: 
                if(isinstance(e, ProcessException)):
                    raise e
                else:
                    raise ProcessException(self.process_name, process_trace_id, "InsertInventoryProductSnapshots", f"Unhandled Exception occured: {e}")

            # Step: UpdateJobStatusToComplete
            
            try:
                job = self.manager.update_inventory_intake_job(
                    job_id, 
                    InventoryIntakeJobUpdateModel(
                        status=InventoryIntakeJobStatuses.Complete
                    )
                )
                
                print(f"Updated inventory intake job {job.id} to status {job.status}")
                
                return job 
                
            except Exception as e:
                if(isinstance(e, ProcessException)):
                    raise e
                else:
                    raise ProcessException(self.process_name, process_trace_id, "UpdateJobStatusToComplete", f"Unhandled Exception occured: {e}")
                
        except Exception as e:
            if(isinstance(e, ProcessException)):
                self.manager.update_inventory_intake_job(
                    job_id, 
                    InventoryIntakeJobUpdateModel(
                        status=InventoryIntakeJobStatuses.Failed,
                        status_details=f"Step: {e.step} - Exception occured: {e}"
                    )
                )
            else:
                self.manager.update_inventory_intake_job(
                    job_id, 
                    InventoryIntakeJobUpdateModel(
                        status=InventoryIntakeJobStatuses.Failed,
                        status_details=f"Unhandled Exception occured: {e}"
                    )
                )
            raise e
            
    def get_pos_integration_and_retailer_info(
        self,
        retailer_location_id: UUID
    )   -> PosIntegrationModel:
        PosInterationSearchModel = PosIntegrationSearchModel(
            retailer_location_ids=[retailer_location_id]
        )
        operators = RequestOperators(
            hydration=["retailer", "retailer_location"],
            skip_paging=True
        )
        
        pos_integrations = self.manager.search_pos_integrations(PosInterationSearchModel, None, operators)
        
        return pos_integrations.items[0] if pos_integrations is not None and len(pos_integrations.items) > 0 else None
    
    def retrieve_inventory_snapshots(
        self,
        job: InventoryIntakeJobModel,
        integration: PosIntegrationModel,
    )   -> list[GenericInventoryObject]: 
        
        
        match(integration.pos_platform):
            case PosPlatforms.Posabit:
                return self.posabit_integration.get_inventory_snapshots ( 
                    integration_key = integration.key,
                    simulator_response_id = job.simulator_response_id
                )
            case _:
                raise Exception(f"Pos Integration Platform {integration.pos_platform} not supported for action retrieve_inventory_snapshots")