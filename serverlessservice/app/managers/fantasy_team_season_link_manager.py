from uuid import UUID
from data_accessors.fantasy_team_accessor import FantasyTeamAccessor
from data_accessors.fantasy_team_season_link_accessor import (
    FantasyTeamSeasonLinkAccessor,
)
from models.common_model import ItemList
from models.fantasy_team_season_link_model import (
    FantasyTeamSeasonLinkCreateModel,
    FantasyTeamSeasonLinkModel,
    FantasyTeamSeasonLinkSearchModel,
)
from util.common import CommonUtilities, RequestOperators
from util.database import PagingModel


class FantasyTeamSeasonLinkManager:
    def __init__(
        self,
        fantasy_team_season_link_accessor: FantasyTeamSeasonLinkAccessor = FantasyTeamSeasonLinkAccessor(),
        fantasy_team_accessor: FantasyTeamAccessor = FantasyTeamAccessor(),
        common_utilities: CommonUtilities = CommonUtilities(),
    ) -> None:
        self.fantasy_team_season_link_accessor = fantasy_team_season_link_accessor
        self.fantasy_team_accessor = fantasy_team_accessor
        self.common_utilities = common_utilities

    def create_fantasy_team_season_link(
        self,
        inbound_model: FantasyTeamSeasonLinkCreateModel,
        request_operators: RequestOperators | None = None,
    ) -> FantasyTeamSeasonLinkModel | None:
        # get fantasy team for parent ids
        fantasy_team = self.fantasy_team_accessor.select_by_id(
            inbound_model.fantasy_team_id
        )

        if fantasy_team is None:
            raise ValueError(
                f"Fantasy team with id {inbound_model.fantasy_team_id} does not exist."
            )

        inbound_model.fantasy_team_owner_id = fantasy_team.owner_id
        inbound_model.fantasy_league_id = fantasy_team.fantasy_league_id

        result = self.fantasy_team_season_link_accessor.insert(
            model=inbound_model, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_fantasy_team_season_links([result], request_operators)

        return result

    def get_fantasy_team_season_link_by_id(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> FantasyTeamSeasonLinkModel | None:
        result = self.fantasy_team_season_link_accessor.select_by_id(
            id=id, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_fantasy_team_season_links([result], request_operators)

        return result

    def search_fantasy_team_season_links(
        self,
        model: FantasyTeamSeasonLinkSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None,
    ) -> ItemList[FantasyTeamSeasonLinkModel]:
        result = self.fantasy_team_season_link_accessor.select(
            model=model, paging_model=paging_model, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_fantasy_team_season_links(result.items, request_operators)

        return result

    def delete_fantasy_team_season_link(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> FantasyTeamSeasonLinkModel | None:
        result: None | FantasyTeamSeasonLinkModel = (
            self.fantasy_team_season_link_accessor.delete(
                id=id, request_operators=request_operators
            )
        )

        return result
