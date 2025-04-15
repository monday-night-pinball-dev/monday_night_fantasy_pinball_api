from time import sleep
from typing import Any


from tests.qdk.operators.fanatasy_leagues import (
    FantasyLeagueCreateModel,
    FantasyLeagueModel,
    FantasyLeagueSearchModel,
    create_fantasy_league,
    get_fantasy_league_by_id,
    get_fantasy_leagues,
)
from tests.qdk.qa_requests import qa_get
from tests.qdk.types import PagedResponseItemList, RequestOperators, TestContext
from tests.qdk.utils import assert_objects_are_equal, generate_random_string
from util.configuration import (
    get_global_configuration,
    populate_configuration_if_not_exists,
)


def test_gets_fantasy_league_by_id() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object = create_fantasy_league(context)

    result = get_fantasy_league_by_id(context, posted_object.id)

    assert result is not None
    assert result.id == posted_object.id


def test_gets_fantasy_leagues_invalid_inputs() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    result = qa_get(
        f"{context.api_url}/fantasy_leagues",
        query_params={
            "ids": "not an id,also not an id",
            "page": "not a page num",
            "page_length": "not a length num",
            "is_sort_descending": "not a bool",
        },
    )

    assert result.status_code == 422

    errors = result.json()

    assert len(errors["detail"]) == 4

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "query" in error["loc"] and "ids" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "invalid_id_list"
    assert (
        error[0]["msg"]
        == "Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: not an id,\n\t1: also not an id\n]."
    )

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


