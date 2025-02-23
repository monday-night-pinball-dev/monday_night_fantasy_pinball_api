from typing import Any
from uuid import UUID
from adapters.pos_integration_adapters import PosIntegrationDataAdapter
from models.pos_integration_model import (
    PosIntegrationCreateModel,
    PosIntegrationDatabaseModel,
    PosIntegrationModel,
    PosIntegrationSearchModel,
    PosIntegrationUpdateModel,
)
from models.common_model import ItemList
from util.common import RequestOperators
from util.configuration import get_global_configuration
from util.database import PagingModel, SearchTerm
from util.db_connection import SelectQueryResults
 
class PosIntegrationDataAccessor:
    adapter: PosIntegrationDataAdapter = PosIntegrationDataAdapter()

    def insert(
        self, 
        model: PosIntegrationCreateModel,
        request_operators: RequestOperators | None = None
    ) -> PosIntegrationModel:
        
        connection = get_global_configuration().pg_connection

        db_model: dict[str, Any] = self.adapter.convert_from_create_model_to_database_model(model)

        db_result: dict[str, Any] = connection.insert(
            'pos_integrations',
            db_model,
            request_operators
        )

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def select_by_id(
        self, 
        id: UUID, 
        request_operators: RequestOperators | None = None 
    ) -> PosIntegrationModel:

        connection = get_global_configuration().pg_connection

        db_result = connection.select_by_id(
            'pos_integrations',
            id,
            request_operators
        )

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def select(
        self,
        model: PosIntegrationSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None
    ) -> ItemList[PosIntegrationModel]:

        connection = get_global_configuration().pg_connection

        search_terms: list[SearchTerm] = self.adapter.convert_from_search_model_to_search_terms(model)

        db_result: SelectQueryResults = connection.select(
            'pos_integrations',
            search_terms,
            paging_model,
            request_operators
        )

        results: ItemList[PosIntegrationModel] = ItemList[PosIntegrationModel](db_result.paging)

        if db_result is None:
            return results

        for item in db_result.items:
            result_model = self.adapter.convert_from_database_model_to_model(item)
            results.items.append(result_model)

        return results

    def update(
        self,
        id: UUID,
        model: PosIntegrationUpdateModel, 
        request_operators: RequestOperators | None = None
    ) -> PosIntegrationModel:
 
        connection = get_global_configuration().pg_connection

        db_model: dict[str, Any] = self.adapter.convert_from_update_model_to_database_model(
                model)

        db_result = connection.update(
            'pos_integrations',
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
    ) -> PosIntegrationModel:

        connection = get_global_configuration().pg_connection

        db_result = connection.delete(
            'pos_integrations',
            id,
            request_operators
        )

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model
