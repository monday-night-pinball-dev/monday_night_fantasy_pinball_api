from uuid import UUID
from data_accessors.fantasy_team_accessor import FantasyTeamAccessor
from data_accessors.fantasy_team_season_link_accessor import (
    FantasyTeamSeasonLinkAccessor,
)
from data_accessors.league_player_accessor import LeaguePlayerAccessor
from data_accessors.league_player_fantasy_team_season_link_accessor import (
    LeaguePlayerFantasyTeamSeasonLinkAccessor,
)
from models.common_model import ItemList
from models.league_player_fantasy_team_season_link_model import (
    LeaguePlayerFantasyTeamSeasonLinkCreateModel,
    LeaguePlayerFantasyTeamSeasonLinkModel,
    LeaguePlayerFantasyTeamSeasonLinkSearchModel,
)
from util.common import CommonUtilities, RequestOperators
from util.database import PagingModel


class LeaguePlayerFantasyTeamSeasonLinkManager:
    def __init__(
        self,
        league_player_fantasy_team_season_link_accessor: LeaguePlayerFantasyTeamSeasonLinkAccessor = LeaguePlayerFantasyTeamSeasonLinkAccessor(),
        fantasy_team_season_link_accessor: FantasyTeamSeasonLinkAccessor = FantasyTeamSeasonLinkAccessor(),
        league_player_accessor: LeaguePlayerAccessor = LeaguePlayerAccessor(),
        common_utilities: CommonUtilities = CommonUtilities(),
    ) -> None:
        self.league_player_fantasy_team_season_link_accessor = (
            league_player_fantasy_team_season_link_accessor
        )
        self.fantasy_team_season_link_accessor = fantasy_team_season_link_accessor
        self.league_player_accessor = league_player_accessor
        self.common_utilities = common_utilities

    def create_league_player_fantasy_team_season_link(
        self,
        inbound_model: LeaguePlayerFantasyTeamSeasonLinkCreateModel,
        request_operators: RequestOperators | None = None,
    ) -> LeaguePlayerFantasyTeamSeasonLinkModel | None:
        # get fantasy team for parent ids
        fantasy_team_season_link = self.fantasy_team_season_link_accessor.select_by_id(
            inbound_model.fantasy_team_season_link_id
        )

        if fantasy_team_season_link is None:
            raise ValueError(
                f"Fantasy team season link with id {inbound_model.fantasy_team_season_link_id} does not exist."
            )

        league_player = self.league_player_accessor.select_by_id(
            inbound_model.league_player_id
        )
        if league_player is None:
            raise ValueError(
                f"League player with id {inbound_model.league_player_id} does not exist."
            )

        inbound_model.league_team_id = league_player.league_team_id

        inbound_model.season_id = fantasy_team_season_link.season_id
        inbound_model.fantasy_team_id = fantasy_team_season_link.fantasy_team_id
        inbound_model.fantasy_league_id = fantasy_team_season_link.fantasy_league_id
        inbound_model.fantasy_team_owner_id = (
            fantasy_team_season_link.fantasy_team_owner_id
        )

        result = self.league_player_fantasy_team_season_link_accessor.insert(
            model=inbound_model, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_league_player_fantasy_team_season_links(
            [result], request_operators
        )

        return result

    def get_league_player_fantasy_team_season_link_by_id(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> LeaguePlayerFantasyTeamSeasonLinkModel | None:
        result = self.league_player_fantasy_team_season_link_accessor.select_by_id(
            id=id, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_league_player_fantasy_team_season_links(
            [result], request_operators
        )

        return result

    def search_league_player_fantasy_team_season_links(
        self,
        model: LeaguePlayerFantasyTeamSeasonLinkSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None,
    ) -> ItemList[LeaguePlayerFantasyTeamSeasonLinkModel]:
        result = self.league_player_fantasy_team_season_link_accessor.select(
            model=model, paging_model=paging_model, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_league_player_fantasy_team_season_links(
            result.items, request_operators
        )

        return result

    def delete_league_player_fantasy_team_season_link(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> LeaguePlayerFantasyTeamSeasonLinkModel | None:
        result: None | LeaguePlayerFantasyTeamSeasonLinkModel = (
            self.league_player_fantasy_team_season_link_accessor.delete(
                id=id, request_operators=request_operators
            )
        )

        return result
