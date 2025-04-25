from uuid import UUID
from data_accessors.fantasy_team_accessor import FantasyTeamAccessor
from models.common_model import ItemList
from models.fantasy_team_model import (
    FantasyTeamCreateModel,
    FantasyTeamModel,
    FantasyTeamSearchModel,
    FantasyTeamUpdateModel,
)
from util.common import CommonUtilities, RequestOperators
from util.database import PagingModel


class FantasyTeamManager:
    def __init__(
        self,
        fantasy_team_accessor: FantasyTeamAccessor = FantasyTeamAccessor(),
        common_utilities: CommonUtilities = CommonUtilities(),
    ) -> None:
        self.fantasy_team_accessor = fantasy_team_accessor
        self.common_utilities = common_utilities

    def create_fantasy_team(
        self,
        inbound_model: FantasyTeamCreateModel,
        request_operators: RequestOperators | None = None,
    ) -> FantasyTeamModel | None:
        result = self.fantasy_team_accessor.insert(
            model=inbound_model, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_fantasy_teams([result], request_operators)

        return result

    def get_fantasy_team_by_id(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> FantasyTeamModel | None:
        result = self.fantasy_team_accessor.select_by_id(
            id=id, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_fantasy_teams([result], request_operators)

        return result

    def search_fantasy_teams(
        self,
        model: FantasyTeamSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None,
    ) -> ItemList[FantasyTeamModel]:
        result = self.fantasy_team_accessor.select(
            model=model, paging_model=paging_model, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_fantasy_teams(result.items, request_operators)

        return result

    def update_league_player(
        self,
        id: UUID,
        model: FantasyTeamUpdateModel,
        request_operators: RequestOperators | None = None,
    ) -> FantasyTeamModel | None:
        result = self.fantasy_team_accessor.update(id, model, request_operators)

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_fantasy_teams([result], request_operators)

        return result

    def delete_fantasy_team(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> FantasyTeamModel | None:
        result: None | FantasyTeamModel = self.fantasy_team_accessor.delete(
            id=id, request_operators=request_operators
        )

        return result