def test_gets_fantasy_leagues_with_ids_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: FantasyLeagueModel = create_fantasy_league(context)
    posted_object_2: FantasyLeagueModel = create_fantasy_league(context)
    posted_object_3: FantasyLeagueModel = create_fantasy_league(context)
    posted_object_4: FantasyLeagueModel = create_fantasy_league(context)
    create_fantasy_league(context)

    filters: FantasyLeagueSearchModel = FantasyLeagueSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )

    result: PagedResponseItemList[FantasyLeagueModel] = get_fantasy_leagues(
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

    posted_item_1: list[FantasyLeagueModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(posted_item_1) == 1
    assert_objects_are_equal(posted_item_1[0], posted_object_1)

    posted_item_2: list[FantasyLeagueModel] = [
        item for item in result.items if item.id == posted_object_2.id
    ]
    assert len(posted_item_2) == 1
    assert_objects_are_equal(posted_item_2[0], posted_object_2)

    posted_item_3: list[FantasyLeagueModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(posted_item_3) == 1
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[FantasyLeagueModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(posted_item_4) == 1
    assert_objects_are_equal(posted_item_4[0], posted_object_4)


def test_gets_fantasy_leagues_with_paging() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: FantasyLeagueModel = create_fantasy_league(context)
    posted_object_2: FantasyLeagueModel = create_fantasy_league(context)

    sleep(1)

    posted_object_3: FantasyLeagueModel = create_fantasy_league(context)
    posted_object_4: FantasyLeagueModel = create_fantasy_league(context)

    filters_1: FantasyLeagueSearchModel = FantasyLeagueSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page=1,
        page_length=2,
    )

    filters_2: FantasyLeagueSearchModel = FantasyLeagueSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page=2,
        page_length=2,
    )

    result_page_1: PagedResponseItemList[FantasyLeagueModel] = get_fantasy_leagues(
        context, filters_1
    )
    result_page_2: PagedResponseItemList[FantasyLeagueModel] = get_fantasy_leagues(
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

    posted_item_page_1_item_1: list[FantasyLeagueModel] = [
        item for item in result_page_1.items if item.id == posted_object_1.id
    ]
    assert len(posted_item_page_1_item_1) == 1
    assert_objects_are_equal(posted_item_page_1_item_1[0], posted_object_1)

    posted_item_page_1_item_2: list[FantasyLeagueModel] = [
        item for item in result_page_1.items if item.id == posted_object_2.id
    ]
    assert len(posted_item_page_1_item_2) == 1
    assert_objects_are_equal(posted_item_page_1_item_2[0], posted_object_2)

    ## Page 2

    assert result_page_2 is not None
    assert result_page_2.items is not None

    assert result_page_2.paging is not None
    assert result_page_2.paging.page == 2
    assert result_page_2.paging.page_length == 2
    assert result_page_2.paging.sort_by == "created_at"
    assert result_page_2.paging.is_sort_descending == False

    assert len(result_page_1.items) == 2

    posted_item_page_2_item_1: list[FantasyLeagueModel] = [
        item for item in result_page_2.items if item.id == posted_object_3.id
    ]
    assert len(posted_item_page_2_item_1) == 1
    assert_objects_are_equal(posted_item_page_2_item_1[0], posted_object_3)

    posted_item_page_2_item_2: list[FantasyLeagueModel] = [
        item for item in result_page_2.items if item.id == posted_object_4.id
    ]
    assert len(posted_item_page_2_item_2) == 1
    assert_objects_are_equal(posted_item_page_2_item_2[0], posted_object_4)


def test_gets_fantasy_leagues_with_name_exact_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    matching_random_string = generate_random_string(16)

    posted_object_1: FantasyLeagueModel = create_fantasy_league(
        context,
        FantasyLeagueCreateModel(name=f"prefix-{matching_random_string}-matches"),
    )
    posted_object_2: FantasyLeagueModel = create_fantasy_league(
        context, FantasyLeagueCreateModel(name=f"{matching_random_string}-matches")
    )
    posted_object_3: FantasyLeagueModel = create_fantasy_league(
        context,
        FantasyLeagueCreateModel(name=f"{matching_random_string}-matches-suffix"),
    )
    posted_object_4: FantasyLeagueModel = create_fantasy_league(
        context,
        FantasyLeagueCreateModel(
            name=f"prefix-{matching_random_string}-matches-suffix"
        ),
    )

    filters: FantasyLeagueSearchModel = FantasyLeagueSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        name=f"{matching_random_string}-matches",
    )

    result: PagedResponseItemList[FantasyLeagueModel] = get_fantasy_leagues(
        context, filters
    )

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 1

    posted_item_2: list[FantasyLeagueModel] = [
        item for item in result.items if item.id == posted_object_2.id
    ]
    assert len(posted_item_2) == 1
    assert_objects_are_equal(posted_item_2[0], posted_object_2)


def test_gets_fantasy_leagues_with_name_like_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    matching_random_string = generate_random_string(16).upper()
    non_matching_random_string = generate_random_string(16)

    posted_object_1: FantasyLeagueModel = create_fantasy_league(
        context,
        FantasyLeagueCreateModel(name=f"prefix-{matching_random_string}-suffix"),
    )
    posted_object_2: FantasyLeagueModel = create_fantasy_league(
        context, FantasyLeagueCreateModel(name=f"{matching_random_string}-suffix")
    )
    posted_object_3: FantasyLeagueModel = create_fantasy_league(
        context,
        FantasyLeagueCreateModel(name=f"not a match-{non_matching_random_string}"),
    )
    posted_object_4: FantasyLeagueModel = create_fantasy_league(
        context, FantasyLeagueCreateModel(name=f"prefix-{matching_random_string}")
    )

    filters: FantasyLeagueSearchModel = FantasyLeagueSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        name_like=f"{matching_random_string.lower()}",
    )

    result: PagedResponseItemList[FantasyLeagueModel] = get_fantasy_leagues(
        context, filters
    )

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 3

    posted_item_1: list[FantasyLeagueModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(posted_item_1) == 1
    assert_objects_are_equal(posted_item_1[0], posted_object_1)

    posted_item_2: list[FantasyLeagueModel] = [
        item for item in result.items if item.id == posted_object_2.id
    ]
    assert len(posted_item_2) == 1
    assert_objects_are_equal(posted_item_2[0], posted_object_2)

    posted_item_4: list[FantasyLeagueModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(posted_item_4) == 1
    assert_objects_are_equal(posted_item_4[0], posted_object_4)
