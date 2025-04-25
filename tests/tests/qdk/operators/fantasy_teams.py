from requests import Response
from tests.qdk.operators.fantasy_leagues import (
    FantasyLeagueCreateModel,
    FantasyLeagueModel,
    create_fantasy_league,
)
from tests.qdk.operators.users import UserCreateModel, UserModel, create_user
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


class FantasyTeamCreateModel:
    def __init__(
        self,
        name: str | None = None,
        fantasy_league_id: str | None = None,
        fantasy_league: FantasyLeagueCreateModel | None = None,
        owner_id: str | None = None,
        owner: UserCreateModel | None = None,
    ) -> None:
        self.name = name
        self.fantasy_league_id = fantasy_league_id
        self.fantasy_league = fantasy_league
        self.owner_id = owner_id
        self.owner = owner


class FantasyTeamModel:
    def __init__(
        self,
        id: str,
        owner_id: str,
        owner: UserModel | None,
        fantasy_league_id: str,
        fantasy_league: FantasyLeagueModel | None,
        name: str,
        created_at: str,
        updated_at: str | None = None,
    ) -> None:
        self.id = id
        self.name = name
        self.fantasy_league_id = fantasy_league_id
        self.fantasy_league = (
            FantasyLeagueModel(**fantasy_league) if fantasy_league else None
        )
        self.owner_id = owner_id
        self.owner = UserModel(**owner) if owner else None
        self.created_at = created_at
        self.updated_at = updated_at


class FantasyTeamSearchModel(PagingRequestModel):
    def __init__(
        self,
        ids: str | None = None,
        owner_ids: str | None = None,
        fantasy_league_ids: str | None = None,
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
        self.owner_ids = owner_ids
        self.fantasy_league_ids = fantasy_league_ids
        self.name = name
        self.name_like = name_like


class FantasyTeamUpdateModel:
    def __init__(
        self,
        name: str | None = None,
        owner_id: str | None = None,
    ) -> None:
        self.name = name
        self.owner_id = owner_id


def mint_default_fantasy_team(
    context: TestContext,
    overrides: FantasyTeamCreateModel | None = None,
    request_operators: RequestOperators | None = None,
) -> FantasyTeamCreateModel:
    overrides = overrides or FantasyTeamCreateModel()

    random_name = generate_random_string()

    default_team = FantasyTeamCreateModel(
        name=random_name + "_fantasy_team",
    )

    copy_object_when_appropriate(default_team, overrides)

    if overrides.owner_id is None:
        new_owner = create_user(context, overrides.owner)
        default_team.owner_id = new_owner.id

        del overrides.owner

    if overrides.fantasy_league_id is None:
        new_fantasy_league = create_fantasy_league(context, overrides.fantasy_league)
        default_team.fantasy_league_id = new_fantasy_league.id

        del overrides.fantasy_league

    return default_team


def create_fantasy_team(
    context: TestContext,
    overrides: FantasyTeamCreateModel | None = None,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
) -> FantasyTeamModel:
    post_object = mint_default_fantasy_team(
        context=context, overrides=overrides, request_operators=request_operators
    )

    result = qa_post(
        context.api_url + "/fantasy_teams",
        post_object,
        request_operators,
    )

    if not allow_failures:
        assert result.status_code == 201

        result_dict = result.json()

        assert_objects_are_equal(
            result_dict,
            post_object.__dict__,
            ["id", "owner", "fantasy_league", "created_at", "updated_at"],
        )

        assert result_dict["id"] is not None
        assert result_dict["created_at"] is not None
        assert result_dict["updated_at"] is None

    return FantasyTeamModel(**result.json())


def get_fantasy_team_by_id(
    context: TestContext,
    id: str,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
):
    url = f"{context.api_url}/fantasy_teams/{id}"

    result = qa_get(url, request_operators=request_operators)

    return_object = FantasyTeamModel(**result.json())

    return return_object


def get_fantasy_teams(
    context: TestContext,
    search_model: FantasyTeamSearchModel | None,
    request_operators: RequestOperators | None = None,
) -> PagedResponseItemList[FantasyTeamModel]:
    url: str = f"{context.api_url}/fantasy_teams"

    result: Response = qa_get(
        url=url,
        query_params=search_model if search_model is not None else {},
        request_operators=request_operators,
    )

    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict["paging"])

    return_items: list[FantasyTeamModel] = [
        FantasyTeamModel(**obj) for obj in result_dict["items"]
    ]

    return_object = PagedResponseItemList[FantasyTeamModel](
        items=return_items, paging=return_paging_object
    )

    return return_object


def update_fantasy_team(
    context: TestContext,
    id: str,
    update_model: FantasyTeamUpdateModel | None = None,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
):
    original_object: FantasyTeamModel = get_fantasy_team_by_id(
        context, id, request_operators
    )

    result = qa_patch(
        f"{context.api_url}/fantasy_teams/{id}", update_model, request_operators
    )

    if allow_failures == False:
        assert result.status_code == 200

        result_dict = result.json()

        assert_object_was_updated(
            original_object.__dict__,
            update_model.__dict__,
            result_dict,
            ["owner", "fantasy_league", "updated_at"],
        )

        assert result_dict["updated_at"] is not None

    return_object = FantasyTeamModel(**result.json())

    return return_object


def fantasy_team_hydration_check(fantasy_team: FantasyTeamModel) -> None:
    assert fantasy_team.owner is not None
    assert fantasy_team.owner.id is not None
    assert fantasy_team.owner.id == fantasy_team.owner_id
    assert fantasy_team.fantasy_league is not None
    assert fantasy_team.fantasy_league.id is not None
    assert fantasy_team.fantasy_league.id == fantasy_team.fantasy_league_id
