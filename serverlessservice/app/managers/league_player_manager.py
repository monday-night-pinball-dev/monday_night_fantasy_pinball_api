from uuid import UUID
from data_accessors.league_player_accessor import LeaguePlayerAccessor
from models.common_model import ItemList
from models.league_player_model import (
    LeaguePlayerCreateModel,
    LeaguePlayerModel,
    LeaguePlayerSearchModel,
    LeaguePlayerUpdateModel,
)
from util.common import CommonUtilities, RequestOperators
from util.database import PagingModel


class LeaguePlayerManager:
    def __init__(
        self,
        league_player_accessor: LeaguePlayerAccessor = LeaguePlayerAccessor(),
        common_utilities: CommonUtilities = CommonUtilities(),
    ) -> None:
        self.league_player_accessor = league_player_accessor
        self.common_utilities = common_utilities

    def create_league_player(
        self,
        inbound_model: LeaguePlayerCreateModel,
        request_operators: RequestOperators | None = None,
    ) -> LeaguePlayerModel | None:
        result = self.league_player_accessor.insert(
            model=inbound_model, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_league_players([result], request_operators)

        return result

    def get_league_player_by_id(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> LeaguePlayerModel | None:
        result = self.league_player_accessor.select_by_id(
            id=id, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_league_players([result], request_operators)

        return result

    def search_league_players(
        self,
        model: LeaguePlayerSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None,
    ) -> ItemList[LeaguePlayerModel]:
        result = self.league_player_accessor.select(
            model=model, paging_model=paging_model, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_league_players(result.items, request_operators)

        return result

    def update_league_player(
        self,
        id: UUID,
        model: LeaguePlayerUpdateModel,
        request_operators: RequestOperators | None = None,
    ) -> LeaguePlayerModel | None:
        result = self.league_player_accessor.update(id, model, request_operators)

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_league_players([result], request_operators)

        return result

    def delete_league_player(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> LeaguePlayerModel | None:
        result: None | LeaguePlayerModel = self.league_player_accessor.delete(
            id=id, request_operators=request_operators
        )

        return result
