from typing import Any

from tests.qdk.operators.fanatasy_leagues import create_fantasy_league
from tests.qdk.qa_requests import qa_post
from tests.qdk.types import TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import (
    get_global_configuration,
    populate_configuration_if_not_exists,
)


def test_posts_invalid_fantasy_league_missing_fields() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/fantasy_leagues", {})

    assert result.status_code == 422

    errors = result.json()

    assert len(errors["detail"]) == 1

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "body" in error["loc"] and "name" in error["loc"]
    ]

    assert len(error) == 1
    assert error[0]["type"] == "missing"
    assert error[0]["msg"] == "Field required"


def test_posts_invalid_fantasy_league_bad_inputs() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    result = qa_post(
        context.api_url + "/fantasy_leagues",
        {
            "name": generate_random_string(65),
        },
    )

    assert result.status_code == 422

    errors = result.json()

    assert len(errors["detail"]) == 1

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "body" in error["loc"] and "name" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "string_too_long"
    assert error[0]["msg"] == "String should have at most 64 characters"


def test_posts_valid_fantasy_league() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    create_fantasy_league(context)
