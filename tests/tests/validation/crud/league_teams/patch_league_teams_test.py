from typing import Any

from tests.qdk.operators.league_teams import (
    LeagueTeamCreateModel,
    LeagueTeamModel,
    LeagueTeamUpdateModel,
    create_league_team,
    league_team_hydration_check,
    update_league_team,
)
from tests.qdk.operators.venues import VenueModel, create_venue
from tests.qdk.qa_requests import qa_patch
from tests.qdk.types import RequestOperators, TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import (
    get_global_configuration,
    populate_configuration_if_not_exists,
)


def test_posts_invalid_league_team_bad_inputs() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object: LeagueTeamModel = create_league_team(context)

    result = qa_patch(
        f"{context.api_url}/league_teams/{posted_object.id}",
        {
            "name": generate_random_string(65),
            "home_venue_id": "patching not an id",
            "short_name": generate_random_string(4),
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
        if "body" in error["loc"] and "short_name" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "string_too_long"
    assert error[0]["msg"] == "String should have at most 3 characters"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "body" in error["loc"] and "home_venue_id" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "uuid_parsing"
    assert (
        error[0]["msg"]
        == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `p` at 1"
    )


def test_patches_valid_league_team() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    random_string = generate_random_string(14)
    random_short_name = generate_random_string(3)

    home_venue_to_switch_to: VenueModel = create_venue(context)

    posted_object: LeagueTeamModel = create_league_team(context)

    update_object: LeagueTeamUpdateModel = LeagueTeamUpdateModel(
        name=random_string + "_name",
        short_name=random_short_name,
        home_venue_id=home_venue_to_switch_to.id,
    )

    update_league_team(context, posted_object.id or "", update_object)


def test_patches_valid_league_team_with_hydration() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    random_string = generate_random_string(14)
    random_short_name = generate_random_string(3)

    home_venue_to_switch_to: VenueModel = create_venue(context)

    posted_object: LeagueTeamModel = create_league_team(context)

    update_object: LeagueTeamUpdateModel = LeagueTeamUpdateModel(
        name=random_string + "_name",
        short_name=random_short_name,
        home_venue_id=home_venue_to_switch_to.id,
    )

    result = update_league_team(
        context,
        posted_object.id or "",
        update_object,
        request_operators=RequestOperators(hydration_properties=["home_venue"]),
    )

    league_team_hydration_check(result)
