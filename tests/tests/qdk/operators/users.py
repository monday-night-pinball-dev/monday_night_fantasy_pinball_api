import datetime
from typing import Any, Self

from requests import Response
from tests.qdk.operators.league_players import (
    LeaguePlayerCreateModel,
    LeaguePlayerModel,
    create_league_player,
)
from tests.qdk.qa_requests import qa_get, qa_patch, qa_post
from tests.qdk.types import (
    PagedResponseItemList,
    PagingResponseModel,
    PagingRequestModel,
    RequestOperators,
    TestContext,
)
from tests.qdk.utils import (
    assert_object_was_updated,
    assert_objects_are_equal,
    copy_object_when_appropriate,
    generate_random_string,
)


class UserCreateModel:
    def __init__(
        self,
        league_player_id: str | None = None,
        league_player: LeaguePlayerCreateModel | None = None,
        create_league_player_if_null: bool | None = False,
        name: str | None = None,
        username: str | None = None,
        role: str | None = None,
    ) -> None:
        self.league_player_id = league_player_id
        self.league_player = league_player
        self.create_league_player_if_null = create_league_player_if_null
        self.name = name
        self.username = username
        self.role = role


class UserUpdateModel:
    def __init__(
        self,
        name: str | None = None,
        role: str | None = None,
    ) -> None:
        self.first_name = name
        self.role = role


class UserModel:
    def __init__(
        self,
        id: str,
        name: str,
        username: str,
        role: str,
        created_at: datetime.datetime,
        league_player_id: str | None = None,
        league_player: LeaguePlayerModel | None = None,
        updated_at: datetime.datetime | None = None,
    ) -> None:
        self.id = id
        self.name = name
        self.username = username
        self.role = role
        self.league_player_id = league_player_id
        self.league_player = (
            LeaguePlayerModel(**league_player) if league_player is not None else None
        )

        self.created_at = created_at
        self.updated_at = updated_at


class UserSearchModel(PagingRequestModel):
    def __init__(
        self,
        ids: str | None = None,
        league_player_ids: str | None = None,
        name_like: str | None = None,
        name: str | None = None,
        username_like: str | None = None,
        username: str | None = None,
        role: str | None = None,
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
        self.name = name
        self.league_player_ids = league_player_ids
        self.role = role
        self.name_like = name_like
        self.username_like = username_like
        self.username = username


def mint_default_user(
    context: TestContext,
    overrides: UserCreateModel | None = None,
    request_operators: RequestOperators | None = None,
) -> UserCreateModel:
    random_string = generate_random_string()

    overrides = overrides or UserCreateModel()

    default_user: UserCreateModel = UserCreateModel(
        name=random_string + "_name",
        username=random_string + "_username@example.com",
        role="MnfpAdmin",
    )

    if overrides.league_player_id is None and overrides.create_league_player_if_null:
        new_league_player = create_league_player(
            context, overrides.league_player, request_operators=request_operators
        )
        overrides.league_player_id = new_league_player.id

        del overrides.league_player
        del overrides.create_league_player_if_null

    copy_object_when_appropriate(default_user, overrides)

    return default_user


def create_user(
    context: TestContext,
    overrides: UserCreateModel | None = None,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
) -> UserModel:
    post_object: UserCreateModel = mint_default_user(
        context=context, overrides=overrides, request_operators=request_operators
    )

    result: Response = qa_post(
        context.api_url + "/users", post_object, request_operators
    )

    if allow_failures == False:
        assert result.status_code == 201

        result_dict = result.json()

        assert_objects_are_equal(
            result_dict,
            post_object.__dict__,
            [
                "id",
                "created_at",
                "updated_at",
                "username",
                "league_player_id",
                "league_player",
            ],
        )

        assert result_dict["id"] is not None
        assert result_dict["created_at"] is not None
        assert result_dict["updated_at"] is None

        assert result_dict["username"].lower() == post_object.username.lower()

    return_object = UserModel(**result.json())

    return return_object


def get_user_by_id(
    context: TestContext,
    id: str,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
) -> UserModel:
    url: str = f"{context.api_url}/users/{id}"

    result: Response = qa_get(url, request_operators=request_operators)

    return_object = UserModel(**result.json())

    return return_object


def get_users(
    context: TestContext,
    search_model: UserSearchModel | None,
    request_operators: RequestOperators | None = None,
) -> PagedResponseItemList[UserModel]:
    url: str = f"{context.api_url}/users"

    result: Response = qa_get(
        url=url,
        query_params=search_model if search_model is not None else {},
        request_operators=request_operators,
    )

    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict["paging"])

    return_items: list[UserModel] = [UserModel(**obj) for obj in result_dict["items"]]

    return_object = PagedResponseItemList[UserModel](
        items=return_items, paging=return_paging_object
    )

    return return_object


def update_user(
    context: TestContext,
    id: str,
    update_model: UserUpdateModel | None = None,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
) -> UserModel:
    original_object: UserModel = get_user_by_id(context, id, request_operators)

    result: Response = qa_patch(
        f"{context.api_url}/users/{id}", update_model, request_operators
    )

    if allow_failures == False:
        assert result.status_code == 200

        result_dict = result.json()

        assert_object_was_updated(
            original_object.__dict__,
            update_model.__dict__,
            result_dict,
            ["league_player", "updated_at"],
        )

        assert result_dict["updated_at"] is not None

    return_object = UserModel(**result.json())

    return return_object


def user_hydration_check(user: UserModel) -> None:
    assert user.league_player is not None
    assert user.league_player.id is not None
    assert user.league_player.id == user.league_player_id
