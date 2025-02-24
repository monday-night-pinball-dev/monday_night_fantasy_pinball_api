import datetime
import string

from requests import Response
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


class LeagueTeamCreateModel:
    def __init__(
        self,
        home_venue_id: str | None = None,
        home_venue: VenueCreateModel | None = None,
        name: str | None = None,
        short_name: str | None = None,
    ) -> None:
        self.home_venue_id = home_venue_id
        self.home_venue = home_venue
        self.name = name
        self.short_name = short_name


class LeagueTeamModel:
    def __init__(
        self,
        id: str,
        home_venue_id: str,
        name: str,
        short_name: str,
        created_at: datetime.datetime,
        home_venue: VenueModel | None = None,
        updated_at: datetime.datetime | None = None,
    ) -> None:
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.home_venue_id = home_venue_id
        self.home_venue = VenueModel(**home_venue) if home_venue is not None else None

        self.name = name
        self.short_name = short_name


class LeagueTeamSearchModel(PagingRequestModel):
    def __init__(
        self,
        ids: str | None = None,
        home_venue_ids: str | None = None,
        name: str | None = None,
        name_like: str | None = None,
        short_name: str | None = None,
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
        self.home_venue_ids = home_venue_ids
        self.name = name
        self.name_like = name_like
        self.short_name = short_name


class LeagueTeamUpdateModel:
    def __init__(
        self,
        home_venue_id: str | None = None,
        name: str | None = None,
        short_name: str | None = None,
    ) -> None:
        self.home_venue_id = home_venue_id
        self.name = name
        self.short_name = short_name


def mint_default_league_team(
    context: TestContext,
    overrides: LeagueTeamCreateModel | None = None,
    request_operators: RequestOperators | None = None,
) -> LeagueTeamCreateModel:
    overrides = overrides or LeagueTeamCreateModel()

    random_string = generate_random_string()
    random_short_name = generate_random_string(len=3, charset=string.ascii_uppercase)

    default_league_team: LeagueTeamCreateModel = LeagueTeamCreateModel(
        name=random_string + "_league_team_name",
        short_name=random_short_name,
    )

    if overrides.home_venue_id is None:
        new_home_venue = create_venue(context, overrides.home_venue)
        overrides.home_venue_id = new_home_venue.id

        del overrides.home_venue

    copy_object_when_appropriate(default_league_team, overrides)

    return default_league_team


def create_league_team(
    context: TestContext,
    overrides: LeagueTeamCreateModel | None = None,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
):
    post_object = mint_default_league_team(
        context=context, overrides=overrides, request_operators=request_operators
    )

    result = qa_post(context.api_url + "/league_teams", post_object, request_operators)

    if allow_failures == False:
        assert result.status_code == 201

        result_dict = result.json()

        assert_objects_are_equal(
            result_dict,
            post_object.__dict__,
            ["id", "home_venue", "created_at", "updated_at"],
        )

        assert result_dict["id"] is not None
        assert result_dict["created_at"] is not None
        assert result_dict["updated_at"] is None

    return_object = LeagueTeamModel(**result.json())

    return return_object


def get_league_team_by_id(
    context: TestContext,
    id: str,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
):
    url = f"{context.api_url}/league_teams/{id}"

    result = qa_get(url, request_operators=request_operators)

    return_object = LeagueTeamModel(**result.json())

    return return_object


def get_league_teams(
    context: TestContext,
    search_model: LeagueTeamSearchModel | None,
    request_operators: RequestOperators | None = None,
) -> PagedResponseItemList[LeagueTeamModel]:
    url: str = f"{context.api_url}/league_teams"

    result: Response = qa_get(
        url=url,
        query_params=search_model if search_model is not None else {},
        request_operators=request_operators,
    )

    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict["paging"])

    return_items: list[LeagueTeamModel] = [
        LeagueTeamModel(**obj) for obj in result_dict["items"]
    ]

    return_object = PagedResponseItemList[LeagueTeamModel](
        items=return_items, paging=return_paging_object
    )

    return return_object


def update_league_team(
    context: TestContext,
    id: str,
    update_model: LeagueTeamUpdateModel | None = None,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
):
    original_object: LeagueTeamModel = get_league_team_by_id(
        context, id, request_operators
    )

    result = qa_patch(
        f"{context.api_url}/league_teams/{id}", update_model, request_operators
    )

    if allow_failures == False:
        assert result.status_code == 200

        result_dict = result.json()

        assert_object_was_updated(
            original_object.__dict__,
            update_model.__dict__,
            result_dict,
            ["home_venue", "updated_at"],
        )

        assert result_dict["updated_at"] is not None

    return_object = LeagueTeamModel(**result.json())

    return return_object


def league_team_hydration_check(league_team: LeagueTeamModel) -> None:
    assert league_team.home_venue is not None
    assert league_team.home_venue.id is not None
    assert league_team.home_venue.id == league_team.home_venue_id
