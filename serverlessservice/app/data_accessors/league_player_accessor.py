from typing import Any
from uuid import UUID
from adapters.league_player_adapters import LeaguePlayerAdapter, LeaguePlayerAdapter
from models.league_player_model import (
    LeaguePlayerCreateModel,
    LeaguePlayerModel,
    LeaguePlayerSearchModel,
    LeaguePlayerUpdateModel,
)
from models.common_model import ItemList
from util.common import RequestOperators
from util.configuration import get_global_configuration
from util.database import PagingModel, SearchTerm
from util.db_connection import SelectQueryResults


class LeaguePlayerAccessor:
    def __init__(
        self,
        adapter: LeaguePlayerAdapter = LeaguePlayerAdapter(),
    ) -> None:
        self.adapter = adapter

    def insert(
        self,
        model: LeaguePlayerCreateModel,
        request_operators: RequestOperators | None = None,
    ) -> LeaguePlayerModel:
        connection = get_global_configuration().pg_connection

        db_model: dict[str, Any] = (
            self.adapter.convert_from_create_model_to_database_model(model)
        )

        db_result: dict[str, Any] = connection.insert(
            "league_players", db_model, request_operators
        )

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def select_by_id(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> LeaguePlayerModel:
        connection = get_global_configuration().pg_connection

        db_result = connection.select_by_id("league_players", id, request_operators)

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def select(
        self,
        model: LeaguePlayerSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None,
    ) -> ItemList[LeaguePlayerModel]:
        connection = get_global_configuration().pg_connection

        search_terms: list[SearchTerm] = (
            self.adapter.convert_from_search_model_to_search_terms(model)
        )

        db_result: SelectQueryResults = connection.select(
            "league_players", search_terms, paging_model, request_operators
        )

        results: ItemList[LeaguePlayerModel] = ItemList[LeaguePlayerModel](
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
        model: LeaguePlayerUpdateModel,
        request_operators: RequestOperators | None = None,
    ) -> LeaguePlayerModel:
        connection = get_global_configuration().pg_connection

        db_model: dict[str, Any] = (
            self.adapter.convert_from_update_model_to_database_model(model)
        )

        db_result = connection.update("league_players", id, db_model, request_operators)

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def delete(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> LeaguePlayerModel:
        connection = get_global_configuration().pg_connection

        db_result = connection.delete("league_players", id, request_operators)

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model
