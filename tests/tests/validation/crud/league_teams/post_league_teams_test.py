from typing import Any

from tests.qdk.operators.league_teams import (
    LeagueTeamCreateModel,
    create_league_team,
    league_team_hydration_check,
)
from tests.qdk.qa_requests import qa_post
from tests.qdk.types import RequestOperators, TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import (
    get_global_configuration,
    populate_configuration_if_not_exists,
)


def test_posts_invalid_league_team_missing_fields() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/league_teams", {})

    assert result.status_code == 422

    errors = result.json()

    assert len(errors["detail"]) == 4

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
        if "body" in error["loc"] and "short_name" in error["loc"]
    ]

    assert len(error) == 1
    assert error[0]["type"] == "missing"
    assert error[0]["msg"] == "Field required"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "body" in error["loc"] and "home_venue_id" in error["loc"]
    ]

    assert len(error) == 1
    assert error[0]["type"] == "missing"
    assert error[0]["msg"] == "Field required"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "body" in error["loc"] and "global_mnp_id" in error["loc"]
    ]

    assert len(error) == 1
    assert error[0]["type"] == "missing"
    assert error[0]["msg"] == "Field required"


def test_posts_invalid_league_team_bad_inputs() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    result = qa_post(
        context.api_url + "/league_teams",
        {
            "name": generate_random_string(65),
            "short_name": generate_random_string(4),
            "home_venue_id": "not an id",
            "global_mnp_id": "also not an id",
        },
    )

    assert result.status_code == 422

    errors = result.json()

    assert len(errors["detail"]) == 4

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "body" in error["loc"] and "name" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "string_too_long"
    assert error[0]["msg"] == "String should have at most 64 characters"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "body" in error["loc"] and "home_venue_id" in error["loc"]
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
        if "body" in error["loc"] and "short_name" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "string_too_long"
    assert error[0]["msg"] == "String should have at most 3 characters"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "body" in error["loc"] and "global_mnp_id" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "uuid_parsing"
    assert (
        error[0]["msg"]
        == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `l` at 2"
    )


def test_posts_valid_league_team() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    create_league_team(context)


def test_posts_valid_league_team_with_hydration() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    created_league_team = create_league_team(
        context,
        None,
        request_operators=RequestOperators(hydration_properties=["home_venue"]),
    )

    assert created_league_team.home_venue is not None
    assert created_league_team.home_venue.id is not None
    assert created_league_team.home_venue.id == created_league_team.home_venue_id

    league_team_hydration_check(created_league_team)
