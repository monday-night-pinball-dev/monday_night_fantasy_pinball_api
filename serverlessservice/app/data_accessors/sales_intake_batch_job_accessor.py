from typing import Any
from uuid import UUID
from adapters.sales_intake_batch_job_adapters import SalesIntakeBatchJobDataAdapter
from models.sales_intake_batch_job_model import (
    SalesIntakeBatchJobCreateModel,
    SalesIntakeBatchJobDatabaseModel,
    SalesIntakeBatchJobModel,
    SalesIntakeBatchJobSearchModel,
    SalesIntakeBatchJobUpdateModel,
)
from models.common_model import ItemList
from util.common import RequestOperators
from util.configuration import get_global_configuration
from util.database import PagingModel, SearchTerm
from util.db_connection import SelectQueryResults
 
class SalesIntakeBatchJobDataAccessor:
    adapter: SalesIntakeBatchJobDataAdapter = SalesIntakeBatchJobDataAdapter()

    def insert(
        self,
        model: SalesIntakeBatchJobCreateModel,
        request_operators: RequestOperators | None = None
    ) -> SalesIntakeBatchJobModel:
        
        connection = get_global_configuration().pg_connection

        db_model: dict[str, Any] = self.adapter.convert_from_create_model_to_database_model(model)

        db_result: dict[str, Any] = connection.insert(
            'sales_intake_batch_jobs',
            db_model,
            request_operators
        )

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def select_by_id(
        self, 
        id: UUID, 
        request_operators: RequestOperators | None = None 
    ) -> SalesIntakeBatchJobModel:

        connection = get_global_configuration().pg_connection

        db_result = connection.select_by_id(
            'sales_intake_batch_jobs',
            id,
            request_operators
        )

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def select(
        self,
        model: SalesIntakeBatchJobSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None
    ) -> ItemList[SalesIntakeBatchJobModel]:

        connection = get_global_configuration().pg_connection

        search_terms: list[SearchTerm] = self.adapter.convert_from_search_model_to_search_terms(
                model
        )
        
        db_result: SelectQueryResults = connection.select('sales_intake_batch_jobs', 
            search_terms, 
            paging_model,
            request_operators
        )

        results: ItemList[SalesIntakeBatchJobModel] = ItemList[SalesIntakeBatchJobModel](db_result.paging)

        if db_result is None:
            return results

        for item in db_result.items:
            result_model = self.adapter.convert_from_database_model_to_model(item)
            results.items.append(result_model)

        return results

    def update(
        self,
        id: UUID,
        model: SalesIntakeBatchJobUpdateModel, 
        request_operators: RequestOperators | None = None
    ) -> SalesIntakeBatchJobModel:
        
        connection = get_global_configuration().pg_connection

        db_model: dict[str, Any] = self.adapter.convert_from_update_model_to_database_model(
                model)

        db_result = connection.update(
            'sales_intake_batch_jobs',
            id,
            db_model,
            request_operators
        )

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def delete(
        self,
        id: UUID,
        request_operators: RequestOperators | None = None
    ) -> SalesIntakeBatchJobModel:

        connection = get_global_configuration().pg_connection

        db_result = connection.delete(
            'sales_intake_batch_jobs',
            id,
            request_operators
        )

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(
            db_result
        )

        return result_model
