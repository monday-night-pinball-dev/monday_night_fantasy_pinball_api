from managers.fantasy_league_manager import FantasyLeagueManager
from managers.fantasy_team_season_link_manager import FantasyTeamSeasonLinkManager
from managers.league_player_manager import LeaguePlayerManager
from managers.league_team_manager import LeagueTeamManager
from managers.user_manager import UserManager
from managers.venue_manager import VenueManager
from managers.season_manager import SeasonManager
from managers.fantasy_team_manager import FantasyTeamManager
from models.fantasy_league_model import FantasyLeagueSearchModel
from models.fantasy_team_model import FantasyTeamModel, FantasyTeamSearchModel
from models.fantasy_team_season_link_model import (
    FantasyTeamSeasonLinkModel,
    FantasyTeamSeasonLinkSearchModel,
)
from models.league_player_fantasy_team_season_link_model import (
    LeaguePlayerFantasyTeamSeasonLinkModel,
)
from models.league_player_model import LeaguePlayerModel, LeaguePlayerSearchModel
from models.league_team_model import LeagueTeamModel, LeagueTeamSearchModel
from models.season_model import SeasonSearchModel
from models.user_model import UserModel, UserSearchModel
from models.venue_model import VenueModel, VenueSearchModel
from util.common import RequestOperators
from util.hydration import HydrationUtil


