from time import sleep
from typing import Any


from tests.qdk.operators.fantasy_teams import (
    FantasyTeamCreateModel,
    FantasyTeamModel,
    FantasyTeamSearchModel,
    fantasy_team_hydration_check,
)
from tests.qdk.operators.fantasy_teams import (
    create_fantasy_team,
    get_fantasy_team_by_id,
    get_fantasy_teams,
)
from tests.qdk.qa_requests import qa_get
from tests.qdk.types import PagedResponseItemList, RequestOperators, TestContext
from tests.qdk.utils import assert_objects_are_equal, generate_random_string
from util.configuration import (
    get_global_configuration,
    populate_configuration_if_not_exists,
)


def test_gets_fantasy_team_by_id() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object = create_fantasy_team(context)

    result = get_fantasy_team_by_id(context, posted_object.id)

    assert result is not None
    assert result.id == posted_object.id


def test_gets_fantasy_teams_invalid_inputs() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    result = qa_get(
        f"{context.api_url}/fantasy_teams",
        query_params={
            "ids": "not an id,also not an id",
            "owner_ids": "no id,no other id",
            "fantasy_league_ids": "still not id,and other id",
            "page": "not a page num",
            "page_length": "not a length num",
            "is_sort_descending": "not a bool",
        },
    )

    assert result.status_code == 422

    errors = result.json()

    assert len(errors["detail"]) == 6

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "query" in error["loc"] and "ids" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "invalid_id_list"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "query" in error["loc"] and "owner_ids" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "invalid_id_list"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "query" in error["loc"] and "fantasy_league_ids" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "invalid_id_list"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "query" in error["loc"] and "page" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "int_parsing"
    assert (
        error[0]["msg"]
        == "Input should be a valid integer, unable to parse string as an integer"
    )

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "query" in error["loc"] and "page_length" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "int_parsing"
    assert (
        error[0]["msg"]
        == "Input should be a valid integer, unable to parse string as an integer"
    )

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "query" in error["loc"] and "is_sort_descending" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "bool_parsing"
    assert (
        error[0]["msg"] == "Input should be a valid boolean, unable to interpret input"
    )


