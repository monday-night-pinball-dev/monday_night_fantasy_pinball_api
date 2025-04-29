from requests import Response
from tests.qdk.operators.fantasy_leagues import (
    FantasyLeagueModel,
)
from tests.qdk.operators.fantasy_team_season_links import (
    FantasyTeamSeasonLinkCreateModel,
    FantasyTeamSeasonLinkModel,
    create_fantasy_team_season_link,
)
from tests.qdk.operators.fantasy_teams import (
    FantasyTeamCreateModel,
    FantasyTeamModel,
    create_fantasy_team,
)
from tests.qdk.operators.league_players import (
    LeaguePlayerCreateModel,
    LeaguePlayerModel,
    create_league_player,
)
from tests.qdk.operators.league_teams import LeagueTeamModel
from tests.qdk.operators.seasons import SeasonCreateModel, SeasonModel, create_season
from tests.qdk.operators.users import UserModel

from tests.qdk.qa_requests import qa_get, qa_post
from tests.qdk.types import (
    PagedResponseItemList,
    PagingRequestModel,
    PagingResponseModel,
    RequestOperators,
    TestContext,
)
from tests.qdk.utils import (
    assert_objects_are_equal,
    copy_object_when_appropriate,
)


class LeaguePlayerFantasyTeamSeasonLinkCreateModel:
    def __init__(
        self,
        league_player_id: str | None = None,
        league_player: LeaguePlayerCreateModel | None = None,
        fantasy_team_season_link_id: str | None = None,
        fantasy_team_season_link: FantasyTeamSeasonLinkCreateModel | None = None,
    ) -> None:
        self.league_player_id = league_player_id
        self.league_player = league_player
        self.fantasy_team_season_link_id = fantasy_team_season_link_id
        self.fantasy_team_season_link = fantasy_team_season_link


class LeaguePlayerFantasyTeamSeasonLinkModel:
    def __init__(
        self,
        id: str,
        league_player_id: str,
        league_team_id: str,
        fantasy_team_season_link_id: str,
        season_id: str,
        fantasy_team_id: str,
        fantasy_team_owner_id: str,
        fantasy_league_id: str,
        created_at: str,
        league_player: LeaguePlayerModel | None = None,
        league_team: LeagueTeamModel | None = None,
        fantasy_team_season_link: FantasyTeamSeasonLinkModel | None = None,
        season: SeasonModel | None = None,
        fantasy_team: FantasyTeamModel | None = None,
        fantasy_team_owner: UserModel | None = None,
        fantasy_league: FantasyLeagueModel | None = None,
        updated_at: str | None = None,
    ) -> None:
        self.id = id
        self.league_player_id = league_player_id
        self.league_team_id = league_team_id
        self.fantasy_team_season_link_id = fantasy_team_season_link_id
        self.season_id = season_id
        self.fantasy_team_id = fantasy_team_id
        self.fantasy_team_owner_id = fantasy_team_owner_id
        self.fantasy_league_id = fantasy_league_id
        self.league_player = (
            LeaguePlayerModel(**league_player) if league_player else None
        )
        self.league_team = LeagueTeamModel(**league_team) if league_team else None
        self.fantasy_team_season_link = (
            FantasyTeamSeasonLinkModel(**fantasy_team_season_link)
            if fantasy_team_season_link
            else None
        )
        self.season = SeasonModel(**season) if season else None
        self.fantasy_team = FantasyTeamModel(**fantasy_team) if fantasy_team else None
        self.fantasy_team_owner = (
            UserModel(**fantasy_team_owner) if fantasy_team_owner else None
        )
        self.fantasy_league = (
            FantasyLeagueModel(**fantasy_league) if fantasy_league else None
        )

        self.created_at = created_at
        self.updated_at = updated_at


class LeaguePlayerFantasyTeamSeasonLinkSearchModel(PagingRequestModel):
    def __init__(
        self,
        ids: str | None = None,
        league_player_ids: str | None = None,
        league_team_ids: str | None = None,
        fantasy_team_season_link_ids: str | None = None,
        fantasy_team_ids: str | None = None,
        fantasy_team_owner_ids: str | None = None,
        fantasy_league_ids: str | None = None,
        season_ids: str | None = None,
        page: int | None = None,
        page_length: int | None = None,
        is_sort_descending: bool | None = None,
        sort_by: str | None = None,
    ) -> None:
        super().__init__(
            page=page,
            page_length=page_length,
            is_sort_descending=is_sort_descending,
            sort_by=sort_by,
        )

        self.ids = ids
        self.league_player_ids = league_player_ids
        self.league_team_ids = league_team_ids
        self.fantasy_team_season_link_ids = fantasy_team_season_link_ids
        self.fantasy_team_ids = fantasy_team_ids
        self.fantasy_team_owner_ids = fantasy_team_owner_ids
        self.fantasy_league_ids = fantasy_league_ids
        self.season_ids = season_ids


