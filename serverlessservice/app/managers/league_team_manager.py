from uuid import UUID
from data_accessors.league_team_accessor import LeagueTeamAccessor
from models.common_model import ItemList
from models.league_team_model import (
    LeagueTeamCreateModel,
    LeagueTeamModel,
    LeagueTeamSearchModel,
    LeagueTeamUpdateModel,
)
from util.common import CommonUtilities, RequestOperators
from util.database import PagingModel


class LeagueTeamManager:
    def __init__(
        self,
        league_team_accessor: LeagueTeamAccessor = LeagueTeamAccessor(),
        common_utilities: CommonUtilities = CommonUtilities(),
    ) -> None:
        self.league_team_accessor = league_team_accessor
        self.common_utilities = common_utilities

    def create_league_team(
        self,
        inbound_model: LeagueTeamCreateModel,
        request_operators: RequestOperators | None = None,
    ) -> LeagueTeamModel | None:
        result = self.league_team_accessor.insert(
            model=inbound_model, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_league_teams([result], request_operators)

        return result

    def get_league_team_by_id(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> LeagueTeamModel | None:
        result = self.league_team_accessor.select_by_id(
            id=id, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_league_teams([result], request_operators)

        return result

    def search_league_teams(
        self,
        model: LeagueTeamSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None,
    ) -> ItemList[LeagueTeamModel]:
        result = self.league_team_accessor.select(
            model=model, paging_model=paging_model, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_league_teams(result.items, request_operators)

        return result

    def update_league_team(
        self,
        id: UUID,
        model: LeagueTeamUpdateModel,
        request_operators: RequestOperators | None = None,
    ) -> LeagueTeamModel | None:
        result = self.league_team_accessor.update(id, model, request_operators)

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_league_teams([result], request_operators)

        return result

    def delete_league_team(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> LeagueTeamModel | None:
        result: None | LeagueTeamModel = self.league_team_accessor.delete(
            id=id, request_operators=request_operators
        )

        return result
