import datetime
import string

from requests import Response
from tests.qdk.operators.league_teams import (
    LeagueTeamCreateModel,
    LeagueTeamModel,
    create_league_team,
)
from tests.qdk.operators.venues import (
    VenueCreateModel,
    VenueModel,
    create_venue,
)
from tests.qdk.qa_requests import qa_get, qa_patch, qa_post
from tests.qdk.types import (
    PagedResponseItemList,
    PagingRequestModel,
    PagingResponseModel,
    RequestOperators,
    TestContext,
)
from tests.qdk.utils import (
    assert_object_was_updated,
    assert_objects_are_equal,
    copy_object_when_appropriate,
    generate_random_string,
)


class LeaguePlayerCreateModel:
    def __init__(
        self,
        league_team_id: str | None = None,
        league_team: LeagueTeamCreateModel | None = None,
        create_league_team_if_null: bool | None = False,
        name: str | None = None,
    ) -> None:
        self.league_team_id = league_team_id
        self.league_team = league_team
        self.name = name
        self.create_league_team_if_null = create_league_team_if_null


class LeaguePlayerModel:
    def __init__(
        self,
        id: str,
        name: str,
        created_at: datetime.datetime,
        league_team_id: str | None = None,
        league_team: LeagueTeamModel | None = None,
        updated_at: datetime.datetime | None = None,
    ) -> None:
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.league_team_id = league_team_id
        self.league_team = (
            LeagueTeamModel(**league_team) if league_team is not None else None
        )

        self.name = name


class LeaguePlayerSearchModel(PagingRequestModel):
    def __init__(
        self,
        ids: str | None = None,
        league_team_ids: str | None = None,
        name: str | None = None,
        name_like: str | None = None,
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
        self.league_team_ids = league_team_ids
        self.name = name
        self.name_like = name_like


class LeaguePlayerUpdateModel:
    def __init__(
        self,
        league_team_id: str | None = None,
        name: str | None = None,
    ) -> None:
        self.league_team_id = league_team_id
        self.name = name


def mint_default_league_player(
    context: TestContext,
    overrides: LeaguePlayerCreateModel | None = None,
    request_operators: RequestOperators | None = None,
) -> LeaguePlayerCreateModel:
    overrides = overrides or LeaguePlayerCreateModel()

    random_string = generate_random_string()

    default_league_player: LeaguePlayerCreateModel = LeaguePlayerCreateModel(
        name=random_string + "_name"
    )

    if overrides.league_team_id is None and overrides.create_league_team_if_null:
        new_team_league = create_league_team(context, overrides.league_team)
        overrides.league_team_id = new_team_league.id

        del overrides.league_team
        del overrides.create_league_team_if_null

    copy_object_when_appropriate(default_league_player, overrides)

    return default_league_player


def create_league_player(
    context: TestContext,
    overrides: LeaguePlayerCreateModel | None = None,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
):
    post_object = mint_default_league_player(
        context=context, overrides=overrides, request_operators=request_operators
    )

    result = qa_post(
        context.api_url + "/league_players", post_object, request_operators
    )

    if allow_failures == False:
        assert result.status_code == 201

        result_dict = result.json()

        assert_objects_are_equal(
            result_dict,
            post_object.__dict__,
            ["id", "league_team_id", "league_team", "created_at", "updated_at"],
        )

        assert result_dict["id"] is not None
        assert result_dict["created_at"] is not None
        assert result_dict["updated_at"] is None

    return_object = LeaguePlayerModel(**result.json())

    return return_object


def get_league_player_by_id(
    context: TestContext,
    id: str,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
):
    url = f"{context.api_url}/league_players/{id}"

    result = qa_get(url, request_operators=request_operators)

    return_object = LeaguePlayerModel(**result.json())

    return return_object


def get_league_players(
    context: TestContext,
    search_model: LeaguePlayerSearchModel | None,
    request_operators: RequestOperators | None = None,
) -> PagedResponseItemList[LeaguePlayerModel]:
    url: str = f"{context.api_url}/league_players"

    result: Response = qa_get(
        url=url,
        query_params=search_model if search_model is not None else {},
        request_operators=request_operators,
    )

    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict["paging"])

    return_items: list[LeaguePlayerModel] = [
        LeaguePlayerModel(**obj) for obj in result_dict["items"]
    ]

    return_object = PagedResponseItemList[LeaguePlayerModel](
        items=return_items, paging=return_paging_object
    )

    return return_object


def update_league_player(
    context: TestContext,
    id: str,
    update_model: LeaguePlayerUpdateModel | None = None,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
):
    original_object: LeaguePlayerModel = get_league_player_by_id(
        context, id, request_operators
    )

    result = qa_patch(
        f"{context.api_url}/league_players/{id}", update_model, request_operators
    )

    if allow_failures == False:
        assert result.status_code == 200

        result_dict = result.json()

        assert_object_was_updated(
            original_object.__dict__,
            update_model.__dict__,
            result_dict,
            ["league_team", "updated_at"],
        )

        assert result_dict["updated_at"] is not None

    return_object = LeaguePlayerModel(**result.json())

    return return_object


def league_player_hydration_check(league_player: LeaguePlayerModel) -> None:
    assert league_player.league_team is not None
    assert league_player.league_team.id is not None
    assert league_player.league_team.id == league_player.league_team_id