def mint_default_league_player_fantasy_team_season_link(
    context: TestContext,
    overrides: LeaguePlayerFantasyTeamSeasonLinkCreateModel | None = None,
    request_operators: RequestOperators | None = None,
) -> LeaguePlayerFantasyTeamSeasonLinkCreateModel:
    overrides = overrides or LeaguePlayerFantasyTeamSeasonLinkCreateModel()

    default_obj = LeaguePlayerFantasyTeamSeasonLinkCreateModel()

    if overrides.league_player_id is None:
        new_league_player = create_league_player(context, overrides.league_player)
        default_obj.league_player_id = new_league_player.id

        del overrides.league_player

    if overrides.fantasy_team_season_link_id is None:
        new_fantasy_team_season_link = create_fantasy_team_season_link(
            context, overrides.fantasy_team_season_link
        )
        default_obj.fantasy_team_season_link_id = new_fantasy_team_season_link.id

        del overrides.fantasy_team_season_link

    copy_object_when_appropriate(default_obj, overrides)

    return default_obj


def create_league_player_fantasy_team_season_link(
    context: TestContext,
    overrides: LeaguePlayerFantasyTeamSeasonLinkCreateModel | None = None,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
) -> LeaguePlayerFantasyTeamSeasonLinkModel:
    post_object = mint_default_league_player_fantasy_team_season_link(
        context=context, overrides=overrides, request_operators=request_operators
    )

    result = qa_post(
        context.api_url + "/league_player_fantasy_team_season_links",
        post_object,
        request_operators,
    )

    if not allow_failures:
        assert result.status_code == 201

        result_dict = result.json()

        assert_objects_are_equal(
            result_dict,
            post_object.__dict__,
            [
                "id",
                "league_team_id",
                "season_id",
                "fantasy_team_id",
                "fantasy_team_owner_id",
                "fantasy_league_id",
                "league_player",
                "league_team",
                "fantasy_team_season_link",
                "season",
                "fantasy_team",
                "fantasy_team_owner",
                "fantasy_league",
                "created_at",
                "updated_at",
            ],
        )

        assert result_dict["id"] is not None
        assert result_dict["created_at"] is not None
        assert result_dict["updated_at"] is None

    return LeaguePlayerFantasyTeamSeasonLinkModel(**result.json())


def get_league_player_fantasy_team_season_link_by_id(
    context: TestContext,
    id: str,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
):
    url = f"{context.api_url}/league_player_fantasy_team_season_links/{id}"

    result = qa_get(url, request_operators=request_operators)

    return_object = LeaguePlayerFantasyTeamSeasonLinkModel(**result.json())

    return return_object


def get_league_player_fantasy_team_season_links(
    context: TestContext,
    search_model: LeaguePlayerFantasyTeamSeasonLinkSearchModel | None,
    request_operators: RequestOperators | None = None,
) -> PagedResponseItemList[LeaguePlayerFantasyTeamSeasonLinkModel]:
    url: str = f"{context.api_url}/league_player_fantasy_team_season_links"

    result: Response = qa_get(
        url=url,
        query_params=search_model if search_model is not None else {},
        request_operators=request_operators,
    )

    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict["paging"])

    return_items: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        LeaguePlayerFantasyTeamSeasonLinkModel(**obj) for obj in result_dict["items"]
    ]

    return_object = PagedResponseItemList[LeaguePlayerFantasyTeamSeasonLinkModel](
        items=return_items, paging=return_paging_object
    )

    return return_object


def league_player_fantasy_team_season_link_hydration_check(
    league_player_fantasy_team_season_link: LeaguePlayerFantasyTeamSeasonLinkModel,
) -> None:
    assert league_player_fantasy_team_season_link.league_player is not None
    assert league_player_fantasy_team_season_link.league_player.id is not None
    assert (
        league_player_fantasy_team_season_link.league_player.id
        == league_player_fantasy_team_season_link.league_player_id
    )

    assert league_player_fantasy_team_season_link.league_team is not None
    assert league_player_fantasy_team_season_link.league_team.id is not None
    assert (
        league_player_fantasy_team_season_link.league_team.id
        == league_player_fantasy_team_season_link.league_team_id
    )

    assert league_player_fantasy_team_season_link.fantasy_team_season_link is not None
    assert (
        league_player_fantasy_team_season_link.fantasy_team_season_link.id is not None
    )
    assert (
        league_player_fantasy_team_season_link.fantasy_team_season_link.id
        == league_player_fantasy_team_season_link.fantasy_team_season_link_id
    )

    assert league_player_fantasy_team_season_link.season is not None
    assert league_player_fantasy_team_season_link.season.id is not None
    assert (
        league_player_fantasy_team_season_link.season.id
        == league_player_fantasy_team_season_link.season_id
    )

    assert league_player_fantasy_team_season_link.fantasy_team is not None
    assert league_player_fantasy_team_season_link.fantasy_team.id is not None
    assert (
        league_player_fantasy_team_season_link.fantasy_team.id
        == league_player_fantasy_team_season_link.fantasy_team_id
    )

    assert league_player_fantasy_team_season_link.fantasy_team_owner is not None
    assert league_player_fantasy_team_season_link.fantasy_team_owner.id is not None
    assert (
        league_player_fantasy_team_season_link.fantasy_team_owner.id
        == league_player_fantasy_team_season_link.fantasy_team_owner_id
    )

    assert league_player_fantasy_team_season_link.fantasy_league is not None
    assert league_player_fantasy_team_season_link.fantasy_league.id is not None
    assert (
        league_player_fantasy_team_season_link.fantasy_league.id
        == league_player_fantasy_team_season_link.fantasy_league_id
    )
