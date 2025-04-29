from requests import Response
from tests.qdk.operators.fantasy_leagues import (
    FantasyLeagueModel,
)
from tests.qdk.operators.fantasy_teams import (
    FantasyTeamCreateModel,
    FantasyTeamModel,
    create_fantasy_team,
)
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


class FantasyTeamSeasonLinkCreateModel:
    def __init__(
        self,
        season_id: str | None = None,
        season: SeasonCreateModel | None = None,
        fantasy_team_id: str | None = None,
        fantasy_team: FantasyTeamCreateModel | None = None,
    ) -> None:
        self.season_id = season_id
        self.season = season
        self.fantasy_team_id = fantasy_team_id
        self.fantasy_team = fantasy_team


class FantasyTeamSeasonLinkModel:
    def __init__(
        self,
        id: str,
        fantasy_team_owner_id: str,
        season_id: str,
        fantasy_team_id: str,
        fantasy_league_id: str,
        created_at: str,
        season: SeasonModel | None = None,
        fantasy_team: FantasyTeamModel | None = None,
        fantasy_team_owner: UserModel | None = None,
        fantasy_league: FantasyLeagueModel | None = None,
        updated_at: str | None = None,
    ) -> None:
        self.id = id
        self.season_id = season_id
        self.season = SeasonModel(**season) if season else None
        self.fantasy_team_id = fantasy_team_id
        self.fantasy_team = FantasyTeamModel(**fantasy_team) if fantasy_team else None
        self.fantasy_league_id = fantasy_league_id
        self.fantasy_league = (
            FantasyLeagueModel(**fantasy_league) if fantasy_league else None
        )
        self.fantasy_team_owner_id = fantasy_team_owner_id
        self.fantasy_team_owner = (
            UserModel(**fantasy_team_owner) if fantasy_team_owner else None
        )
        self.created_at = created_at
        self.updated_at = updated_at


class FantasyTeamSeasonLinkSearchModel(PagingRequestModel):
    def __init__(
        self,
        ids: str | None = None,
        season_ids: str | None = None,
        fantasy_team_ids: str | None = None,
        fantasy_team_owner_ids: str | None = None,
        fantasy_league_ids: str | None = None,
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
        self.season_ids = season_ids
        self.fantasy_league_ids = fantasy_league_ids
        self.fantasy_team_ids = fantasy_team_ids
        self.fantasy_team_owner_ids = fantasy_team_owner_ids


def mint_default_fantasy_team_season_link(
    context: TestContext,
    overrides: FantasyTeamSeasonLinkCreateModel | None = None,
    request_operators: RequestOperators | None = None,
) -> FantasyTeamSeasonLinkCreateModel:
    overrides = overrides or FantasyTeamSeasonLinkCreateModel()

    default_obj = FantasyTeamSeasonLinkCreateModel()

    if overrides.fantasy_team_id is None:
        new_fantasy_team = create_fantasy_team(context, overrides.fantasy_team)
        default_obj.fantasy_team_id = new_fantasy_team.id

        del overrides.fantasy_team

    if overrides.season_id is None:
        new_season = create_season(context, overrides.season)
        default_obj.season_id = new_season.id

        del overrides.season

    copy_object_when_appropriate(default_obj, overrides)

    return default_obj


def create_fantasy_team_season_link(
    context: TestContext,
    overrides: FantasyTeamSeasonLinkCreateModel | None = None,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
) -> FantasyTeamSeasonLinkModel:
    post_object = mint_default_fantasy_team_season_link(
        context=context, overrides=overrides, request_operators=request_operators
    )

    result = qa_post(
        context.api_url + "/fantasy_team_season_links",
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
                "season",
                "fantasy_team",
                "fantasy_team_owner_id",
                "fantasy_team_owner",
                "fantasy_league_id",
                "fantasy_league",
                "created_at",
                "updated_at",
            ],
        )

        assert result_dict["id"] is not None
        assert result_dict["created_at"] is not None
        assert result_dict["updated_at"] is None

    return FantasyTeamSeasonLinkModel(**result.json())


def get_fantasy_team_season_link_by_id(
    context: TestContext,
    id: str,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
):
    url = f"{context.api_url}/fantasy_team_season_links/{id}"

    result = qa_get(url, request_operators=request_operators)

    return_object = FantasyTeamSeasonLinkModel(**result.json())

    return return_object


def get_fantasy_team_season_links(
    context: TestContext,
    search_model: FantasyTeamSeasonLinkSearchModel | None,
    request_operators: RequestOperators | None = None,
) -> PagedResponseItemList[FantasyTeamSeasonLinkModel]:
    url: str = f"{context.api_url}/fantasy_team_season_links"

    result: Response = qa_get(
        url=url,
        query_params=search_model if search_model is not None else {},
        request_operators=request_operators,
    )

    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict["paging"])

    return_items: list[FantasyTeamSeasonLinkModel] = [
        FantasyTeamSeasonLinkModel(**obj) for obj in result_dict["items"]
    ]

    return_object = PagedResponseItemList[FantasyTeamSeasonLinkModel](
        items=return_items, paging=return_paging_object
    )

    return return_object


def fantasy_team_season_link_hydration_check(
    fantasy_team_season_link: FantasyTeamSeasonLinkModel,
) -> None:
    assert fantasy_team_season_link.fantasy_team_owner is not None
    assert fantasy_team_season_link.fantasy_team_owner.id is not None
    assert (
        fantasy_team_season_link.fantasy_team_owner.id
        == fantasy_team_season_link.fantasy_team_owner_id
    )

    assert fantasy_team_season_link.fantasy_league is not None
    assert fantasy_team_season_link.fantasy_league.id is not None
    assert (
        fantasy_team_season_link.fantasy_league.id
        == fantasy_team_season_link.fantasy_league_id
    )

    assert fantasy_team_season_link.fantasy_team is not None
    assert fantasy_team_season_link.fantasy_team.id is not None
    assert (
        fantasy_team_season_link.fantasy_team.id
        == fantasy_team_season_link.fantasy_team_id
    )

    assert fantasy_team_season_link.season is not None
    assert fantasy_team_season_link.season.id is not None
    assert fantasy_team_season_link.season.id == fantasy_team_season_link.season_id
