from typing import Any
from uuid import UUID
from adapters.fantasy_team_season_link_adapters import FantasyTeamSeasonLinkAdapter
from models.fantasy_team_season_link_model import (
    FantasyTeamSeasonLinkCreateModel,
    FantasyTeamSeasonLinkModel,
    FantasyTeamSeasonLinkSearchModel,
)
from models.common_model import ItemList
from util.common import RequestOperators
from util.configuration import get_global_configuration
from util.database import PagingModel, SearchTerm
from util.db_connection import SelectQueryResults


class FantasyTeamSeasonLinkAccessor:
    def __init__(
        self, adapter: FantasyTeamSeasonLinkAdapter = FantasyTeamSeasonLinkAdapter()
    ) -> None:
        self.adapter = adapter

    def insert(
        self,
        model: FantasyTeamSeasonLinkCreateModel,
        request_operators: RequestOperators | None = None,
    ) -> FantasyTeamSeasonLinkModel:
        connection = get_global_configuration().pg_connection

        db_model: dict[str, Any] = (
            self.adapter.convert_from_create_model_to_database_model(model)
        )

        db_result: dict[str, Any] = connection.insert(
            "fantasy_team_season_links", db_model, request_operators
        )

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def select_by_id(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> FantasyTeamSeasonLinkModel:
        connection = get_global_configuration().pg_connection

        db_result = connection.select_by_id(
            "fantasy_team_season_links", id, request_operators
        )

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def select(
        self,
        model: FantasyTeamSeasonLinkSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None,
    ) -> ItemList[FantasyTeamSeasonLinkModel]:
        connection = get_global_configuration().pg_connection

        search_terms: list[SearchTerm] = (
            self.adapter.convert_from_search_model_to_search_terms(model)
        )

        db_result: SelectQueryResults = connection.select(
            "fantasy_team_season_links", search_terms, paging_model, request_operators
        )

        results: ItemList[FantasyTeamSeasonLinkModel] = ItemList[
            FantasyTeamSeasonLinkModel
        ](db_result.paging)

        if db_result is None:
            return results

        for item in db_result.items:
            result_model = self.adapter.convert_from_database_model_to_model(item)
            results.items.append(result_model)

        return results

    def delete(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> FantasyTeamSeasonLinkModel:
        connection = get_global_configuration().pg_connection

        db_result = connection.delete(
            "fantasy_team_season_links", id, request_operators
        )

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model
