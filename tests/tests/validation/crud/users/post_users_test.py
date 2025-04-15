from typing import Any

from tests.qdk.operators.users import (
    UserCreateModel,
    create_user,
    user_hydration_check,
)
from tests.qdk.qa_requests import qa_post
from tests.qdk.types import RequestOperators, TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import (
    get_global_configuration,
    populate_configuration_if_not_exists,
)


def test_posts_invalid_user_missing_fields() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/users", {})

    assert result.status_code == 422

    errors = result.json()

    assert len(errors["detail"]) == 2

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "body" in error["loc"] and "name" in error["loc"]
    ]

    assert len(error) == 1
    assert error[0]["type"] == "missing"
    assert error[0]["msg"] == "Field required"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "body" in error["loc"] and "username" in error["loc"]
    ]

    assert len(error) == 1
    assert error[0]["type"] == "missing"
    assert error[0]["msg"] == "Field required"


def test_posts_invalid_user_bad_inputs() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    result = qa_post(
        context.api_url + "/users",
        {
            "name": generate_random_string(256),
            "league_player_id": "not an id",
            "username": "not an email",
        },
    )

    assert result.status_code == 422

    errors = result.json()

    assert len(errors["detail"]) == 3

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
        if "body" in error["loc"] and "league_player_id" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "uuid_parsing"
    assert (
        error[0]["msg"]
        == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `n` at 1"
    )

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "body" in error["loc"] and "username" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "value_error"
    assert (
        error[0]["msg"]
        == "value is not a valid email address: An email address must have an @-sign."
    )


def test_posts_valid_user() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    create_user(context)


def test_posts_valid_user_with_hydration() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    created_user = create_user(
        context,
        UserCreateModel(
            create_league_player_if_null=True,
        ),
        request_operators=RequestOperators(hydration_properties=["league_player"]),
    )

    assert created_user.league_player is not None
    assert created_user.league_player.id is not None
    assert created_user.league_player.id == created_user.league_player_id

    user_hydration_check(created_user)
