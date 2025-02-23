from typing import Any
from uuid import UUID
from adapters.pos_simulator_response_adapters import PosSimulatorResponseDataAdapter
from models.pos_simulator_response_model import (
    PosSimulatorResponseCreateModel,
    PosSimulatorResponseDatabaseModel,
    PosSimulatorResponseModel,
    PosSimulatorResponseSearchModel, 
)
from models.common_model import ItemList
from util.common import RequestOperators
from util.configuration import get_global_configuration
from util.database import PagingModel, SearchTerm
from util.db_connection import SelectQueryResults
 
class PosSimulatorResponseDataAccessor:
    adapter: PosSimulatorResponseDataAdapter = PosSimulatorResponseDataAdapter()

    def insert(
        self,
        model: PosSimulatorResponseCreateModel,
        request_operators: RequestOperators | None = None
    ) -> PosSimulatorResponseModel:
        
        connection = get_global_configuration().pg_connection

        db_model: dict[str, Any] = self.adapter.convert_from_create_model_to_database_model(model)

        db_result: dict[str, Any] = connection.insert(
            'pos_simulator_responses',
            db_model,
            request_operators
        )

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def select_by_id(
        self, 
        id: UUID, 
        request_operators: RequestOperators | None = None 
    ) -> PosSimulatorResponseModel:

        connection = get_global_configuration().pg_connection

        db_result = connection.select_by_id(
            'pos_simulator_responses',
            id,
            request_operators
        )

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def select(
        self,
        model: PosSimulatorResponseSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None
    ) -> ItemList[PosSimulatorResponseModel]:

        connection = get_global_configuration().pg_connection

        search_terms: list[SearchTerm] = self.adapter.convert_from_search_model_to_search_terms(model)

        db_result: SelectQueryResults = connection.select(
            'pos_simulator_responses',
            search_terms,
            paging_model,
            request_operators
        )

        results: ItemList[PosSimulatorResponseModel] = ItemList[PosSimulatorResponseModel](db_result.paging)

        if db_result is None:
            return results

        for item in db_result.items:
            result_model = self.adapter.convert_from_database_model_to_model(item)
            results.items.append(result_model)

        return results 

    def delete(
        self,
        id: UUID,
        request_operators: RequestOperators | None = None
    ):

        connection = get_global_configuration().pg_connection

        db_result = connection.delete(
            'pos_simulator_responses',
            id,
            request_operators
        )

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model
