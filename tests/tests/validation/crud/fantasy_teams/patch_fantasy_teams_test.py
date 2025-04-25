from typing import Any


from tests.qdk.operators.fantasy_teams import (
    FantasyTeamModel,
    FantasyTeamUpdateModel,
    create_fantasy_team,
    update_fantasy_team,
)
from tests.qdk.operators.users import create_user
from tests.qdk.qa_requests import qa_patch
from tests.qdk.types import TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import (
    get_global_configuration,
    populate_configuration_if_not_exists,
)


def test_posts_invalid_fantasy_team_bad_inputs() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object: FantasyTeamModel = create_fantasy_team(context)

    result = qa_patch(
        f"{context.api_url}/fantasy_teams/{posted_object.id}",
        {
            "name": generate_random_string(65),
            "owner_id": "not an id",
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
    assert error[0]["msg"] == "String should have at most 64 characters"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "body" in error["loc"] and "owner_id" in error["loc"]
    ]


def test_patches_valid_fantasy_team() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    random_string = generate_random_string(14)

    posted_object: FantasyTeamModel = create_fantasy_team(context)

    owner_to_patch_to = create_user(context)

    update_object: FantasyTeamUpdateModel = FantasyTeamUpdateModel(
        name=random_string + "_name",
        owner_id=owner_to_patch_to.id,
    )

    update_fantasy_team(context, posted_object.id, update_object)
