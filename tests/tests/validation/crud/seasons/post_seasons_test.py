from typing import Any

from tests.qdk.operators.seasons import create_season
from tests.qdk.qa_requests import qa_post
from tests.qdk.types import TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import (
    get_global_configuration,
    populate_configuration_if_not_exists,
)


def test_posts_invalid_season_missing_fields() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/seasons", {})

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
        if "body" in error["loc"] and "season_number" in error["loc"]
    ]

    assert len(error) == 1
    assert error[0]["type"] == "missing"
    assert error[0]["msg"] == "Field required"


def test_posts_invalid_season_bad_inputs() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    result = qa_post(
        context.api_url + "/seasons",
        {"name": generate_random_string(256), "season_number": "not a number"},
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
        if "body" in error["loc"] and "season_number" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "int_parsing"
    assert (
        error[0]["msg"]
        == "Input should be a valid integer, unable to parse string as an integer"
    )


def test_posts_valid_season() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    create_season(context)
