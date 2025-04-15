from typing import Any


from tests.qdk.operators.fanatasy_leagues import (
    FantasyLeagueModel,
    FantasyLeagueUpdateModel,
    create_fantasy_league,
    update_fantasy_league,
)
from tests.qdk.operators.venues import VenueModel, create_venue
from tests.qdk.qa_requests import qa_patch
from tests.qdk.types import RequestOperators, TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import (
    get_global_configuration,
    populate_configuration_if_not_exists,
)


def test_posts_invalid_fantasy_league_bad_inputs() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object: FantasyLeagueModel = create_fantasy_league(context)

    result = qa_patch(
        f"{context.api_url}/fantasy_leagues/{posted_object.id}",
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


def test_patches_valid_fantasy_league() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    random_string = generate_random_string(14)

    posted_object: FantasyLeagueModel = create_fantasy_league(context)

    update_object: FantasyLeagueUpdateModel = FantasyLeagueUpdateModel(
        name=random_string + "_name",
    )

    update_fantasy_league(context, posted_object.id or "", update_object)