def test_gets_fantasy_teams_with_ids_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: FantasyTeamModel = create_fantasy_team(context)
    posted_object_2: FantasyTeamModel = create_fantasy_team(context)
    posted_object_3: FantasyTeamModel = create_fantasy_team(context)
    posted_object_4: FantasyTeamModel = create_fantasy_team(context)
    create_fantasy_team(context)

    filters: FantasyTeamSearchModel = FantasyTeamSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )

    result: PagedResponseItemList[FantasyTeamModel] = get_fantasy_teams(
        context, filters
    )

    assert result is not None
    assert result.items is not None

    assert result.paging is not None
    assert result.paging.page == 1
    assert result.paging.page_length == 25
    assert result.paging.sort_by == "created_at"
    assert result.paging.is_sort_descending == False

    assert len(result.items) == 4

    result_item_1: list[FantasyTeamModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(result_item_1) == 1
    assert_objects_are_equal(result_item_1[0], posted_object_1)

    result_item_2: list[FantasyTeamModel] = [
        item for item in result.items if item.id == posted_object_2.id
    ]
    assert len(result_item_2) == 1
    assert_objects_are_equal(result_item_2[0], posted_object_2)

    result_item_3: list[FantasyTeamModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(result_item_3) == 1
    assert_objects_are_equal(result_item_3[0], posted_object_3)

    result_item_4: list[FantasyTeamModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(result_item_4) == 1
    assert_objects_are_equal(result_item_4[0], posted_object_4)


def test_gets_league_players_with_ids_filter_with_hydration() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: FantasyTeamModel = create_fantasy_team(
        context, FantasyTeamCreateModel()
    )
    posted_object_2: FantasyTeamModel = create_fantasy_team(
        context, FantasyTeamCreateModel()
    )
    posted_object_3: FantasyTeamModel = create_fantasy_team(
        context, FantasyTeamCreateModel()
    )
    posted_object_4: FantasyTeamModel = create_fantasy_team(
        context, FantasyTeamCreateModel()
    )

    filters: FantasyTeamSearchModel = FantasyTeamSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )

    result: PagedResponseItemList[FantasyTeamModel] = get_fantasy_teams(
        context,
        filters,
        request_operators=RequestOperators(
            hydration_properties=["owner", "fantasy_league"]
        ),
    )

    assert result is not None
    assert result.items is not None

    assert result.paging is not None
    assert result.paging.page == 1
    assert result.paging.page_length == 25
    assert result.paging.sort_by == "created_at"
    assert result.paging.is_sort_descending == False

    assert len(result.items) == 4

    result_item_1: list[FantasyTeamModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(result_item_1) == 1
    assert_objects_are_equal(
        result_item_1[0], posted_object_1, ["owner", "fantasy_league"]
    )

    fantasy_team_hydration_check(result_item_1[0])

    result_item_2: list[FantasyTeamModel] = [
        item for item in result.items if item.id == posted_object_2.id
    ]
    assert len(result_item_2) == 1
    assert_objects_are_equal(
        result_item_2[0], posted_object_2, ["owner", "fantasy_league"]
    )

    fantasy_team_hydration_check(result_item_2[0])

    result_item_3: list[FantasyTeamModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(result_item_3) == 1
    assert_objects_are_equal(
        result_item_3[0], posted_object_3, ["owner", "fantasy_league"]
    )

    fantasy_team_hydration_check(result_item_3[0])

    result_item_4: list[FantasyTeamModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(result_item_4) == 1
    assert_objects_are_equal(
        result_item_4[0], posted_object_4, ["owner", "fantasy_league"]
    )

    fantasy_team_hydration_check(result_item_4[0])


def test_gets_fantasy_teams_with_paging() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: FantasyTeamModel = create_fantasy_team(context)
    posted_object_2: FantasyTeamModel = create_fantasy_team(context)

    sleep(1)

    posted_object_3: FantasyTeamModel = create_fantasy_team(context)
    posted_object_4: FantasyTeamModel = create_fantasy_team(context)

    filters_1: FantasyTeamSearchModel = FantasyTeamSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page=1,
        page_length=2,
    )

    filters_2: FantasyTeamSearchModel = FantasyTeamSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page=2,
        page_length=2,
    )

    result_page_1: PagedResponseItemList[FantasyTeamModel] = get_fantasy_teams(
        context, filters_1
    )
    result_page_2: PagedResponseItemList[FantasyTeamModel] = get_fantasy_teams(
        context, filters_2
    )

    ## Page 1

    assert result_page_1 is not None
    assert result_page_1.items is not None

    assert result_page_1.paging is not None
    assert result_page_1.paging.page == 1
    assert result_page_1.paging.page_length == 2
    assert result_page_1.paging.sort_by == "created_at"
    assert result_page_1.paging.is_sort_descending == False

    result_item_page_1_item_1: list[FantasyTeamModel] = [
        item for item in result_page_1.items if item.id == posted_object_1.id
    ]
    assert len(result_item_page_1_item_1) == 1
    assert_objects_are_equal(result_item_page_1_item_1[0], posted_object_1)

    result_item_page_1_item_2: list[FantasyTeamModel] = [
        item for item in result_page_1.items if item.id == posted_object_2.id
    ]
    assert len(result_item_page_1_item_2) == 1
    assert_objects_are_equal(result_item_page_1_item_2[0], posted_object_2)

    ## Page 2

    assert result_page_2 is not None
    assert result_page_2.items is not None

    assert result_page_2.paging is not None
    assert result_page_2.paging.page == 2
    assert result_page_2.paging.page_length == 2
    assert result_page_2.paging.sort_by == "created_at"
    assert result_page_2.paging.is_sort_descending == False

    assert len(result_page_1.items) == 2

    result_item_page_2_item_1: list[FantasyTeamModel] = [
        item for item in result_page_2.items if item.id == posted_object_3.id
    ]
    assert len(result_item_page_2_item_1) == 1
    assert_objects_are_equal(result_item_page_2_item_1[0], posted_object_3)

    result_item_page_2_item_2: list[FantasyTeamModel] = [
        item for item in result_page_2.items if item.id == posted_object_4.id
    ]
    assert len(result_item_page_2_item_2) == 1
    assert_objects_are_equal(result_item_page_2_item_2[0], posted_object_4)


def test_gets_fantasy_teams_with_name_exact_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    matching_random_string = generate_random_string(16)

    posted_object_1: FantasyTeamModel = create_fantasy_team(
        context,
        FantasyTeamCreateModel(name=f"prefix-{matching_random_string}-matches"),
    )
    posted_object_2: FantasyTeamModel = create_fantasy_team(
        context, FantasyTeamCreateModel(name=f"{matching_random_string}-matches")
    )
    posted_object_3: FantasyTeamModel = create_fantasy_team(
        context,
        FantasyTeamCreateModel(name=f"{matching_random_string}-matches-suffix"),
    )
    posted_object_4: FantasyTeamModel = create_fantasy_team(
        context,
        FantasyTeamCreateModel(name=f"prefix-{matching_random_string}-matches-suffix"),
    )

    filters: FantasyTeamSearchModel = FantasyTeamSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        name=f"{matching_random_string}-matches",
    )

    result: PagedResponseItemList[FantasyTeamModel] = get_fantasy_teams(
        context, filters
    )

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 1

    result_item_2: list[FantasyTeamModel] = [
        item for item in result.items if item.id == posted_object_2.id
    ]
    assert len(result_item_2) == 1
    assert_objects_are_equal(result_item_2[0], posted_object_2)


def test_gets_fantasy_teams_with_name_like_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    matching_random_string = generate_random_string(16).upper()
    non_matching_random_string = generate_random_string(16)

    posted_object_1: FantasyTeamModel = create_fantasy_team(
        context,
        FantasyTeamCreateModel(name=f"prefix-{matching_random_string}-suffix"),
    )
    posted_object_2: FantasyTeamModel = create_fantasy_team(
        context, FantasyTeamCreateModel(name=f"{matching_random_string}-suffix")
    )
    posted_object_3: FantasyTeamModel = create_fantasy_team(
        context,
        FantasyTeamCreateModel(name=f"not a match-{non_matching_random_string}"),
    )
    posted_object_4: FantasyTeamModel = create_fantasy_team(
        context, FantasyTeamCreateModel(name=f"prefix-{matching_random_string}")
    )

    filters: FantasyTeamSearchModel = FantasyTeamSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        name_like=f"{matching_random_string.lower()}",
    )

    result: PagedResponseItemList[FantasyTeamModel] = get_fantasy_teams(
        context, filters
    )

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 3

    result_item_1: list[FantasyTeamModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(result_item_1) == 1
    assert_objects_are_equal(result_item_1[0], posted_object_1)

    result_item_2: list[FantasyTeamModel] = [
        item for item in result.items if item.id == posted_object_2.id
    ]
    assert len(result_item_2) == 1
    assert_objects_are_equal(result_item_2[0], posted_object_2)

    result_item_4: list[FantasyTeamModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(result_item_4) == 1
    assert_objects_are_equal(result_item_4[0], posted_object_4)


def test_gets_fantasy_teams_with_fantasy_league_ids_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: FantasyTeamModel = create_fantasy_team(
        context, FantasyTeamCreateModel()
    )
    posted_object_2: FantasyTeamModel = create_fantasy_team(
        context, FantasyTeamCreateModel()
    )
    posted_object_3: FantasyTeamModel = create_fantasy_team(
        context,
        FantasyTeamCreateModel(fantasy_league_id=posted_object_1.fantasy_league_id),
    )
    posted_object_4: FantasyTeamModel = create_fantasy_team(
        context, FantasyTeamCreateModel()
    )

    filters: FantasyTeamSearchModel = FantasyTeamSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        fantasy_league_ids=f"{posted_object_1.fantasy_league_id},{posted_object_4.fantasy_league_id}",
    )

    result: PagedResponseItemList[FantasyTeamModel] = get_fantasy_teams(
        context, filters
    )

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 3

    result_item_1: list[FantasyTeamModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(result_item_1) == 1
    assert_objects_are_equal(result_item_1[0], posted_object_1)

    result_item_3: list[FantasyTeamModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(result_item_3) == 1
    assert_objects_are_equal(result_item_3[0], posted_object_3)

    result_item_4: list[FantasyTeamModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(result_item_4) == 1
    assert_objects_are_equal(result_item_4[0], posted_object_4)


def test_gets_fantasy_teams_with_owner_ids_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: FantasyTeamModel = create_fantasy_team(
        context, FantasyTeamCreateModel()
    )
    posted_object_2: FantasyTeamModel = create_fantasy_team(
        context, FantasyTeamCreateModel()
    )
    posted_object_3: FantasyTeamModel = create_fantasy_team(
        context,
        FantasyTeamCreateModel(owner_id=posted_object_1.owner_id),
    )
    posted_object_4: FantasyTeamModel = create_fantasy_team(
        context, FantasyTeamCreateModel()
    )

    filters: FantasyTeamSearchModel = FantasyTeamSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        owner_ids=f"{posted_object_1.owner_id},{posted_object_4.owner_id}",
    )

    result: PagedResponseItemList[FantasyTeamModel] = get_fantasy_teams(
        context, filters
    )

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 3

    result_item_1: list[FantasyTeamModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(result_item_1) == 1
    assert_objects_are_equal(result_item_1[0], posted_object_1)

    result_item_3: list[FantasyTeamModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(result_item_3) == 1
    assert_objects_are_equal(result_item_3[0], posted_object_3)

    result_item_4: list[FantasyTeamModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(result_item_4) == 1
    assert_objects_are_equal(result_item_4[0], posted_object_4)