class Hydrator:
    def __init__(
        self,
        hydration_util: HydrationUtil = HydrationUtil(),
        venue_manager: VenueManager = VenueManager(),
        league_team_manager: LeagueTeamManager = LeagueTeamManager(),
        league_player_manager: LeaguePlayerManager = LeaguePlayerManager(),
        fantasy_league_manager: FantasyLeagueManager = FantasyLeagueManager(),
        fantasy_team_manager: FantasyTeamManager = FantasyTeamManager(),
        fantasy_team_season_link_manager: FantasyTeamSeasonLinkManager = FantasyTeamSeasonLinkManager(),
        season_manager: SeasonManager = SeasonManager(),
        user_manager: UserManager = UserManager(),
    ) -> None:
        self.venue_manager = venue_manager
        self.hydration_util = hydration_util
        self.league_team_manager = league_team_manager
        self.league_player_manager = league_player_manager
        self.fantasy_league_manager = fantasy_league_manager
        self.fantasy_team_season_link_manager = fantasy_team_season_link_manager
        self.fantasy_team_manager = fantasy_team_manager
        self.season_manager = season_manager
        self.user_manager = user_manager

    def hydrate_venues(
        self,
        result_list: list[VenueModel],
        request_operators: RequestOperators | None = None,
    ):
        pass

    def hydrate_seasons(
        self,
        result_list: list[VenueModel],
        request_operators: RequestOperators | None = None,
    ):
        pass

    def hydrate_league_teams(
        self,
        result_list: list[LeagueTeamModel],
        request_operators: RequestOperators | None = None,
    ):
        # Hydrate league team
        self.hydration_util.hydrate_target(
            "home_venue",
            result_list,
            VenueSearchModel(),
            self.venue_manager.search_venues,
            request_operators.hydration if request_operators is not None else None,
        )

    def hydrate_league_players(
        self,
        result_list: list[LeaguePlayerModel],
        request_operators: RequestOperators | None = None,
    ):
        # Hydrate league team
        self.hydration_util.hydrate_target(
            "league_team",
            result_list,
            LeagueTeamSearchModel(),
            self.league_team_manager.search_league_teams,
            request_operators.hydration if request_operators is not None else None,
        )

    def hydrate_users(
        self,
        result_list: list[UserModel],
        request_operators: RequestOperators | None = None,
    ):
        # Hydrate league player
        self.hydration_util.hydrate_target(
            "league_player",
            result_list,
            LeaguePlayerSearchModel(),
            self.league_player_manager.search_league_players,
            request_operators.hydration if request_operators is not None else None,
        )

    def hydrate_fantasy_teams(
        self,
        result_list: list[FantasyTeamModel],
        request_operators: RequestOperators | None = None,
    ):
        # Example: Hydrate league data if `league_id` exists in the fantasy team model
        self.hydration_util.hydrate_target(
            "fantasy_league",
            result_list,
            FantasyLeagueSearchModel(),
            self.fantasy_league_manager.search_fantasy_leagues,
            request_operators.hydration if request_operators is not None else None,
        )

        # hydrate owner
        self.hydration_util.hydrate_target(
            "owner",
            result_list,
            UserSearchModel(),
            self.user_manager.search_users,
            request_operators.hydration if request_operators is not None else None,
        )

    def hydrate_fantasy_team_season_links(
        self,
        result_list: list[FantasyTeamSeasonLinkModel],
        request_operators: RequestOperators | None = None,
    ):
        # Hydrate season data
        self.hydration_util.hydrate_target(
            "season",
            result_list,
            SeasonSearchModel(),
            self.season_manager.search_seasons,
            request_operators.hydration if request_operators is not None else None,
        )

        # Hydrate fantasy team data
        self.hydration_util.hydrate_target(
            "fantasy_team",
            result_list,
            FantasyTeamSearchModel(),
            self.fantasy_team_manager.search_fantasy_teams,
            request_operators.hydration if request_operators is not None else None,
        )

        # Hydrate fantasy_league data
        self.hydration_util.hydrate_target(
            "fantasy_league",
            result_list,
            FantasyLeagueSearchModel(),
            self.fantasy_league_manager.search_fantasy_leagues,
            request_operators.hydration if request_operators is not None else None,
        )

        # hydrate fantasy_team owner data
        self.hydration_util.hydrate_target(
            "fantasy_team_owner",
            result_list,
            UserSearchModel(),
            self.user_manager.search_users,
            request_operators.hydration if request_operators is not None else None,
        )

    def hydrate_league_player_fantasy_team_season_links(
        self,
        result_list: list[LeaguePlayerFantasyTeamSeasonLinkModel],
        request_operators: RequestOperators | None = None,
    ):
        # Hydrate league player data
        self.hydration_util.hydrate_target(
            "league_player",
            result_list,
            LeaguePlayerSearchModel(),
            self.league_player_manager.search_league_players,
            request_operators.hydration if request_operators is not None else None,
        )
        # Hydrate league Team data
        self.hydration_util.hydrate_target(
            "league_team",
            result_list,
            LeagueTeamSearchModel(),
            self.league_team_manager.search_league_teams,
            request_operators.hydration if request_operators is not None else None,
        )
        # Hydrate fantasy team season link data
        self.hydration_util.hydrate_target(
            "fantasy_team_season_link",
            result_list,
            FantasyTeamSeasonLinkSearchModel(),
            self.fantasy_team_season_link_manager.search_fantasy_team_season_links,
            request_operators.hydration if request_operators is not None else None,
        )

        # Hydrate fantasy team data
        self.hydration_util.hydrate_target(
            "fantasy_team",
            result_list,
            FantasyTeamSearchModel(),
            self.fantasy_team_manager.search_fantasy_teams,
            request_operators.hydration if request_operators is not None else None,
        )
        # Hydrate fantasy_league data
        self.hydration_util.hydrate_target(
            "fantasy_league",
            result_list,
            FantasyLeagueSearchModel(),
            self.fantasy_league_manager.search_fantasy_leagues,
            request_operators.hydration if request_operators is not None else None,
        )
        # hydrate fantasy_team owner data
        self.hydration_util.hydrate_target(
            "fantasy_team_owner",
            result_list,
            UserSearchModel(),
            self.user_manager.search_users,
            request_operators.hydration if request_operators is not None else None,
        )
        # Hydrate season data
        self.hydration_util.hydrate_target(
            "season",
            result_list,
            SeasonSearchModel(),
            self.season_manager.search_seasons,
            request_operators.hydration if request_operators is not None else None,
        )
