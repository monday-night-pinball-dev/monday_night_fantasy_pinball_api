from typing import Any

from tests.qdk.operators.league_players import (
    LeaguePlayerCreateModel,
    create_league_player,
    league_player_hydration_check,
)
from tests.qdk.qa_requests import qa_post
from tests.qdk.types import RequestOperators, TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import (
    get_global_configuration,
    populate_configuration_if_not_exists,
)


def test_posts_invalid_league_player_missing_fields() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/league_players", {})

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


def test_posts_invalid_league_player_bad_inputs() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    result = qa_post(
        context.api_url + "/league_players",
        {
            "name": generate_random_string(256),
            "league_team_id": "not an id",
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
        if "body" in error["loc"] and "league_team_id" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "uuid_parsing"
    assert (
        error[0]["msg"]
        == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `n` at 1"
    )


def test_posts_valid_league_player() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    create_league_player(context)


def test_posts_valid_league_player_with_hydration() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    created_league_player = create_league_player(
        context,
        LeaguePlayerCreateModel(
            create_league_team_if_null=True,
        ),
        request_operators=RequestOperators(hydration_properties=["league_team"]),
    )

    assert created_league_player.league_team is not None
    assert created_league_player.league_team.id is not None
    assert created_league_player.league_team.id == created_league_player.league_team_id

    league_player_hydration_check(created_league_player)
