from typing import Any

from tests.qdk.operators.users import (
    UserCreateModel,
    UserModel,
    UserUpdateModel,
    create_user,
    user_hydration_check,
    update_user,
)
from tests.qdk.operators.league_players import LeagueTeamModel, create_league_player
from tests.qdk.operators.venues import VenueModel, create_venue
from tests.qdk.qa_requests import qa_patch
from tests.qdk.types import RequestOperators, TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import (
    get_global_configuration,
    populate_configuration_if_not_exists,
)


def test_posts_invalid_user_bad_inputs() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object: UserModel = create_user(context)

    result = qa_patch(
        f"{context.api_url}/users/{posted_object.id}",
        {
            "name": generate_random_string(256),
            "role": "not a role",
        },
    )

    assert result.status_code == 422

    errors = result.json()

    assert len(errors["detail"]) == 2

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "body" in error["loc"] and "name" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "string_too_long"
    assert error[0]["msg"] == "String should have at most 255 characters"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "body" in error["loc"] and "role" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "enum"
    assert (
        error[0]["msg"]
        == "Input should be 'MnfpAdmin', 'FantasyCommissioner', 'TeamOwner' or 'LeaguePlayer'"
    )


def test_patches_valid_user() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    random_string = generate_random_string(14)

    posted_object: UserModel = create_user(context)

    update_object: UserUpdateModel = UserUpdateModel(
        name=random_string + "_name", role="FantasyCommissioner"
    )

    update_user(context, posted_object.id or "", update_object)


def test_patches_valid_user_with_hydration() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    random_string = generate_random_string(14)

    posted_object: UserModel = create_user(
        context, UserCreateModel(create_league_player_if_null=True)
    )

    update_object: UserUpdateModel = UserUpdateModel(
        name=random_string + "_name",
        role="FantasyCommissioner",
    )

    result = update_user(
        context,
        posted_object.id or "",
        update_object,
        request_operators=RequestOperators(hydration_properties=["league_player"]),
    )

    user_hydration_check(result)
