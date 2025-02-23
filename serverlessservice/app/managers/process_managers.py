import processes.ingest_inventory_snapshots as ingest_inventory_snapshots
import processes.ingest_historical_sales as ingest_historical_sales

from uuid import UUID 

from data_accessors.inventory_intake_batch_job_accessor import InventoryIntakeBatchJobDataAccessor
from data_accessors.inventory_intake_job_accessor import InventoryIntakeJobDataAccessor
from data_accessors.sales_intake_batch_job_accessor import SalesIntakeBatchJobDataAccessor
from data_accessors.sales_intake_job_accessor import SalesIntakeJobDataAccessor   

from models.inventory_intake_batch_job_model import (   
    InventoryIntakeBatchJobModel
)
from models.inventory_intake_job_model import (   
    InventoryIntakeJobModel
)
from models.sales_intake_batch_job_model import (   
    SalesIntakeBatchJobModel
)
from models.sales_intake_job_model import (   
    SalesIntakeJobModel
)
from models.sales_intake_batch_job_model import (   
    SalesIntakeBatchJobModel
)
from models.sales_intake_job_model import (   
    SalesIntakeJobModel
)

from util.common import CommonUtilities, RequestOperators
from util.hydration import Hydrator 
  
class ProcessManager:

    def __init__(
        self,  
        hydrator: Hydrator = Hydrator(), 
        inventory_intake_batch_job_accessor: InventoryIntakeBatchJobDataAccessor = InventoryIntakeBatchJobDataAccessor(),
        inventory_intake_job_accessor: InventoryIntakeJobDataAccessor = InventoryIntakeJobDataAccessor(),
        sales_intake_job_accessor: SalesIntakeJobDataAccessor = SalesIntakeJobDataAccessor(),
        sales_intake_batch_job_accessor: SalesIntakeBatchJobDataAccessor = SalesIntakeBatchJobDataAccessor(),
        ingest_inventory_snapshots_process: ingest_inventory_snapshots.IngestInventorySnapshotsProcess = ingest_inventory_snapshots.IngestInventorySnapshotsProcess(),
        ingest_historical_sales_process: ingest_historical_sales.IngestHistoricalSalesProcess = ingest_historical_sales.IngestHistoricalSalesProcess(),
        common_utilities: CommonUtilities = CommonUtilities()
        
    ) -> None: 
        
        self.hydrator = hydrator 
        self.ingest_inventory_snapshots_process = ingest_inventory_snapshots_process
        self.inventory_intake_batch_job_accessor = inventory_intake_batch_job_accessor
        self.inventory_intake_job_accessor = inventory_intake_job_accessor
        self.sales_intake_job_accessor = sales_intake_job_accessor
        self.sales_intake_batch_job_accessor = sales_intake_batch_job_accessor
        self.common_utilities = common_utilities
        self.ingest_historical_sales_process = ingest_historical_sales_process
   
    def run_inventory_intake_batch_job(
        self, 
        id: UUID, 
        request_operators: RequestOperators | None = None
    ) -> InventoryIntakeBatchJobModel | None:
        job_to_run: InventoryIntakeBatchJobModel = self.inventory_intake_batch_job_accessor.select_by_id(
            id = id
        )
        
        if(job_to_run == None):
            return None
       
        return None
             
    def run_inventory_intake_job(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> InventoryIntakeJobModel | None:
        job_to_run: InventoryIntakeJobModel = self.inventory_intake_job_accessor.select_by_id(
            id = id,
            request_operators = request_operators
        )
        
        if(job_to_run == None):
            return None
        
        
        result = self.ingest_inventory_snapshots_process.run_process(
            job_to_run.id, 
            self.common_utilities.generate_random_string(
                len = 20,
                charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
            )
        )

        return result
    
    def run_sales_intake_batch_job(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> SalesIntakeBatchJobModel | None:
        job_to_run: SalesIntakeBatchJobModel = self.sales_intake_batch_job_accessor.select_by_id(
            id = id,
            request_operators = request_operators
        )
        
        if(job_to_run == None):
            return None
        
        return None
    
    def run_sales_intake_job(
        self, 
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> SalesIntakeJobModel | None:
        
        job_to_run: SalesIntakeJobModel = self.sales_intake_job_accessor.select_by_id(
            id = id,
            request_operators = request_operators
        )
        
        if(job_to_run == None):
            return None
        
        
        result = self.ingest_historical_sales_process.run_process(
            job_to_run.id, 
            self.common_utilities.generate_random_string(
                len = 20,
                charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
            )
        )

        return result
    
        