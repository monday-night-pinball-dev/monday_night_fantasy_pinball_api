from typing import Any
from uuid import UUID
from adapters.retailer_location_adapters import RetailerLocationDataAdapter
from models.retailer_location_model import (
    RetailerLocationCreateModel,
    RetailerLocationModel,
    RetailerLocationSearchModel,
    RetailerLocationUpdateModel,
)
from models.common_model import ItemList
from util.common import RequestOperators
from util.configuration import get_global_configuration
from util.database import PagingModel, SearchTerm
from util.db_connection import SelectQueryResults
 
class RetailerLocationDataAccessor:
    adapter: RetailerLocationDataAdapter = RetailerLocationDataAdapter()

    def insert(
        self,
        model: RetailerLocationCreateModel,
        request_operators: RequestOperators | None = None
    ) -> RetailerLocationModel:
        
        connection = get_global_configuration().pg_connection

        db_model: dict[str, Any] = self.adapter.convert_from_create_model_to_database_model(model)

        db_result: dict[str, Any] = connection.insert(
            'retailer_locations',
            db_model,
            request_operators
        )

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def select_by_id(
        self, 
        id: UUID, 
        request_operators: RequestOperators | None = None 
    ) -> RetailerLocationModel:

        connection = get_global_configuration().pg_connection

        db_result = connection.select_by_id(
            'retailer_locations',
            id,
            request_operators
        )

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def select(
        self,
        model: RetailerLocationSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None
    ) -> ItemList[RetailerLocationModel]:

        connection = get_global_configuration().pg_connection

        search_terms: list[SearchTerm] = self.adapter.convert_from_search_model_to_search_terms(model)

        db_result: SelectQueryResults = connection.select(
            'retailer_locations',
            search_terms,
            paging_model,
            request_operators
        )

        results: ItemList[RetailerLocationModel] = ItemList[
            RetailerLocationModel](db_result.paging)

        if db_result is None:
            return results

        for item in db_result.items:
            result_model = self.adapter.convert_from_database_model_to_model(item)
            results.items.append(result_model)

        return results

    def update(
        self,
        id: UUID,
        model: RetailerLocationUpdateModel, 
        request_operators: RequestOperators | None = None
    ) -> RetailerLocationModel:


        connection = get_global_configuration().pg_connection

        db_model: dict[str, Any] = self.adapter.convert_from_update_model_to_database_model(
                model)

        db_result = connection.update(
            'retailer_locations',
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
    ) -> RetailerLocationModel:

        connection = get_global_configuration().pg_connection

        db_result = connection.delete(
            'retailer_locations',
            id,
            request_operators
        )

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model
