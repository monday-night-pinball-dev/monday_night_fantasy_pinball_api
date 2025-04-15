from managers.league_player_manager import LeaguePlayerManager
from managers.league_team_manager import LeagueTeamManager
from managers.user_manager import UserManager
from managers.venue_manager import VenueManager
from models.fantasy_league_model import FantasyLeagueModel
from models.league_player_model import LeaguePlayerModel, LeaguePlayerSearchModel
from models.league_team_model import LeagueTeamModel, LeagueTeamSearchModel
from models.user_model import UserModel
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
        user_manager: UserManager = UserManager(),
    ) -> None:
        self.venue_manager = venue_manager
        self.hydration_util = hydration_util
        self.league_team_manager = league_team_manager
        self.league_player_manager = league_player_manager
        self.user_manager = user_manager

    def hydrate_venues(
        self,
        result_list: list[VenueModel],
        request_operators: RequestOperators | None = None,
    ):
        self.hydrate_league_teams(result_list, request_operators)
        return

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
