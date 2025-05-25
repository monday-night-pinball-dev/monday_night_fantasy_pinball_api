from typing import Any
from uuid import UUID
from adapters.venue_adapters import VenueAdapter
from models.venue_model import (
    VenueCreateModel,
    VenueModel,
    VenueSearchModel,
    VenueUpdateModel,
)
from models.common_model import ItemList
from util.common import RequestOperators
from util.configuration import get_global_configuration
from util.database import PagingModel, SearchTerm
from util.db_connection import SelectQueryResults


class VenueAccessor:
    def __init__(self, adapter: VenueAdapter = VenueAdapter()) -> None:
        self.adapter = adapter

    def insert(
        self,
        model: VenueCreateModel,
        request_operators: RequestOperators | None = None,
    ) -> VenueModel:
        connection = get_global_configuration().pg_connection

        db_model: dict[str, Any] = (
            self.adapter.convert_from_create_model_to_database_model(model)
        )

        db_result: dict[str, Any] = connection.insert(
            "venues", db_model, request_operators
        )

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def select_by_id(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> VenueModel:
        connection = get_global_configuration().pg_connection

        db_result = connection.select_by_id("venues", id, request_operators)

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def select(
        self,
        model: VenueSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None,
    ) -> ItemList[VenueModel]:
        connection = get_global_configuration().pg_connection

        search_terms: list[SearchTerm] = (
            self.adapter.convert_from_search_model_to_search_terms(model)
        )

        db_result: SelectQueryResults = connection.select(
            "venues", search_terms, paging_model, request_operators
        )

        results: ItemList[VenueModel] = ItemList[VenueModel](db_result.paging)

        if db_result is None:
            return results

        for item in db_result.items:
            result_model = self.adapter.convert_from_database_model_to_model(item)
            results.items.append(result_model)

        return results

    def update(
        self,
        id: UUID,
        model: VenueUpdateModel,
        request_operators: RequestOperators | None = None,
    ) -> VenueModel:
        connection = get_global_configuration().pg_connection

        db_model: dict[str, Any] = (
            self.adapter.convert_from_update_model_to_database_model(model)
        )

        db_result: dict[str, Any] = connection.update(
            "venues", id, db_model, request_operators
        )

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def delete(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> VenueModel:
        connection = get_global_configuration().pg_connection

        db_result = connection.delete("venues", id, request_operators)

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model
