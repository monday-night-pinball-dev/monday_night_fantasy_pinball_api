from typing import Any
from uuid import UUID
from adapters.fantasy_league_adapters import FantasyLeagueAdapter
from models.fantasy_league_model import (
    FantasyLeagueCreateModel,
    FantasyLeagueModel,
    FantasyLeagueSearchModel,
    FantasyLeagueUpdateModel,
)
from models.common_model import ItemList
from util.common import RequestOperators
from util.configuration import get_global_configuration
from util.database import PagingModel, SearchTerm
from util.db_connection import SelectQueryResults


class FantasyLeagueAccessor:
    def __init__(self, adapter: FantasyLeagueAdapter = FantasyLeagueAdapter()) -> None:
        self.adapter = adapter

    def insert(
        self,
        model: FantasyLeagueCreateModel,
        request_operators: RequestOperators | None = None,
    ) -> FantasyLeagueModel:
        connection = get_global_configuration().pg_connection

        db_model: dict[str, Any] = (
            self.adapter.convert_from_create_model_to_database_model(model)
        )

        db_result: dict[str, Any] = connection.insert(
            "fantasy_leagues", db_model, request_operators
        )

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def select_by_id(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> FantasyLeagueModel:
        connection = get_global_configuration().pg_connection

        db_result = connection.select_by_id("fantasy_leagues", id, request_operators)

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def select(
        self,
        model: FantasyLeagueSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None,
    ) -> ItemList[FantasyLeagueModel]:
        connection = get_global_configuration().pg_connection

        search_terms: list[SearchTerm] = (
            self.adapter.convert_from_search_model_to_search_terms(model)
        )

        db_result: SelectQueryResults = connection.select(
            "fantasy_leagues", search_terms, paging_model, request_operators
        )

        results: ItemList[FantasyLeagueModel] = ItemList[FantasyLeagueModel](
            db_result.paging
        )

        if db_result is None:
            return results

        for item in db_result.items:
            result_model = self.adapter.convert_from_database_model_to_model(item)
            results.items.append(result_model)

        return results

    def update(
        self,
        id: UUID,
        model: FantasyLeagueUpdateModel,
        request_operators: RequestOperators | None = None,
    ) -> FantasyLeagueModel:
        connection = get_global_configuration().pg_connection

        db_model: dict[str, Any] = (
            self.adapter.convert_from_update_model_to_database_model(model)
        )

        db_result = connection.update(
            "fantasy_leagues", id, db_model, request_operators
        )

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def delete(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> FantasyLeagueModel:
        connection = get_global_configuration().pg_connection

        db_result = connection.delete("fantasy_leagues", id, request_operators)

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model
