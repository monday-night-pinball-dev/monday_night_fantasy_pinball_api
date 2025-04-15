from uuid import UUID
from data_accessors.fantasy_league_accessor import FantasyLeagueAccessor
from models.common_model import ItemList
from models.fantasy_league_model import (
    FantasyLeagueCreateModel,
    FantasyLeagueModel,
    FantasyLeagueSearchModel,
    FantasyLeagueUpdateModel,
)
from util.common import CommonUtilities, RequestOperators
from util.database import PagingModel


class FantasyLeagueManager:
    def __init__(
        self,
        fantasy_league_accessor: FantasyLeagueAccessor = FantasyLeagueAccessor(),
        common_utilities: CommonUtilities = CommonUtilities(),
    ) -> None:
        self.fantasy_league_accessor = fantasy_league_accessor
        self.common_utilities = common_utilities

    def create_fantasy_league(
        self,
        inbound_model: FantasyLeagueCreateModel,
        request_operators: RequestOperators | None = None,
    ) -> FantasyLeagueModel | None:
        result = self.fantasy_league_accessor.insert(
            model=inbound_model, request_operators=request_operators
        )

        return result

    def get_fantasy_league_by_id(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> FantasyLeagueModel | None:
        result = self.fantasy_league_accessor.select_by_id(
            id=id, request_operators=request_operators
        )

        return result

    def search_fantasy_leagues(
        self,
        model: FantasyLeagueSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None,
    ) -> ItemList[FantasyLeagueModel]:
        result = self.fantasy_league_accessor.select(
            model=model, paging_model=paging_model, request_operators=request_operators
        )

        return result

    def update_league_player(
        self,
        id: UUID,
        model: FantasyLeagueUpdateModel,
        request_operators: RequestOperators | None = None,
    ) -> FantasyLeagueModel | None:
        result = self.fantasy_league_accessor.update(id, model, request_operators)

        return result

    def delete_fantasy_league(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> FantasyLeagueModel | None:
        result: None | FantasyLeagueModel = self.fantasy_league_accessor.delete(
            id=id, request_operators=request_operators
        )

        return result
