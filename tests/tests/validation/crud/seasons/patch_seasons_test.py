from typing import Any

from tests.qdk.operators.seasons import (
    SeasonModel,
    SeasonUpdateModel,
    create_season,
    update_season,
)
from tests.qdk.qa_requests import qa_patch
from tests.qdk.types import TestContext
from tests.qdk.utils import generate_random_string
from util.configuration import (
    get_global_configuration,
    populate_configuration_if_not_exists,
)


def test_posts_invalid_season_bad_inputs() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object: SeasonModel = create_season(context)

    result = qa_patch(
        f"{context.api_url}/seasons/{posted_object.id}",
        {
            "name": generate_random_string(256),
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
    assert error[0]["msg"] == "String should have at most 255 characters"


def test_patches_valid_season() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    random_string = generate_random_string(14)

    posted_object: SeasonModel = create_season(context)

    update_object: SeasonUpdateModel = SeasonUpdateModel(
        name=random_string + "_season_name",
    )

    update_season(context, posted_object.id or "", update_object)
