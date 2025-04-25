from typing import Any

from tests.qdk.operators.fantasy_team_season_links import (
    FantasyTeamCreateModel,
    create_fantasy_team_season_link,
    fantasy_team_season_link_hydration_check,
)
from tests.qdk.operators.league_players import LeaguePlayerCreateModel
from tests.qdk.qa_requests import qa_post
from tests.qdk.types import RequestOperators, TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import (
    get_global_configuration,
    populate_configuration_if_not_exists,
)


def test_posts_invalid_fantasy_team_season_link_missing_fields() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    result = qa_post(context.api_url + "/fantasy_team_season_links", {})

    assert result.status_code == 422

    errors = result.json()

    assert len(errors["detail"]) == 2

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "body" in error["loc"] and "season_id" in error["loc"]
    ]

    assert len(error) == 1
    assert error[0]["type"] == "missing"
    assert error[0]["msg"] == "Field required"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "body" in error["loc"] and "fantasy_team_id" in error["loc"]
    ]

    assert len(error) == 1
    assert error[0]["type"] == "missing"
    assert error[0]["msg"] == "Field required"


def test_posts_invalid_fantasy_team_season_link_bad_inputs() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    result = qa_post(
        context.api_url + "/fantasy_team_season_links",
        {
            "season_id": "not an id",
            "fantasy_team_id": "not an id either",
        },
    )

    assert result.status_code == 422

    errors = result.json()

    assert len(errors["detail"]) == 2

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "body" in error["loc"] and "season_id" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "uuid_parsing"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "body" in error["loc"] and "fantasy_team_id" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "uuid_parsing"


def test_posts_valid_fantasy_team_season_link() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    create_fantasy_team_season_link(context)


def test_posts_valid_fantasy_team_season_link_with_hydration() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    created_fantasy_team_season_link = create_fantasy_team_season_link(
        context,
        {},
        request_operators=RequestOperators(
            hydration_properties=[
                "season",
                "fantasy_team",
                "fantasy_league",
                "fantasy_team_owner",
            ],
        ),
    )

    fantasy_team_season_link_hydration_check(created_fantasy_team_season_link)
