from typing import Any

from tests.qdk.operators.fantasy_teams import (
    FantasyTeamCreateModel,
    create_fantasy_team,
    fantasy_team_hydration_check,
)
from tests.qdk.operators.league_players import LeaguePlayerCreateModel
from tests.qdk.qa_requests import qa_post
from tests.qdk.types import RequestOperators, TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import (
    get_global_configuration,
    populate_configuration_if_not_exists,
)


def test_posts_invalid_fantasy_team_missing_fields() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/fantasy_teams", {})

    assert result.status_code == 422

    errors = result.json()

    assert len(errors["detail"]) == 3

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
        if "body" in error["loc"] and "owner_id" in error["loc"]
    ]

    assert len(error) == 1
    assert error[0]["type"] == "missing"
    assert error[0]["msg"] == "Field required"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "body" in error["loc"] and "fantasy_league_id" in error["loc"]
    ]

    assert len(error) == 1
    assert error[0]["type"] == "missing"
    assert error[0]["msg"] == "Field required"


def test_posts_invalid_fantasy_team_bad_inputs() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    result = qa_post(
        context.api_url + "/fantasy_teams",
        {
            "name": generate_random_string(65),
            "fantasy_league_id": "not an id",
            "owner_id": "not an id either",
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
    assert error[0]["msg"] == "String should have at most 64 characters"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "body" in error["loc"] and "owner_id" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "uuid_parsing"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "body" in error["loc"] and "fantasy_league_id" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "uuid_parsing"


def test_posts_valid_fantasy_team() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    create_fantasy_team(context)


def test_posts_valid_fantasy_team_with_hydration() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    created_fantasy_team = create_fantasy_team(
        context,
        {},
        request_operators=RequestOperators(
            hydration_properties=["owner", "fantasy_league"]
        ),
    )

    fantasy_team_hydration_check(created_fantasy_team)
