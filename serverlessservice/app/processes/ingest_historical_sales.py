    
from uuid import UUID
from integrations.posabit_integration import PosabitIntegration
from integrations.types import GenericHistoricalSaleItemObject, GenericHistoricalSaleObject, GenericInventoryObject
from models.historical_sale_item_model import HistoricalSaleItemCreateModel
from models.historical_sale_model import HistoricalSaleCreateModel, HistoricalSaleModel, HistoricalSaleSearchModel
from models.inventory_intake_job_model import InventoryIntakeJobModel, InventoryIntakeJobStatuses, InventoryIntakeJobUpdateModel
from models.inventory_product_snapshot_model import InventoryProductSnapshotModel, InventoryProductSnapshotSearchModel, InventoryProductSnapshotCreateModel
from models.pos_integration_model import PosIntegrationModel, PosIntegrationSearchModel, PosPlatforms
from models.product_model import ProductCreateModel, ProductVendorConfirmationStatuses, ProductModel
from models.sales_intake_job_model import SalesIntakeJobModel, SalesIntakeJobStatuses, SalesIntakeJobUpdateModel
from processes.common import CommonProcessUtilities, ProcessException
from util.common import RequestOperators
from util.database import PagingModel 
import managers.managers as managers 

class HistoricSaleCreateModelWithItems(HistoricalSaleCreateModel):
    items: list[HistoricalSaleItemCreateModel]  
    
    def __init__(
        self, 
        items: list[HistoricalSaleItemCreateModel] | None = None,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.items = items
  
class IngestHistoricalSalesProcess:
    
    def __init__(
        self, 
        posabit_integration: PosabitIntegration = PosabitIntegration(),
        manager: managers.Manager = managers.Manager(),
        common_process_utilities: CommonProcessUtilities = CommonProcessUtilities(),
    ) -> None:  
        self.posabit_integration = posabit_integration
        self.manager = manager 
        
        self.common_process_utilities = common_process_utilities
             
        self.process_name = "Ingest Historical Sales"
    
    def run_process(
        self,
        job_id: UUID,
        process_trace_id: str
    ) -> None: 
        
        try:
                
            integration: PosIntegrationModel | None = None
            sales_objects: list[GenericHistoricalSaleObject] | None = None 
            
            job: SalesIntakeJobModel | None = None
            
            # Step: UpdateJobStatusToProcessing 
            
            try:
                job = self.manager.update_sales_intake_job(
                    job_id, 
                    SalesIntakeJobUpdateModel(
                        status=SalesIntakeJobStatuses.Processing
                    )
                )
                    
                if(job is None):
                    raise Exception(f"Sales Intake Job with id {job_id} not found.")
                        
                print(f"Found sales intake job {job.id} for retailer location {job.retailer_location_id}, start_time {job.start_time}, and end_time {job.end_time}")
                    
            except Exception as e:
                if(isinstance(e, ProcessException)):
                    raise e
                else:
                    raise ProcessException(self.process_name, process_trace_id, "Arrange - UpdateJobStatusToProcessing", f"Unhandled Exception occured: {e}")
            
            # Step: Arrange - Get POS Integration and Retailer Info
            
            try: 
                        
                integration = self.get_pos_integration_and_retailer_info(job.retailer_location_id)
                
                if(integration is None):
                    raise Exception(f"No POS Integration found for Retailer Location ID: {job.retailer_location_id}")
                
                print(f"Found {integration.pos_platform} POS Integration {integration.id} for Retailer Location ID: {job.retailer_location_id}")
                
            except Exception as e:
                if(isinstance(e, ProcessException)):
                    raise e
                else:
                    raise ProcessException(self.process_name, process_trace_id, "Arrange - GetIntegrationAndRetailerInfo", f"Unhandled Exception occured: {e}")

            # Step: Arrange - RetrieveSalesFromPOS
            
            try:
                sales_objects = self.retrieve_sales(
                    job=job,
                    integration=integration
                )

            except Exception as e: 
                if(isinstance(e, ProcessException)):
                    raise e
                else:
                    raise ProcessException(self.process_name, process_trace_id, "Arrange - RetrieveInventorySnapshots", f"Unhandled Exception occured: {e}")
                
            # Step: Act - ProcessInventorySnapshots
            
            try:
                for sales_object in sales_objects:
                    
                    # check for existing pos sale
                    existing_sale_search_model = HistoricalSaleSearchModel(
                        retailer_location_ids = [integration.retailer_location_id],
                        pos_sale_ids = [sales_object.pos_sale_id]
                    )
                    
                    existing_sale = self.manager.search_historical_sales(existing_sale_search_model)
                    
                    if(existing_sale is not None and len(existing_sale.items) > 0):
                        print(f"Found existing historical sale {existing_sale.items[0].id} for pos sale id {sales_object.pos_sale_id}")
                        continue
                    
                    else:
                        print(f"No existing historical sale found for pos sale id {sales_object.pos_sale_id}, ingesting...")
                    
                        for sales_item in sales_object.sale_items:
                            try:  
                                
                                existing_product_reference = self.common_process_utilities.retrieve_existing_snapshot_or_sale(integration.retailer_location_id, sales_item.sku)

                                product: ProductModel | None = None
                                
                                if(existing_product_reference is None):
                                    
                                    # Create Candidate Product
                                    
                                    new_product_to_create = ProductCreateModel(
                                        vendor_id = None,
                                        vendor_confirmation_status = ProductVendorConfirmationStatuses.Candidate, 
                                        referring_retailer_location_id = job.retailer_location_id,
                                        confirmed_core_product_id = None,
                                        name = sales_item.product_name,
                                    )
                                    
                                    product = self.manager.create_product(
                                        new_product_to_create
                                    )
                                    
                                    print(f"Created new candidate product {product.id}")
                                
                                else:
                                    product = self.manager.get_product_by_id(existing_product_reference.product_id)
                                    
                                    print(f"Found existing product {product.id}")
                            
                                new_sale_to_create = HistoricalSaleCreateModel(
                                    retailer_location_id = integration.retailer_location_id,
                                    sale_timestamp=sales_object.sale_timestamp,
                                    pos_sale_id=sales_object.pos_sale_id,
                                    total=sales_object.total,
                                    sub_total=sales_object.sub_total,
                                    discount=sales_object.discount,
                                    tax=sales_object.tax,
                                    cost=sales_object.cost,
                                    sales_intake_job_id=job.id,
                                )
                                
                                new_sale = self.manager.create_historical_sale(new_sale_to_create)
                                
                                print(f"Created new historical sale {new_sale.id} for retailer location {integration.retailer_location_id}")
                                
                                new_sale_item_to_create = HistoricalSaleItemCreateModel(
                                    product_id = product.id,
                                    historical_sale_id = new_sale.id,
                                    sku = sales_item.sku,
                                    sale_count = sales_item.sale_count,
                                    sale_timestamp = sales_object.sale_timestamp,
                                    total = sales_item.total,    
                                    sale_product_name = sales_item.product_name,
                                    lot_identifier = sales_item.lot_identifier,
                                    pos_sale_id = sales_item.pos_sale_id,
                                    pos_product_id = sales_item.pos_product_id,
                                    unit_of_weight = sales_item.unit_of_weight,
                                    weight_in_units = sales_item.weight_in_units,
                                    sub_total = sales_item.sub_total,
                                    discount = sales_item.discount,
                                    tax = sales_item.tax,
                                    cost = sales_item.cost,
                                ) 
                                
                                new_sale_item = self.manager.create_historical_sale_item(new_sale_item_to_create)
                                
                                print(f"Created new historical sale item {new_sale_item.id} for historical sale {new_sale.id} and product {new_sale_item.product_id} and sku {new_sale_item.sku}")
                                
                            except Exception as e:
                                print(f"Failed to resolve sales item for sale id {sales_object.id}, item sku {sales_item.sku} at retailer_location {integration.retailer_location_id} - {e}")
                            
            except Exception as e: 
                if(isinstance(e, ProcessException)):
                    raise e
                else:
                    raise ProcessException(self.process_name, process_trace_id, "ProcessInventorySnapshots", f"Unhandled Exception occured: {e}")
  
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
    
    def retrieve_sales(
        self,
        job: SalesIntakeJobModel,
        integration: PosIntegrationModel,
    )   -> list[GenericHistoricalSaleObject]: 
        
        
        match(integration.pos_platform):
            case PosPlatforms.Posabit:
                return self.posabit_integration.get_historical_sales ( 
                    integration_key = integration.key,
                    start_time=job.start_time,
                    simulator_response_id = job.simulator_response_id
                )
            case _:
                raise Exception(f"Pos Integration Platform {integration.pos_platform} not supported for action retrieve_inventory_snapshots")
  
 