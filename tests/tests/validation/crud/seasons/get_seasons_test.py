import random
from time import sleep
from typing import Any


from tests.qdk.operators.seasons import (
    SeasonCreateModel,
    SeasonModel,
    SeasonSearchModel,
    create_season,
    get_season_by_id,
    get_seasons,
)
from tests.qdk.qa_requests import qa_get
from tests.qdk.types import PagedResponseItemList, TestContext
from tests.qdk.utils import assert_objects_are_equal, generate_random_string
from util.configuration import (
    get_global_configuration,
    populate_configuration_if_not_exists,
)


def test_gets_season_by_id() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object = create_season(context)

    result = get_season_by_id(context, posted_object.id)

    assert result is not None
    assert result.id == posted_object.id


def test_gets_seasons_invalid_inputs() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    result = qa_get(
        f"{context.api_url}/seasons",
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


def test_gets_seasons_with_ids_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: SeasonModel = create_season(context)
    posted_object_2: SeasonModel = create_season(context)
    posted_object_3: SeasonModel = create_season(context)
    posted_object_4: SeasonModel = create_season(context)
    create_season(context)

    filters: SeasonSearchModel = SeasonSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )

    result: PagedResponseItemList[SeasonModel] = get_seasons(context, filters)

    assert result is not None
    assert result.items is not None

    assert result.paging is not None
    assert result.paging.page == 1
    assert result.paging.page_length == 25
    assert result.paging.sort_by == "created_at"
    assert result.paging.is_sort_descending == False

    assert len(result.items) == 4

    posted_item_1: list[SeasonModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(posted_item_1) == 1
    assert_objects_are_equal(posted_item_1[0], posted_object_1)

    posted_item_2: list[SeasonModel] = [
        item for item in result.items if item.id == posted_object_2.id
    ]
    assert len(posted_item_2) == 1
    assert_objects_are_equal(posted_item_2[0], posted_object_2)

    posted_item_3: list[SeasonModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(posted_item_3) == 1
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[SeasonModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(posted_item_4) == 1
    assert_objects_are_equal(posted_item_4[0], posted_object_4)


def test_gets_seasons_with_paging() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: SeasonModel = create_season(context)
    posted_object_2: SeasonModel = create_season(context)

    sleep(1)

    posted_object_3: SeasonModel = create_season(context)
    posted_object_4: SeasonModel = create_season(context)

    filters_1: SeasonSearchModel = SeasonSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page=1,
        page_length=2,
    )

    filters_2: SeasonSearchModel = SeasonSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page=2,
        page_length=2,
    )

    result_page_1: PagedResponseItemList[SeasonModel] = get_seasons(context, filters_1)
    result_page_2: PagedResponseItemList[SeasonModel] = get_seasons(context, filters_2)

    ## Page 1

    assert result_page_1 is not None
    assert result_page_1.items is not None

    assert result_page_1.paging is not None
    assert result_page_1.paging.page == 1
    assert result_page_1.paging.page_length == 2
    assert result_page_1.paging.sort_by == "created_at"
    assert result_page_1.paging.is_sort_descending == False

    posted_item_page_1_item_1: list[SeasonModel] = [
        item for item in result_page_1.items if item.id == posted_object_1.id
    ]
    assert len(posted_item_page_1_item_1) == 1
    assert_objects_are_equal(posted_item_page_1_item_1[0], posted_object_1)

    posted_item_page_1_item_2: list[SeasonModel] = [
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

    posted_item_page_2_item_1: list[SeasonModel] = [
        item for item in result_page_2.items if item.id == posted_object_3.id
    ]
    assert len(posted_item_page_2_item_1) == 1
    assert_objects_are_equal(posted_item_page_2_item_1[0], posted_object_3)

    posted_item_page_2_item_2: list[SeasonModel] = [
        item for item in result_page_2.items if item.id == posted_object_4.id
    ]
    assert len(posted_item_page_2_item_2) == 1
    assert_objects_are_equal(posted_item_page_2_item_2[0], posted_object_4)


def test_gets_seasons_with_name_exact_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    matching_random_string = generate_random_string(16)

    posted_object_1: SeasonModel = create_season(
        context, SeasonCreateModel(name=f"prefix-{matching_random_string}-matches")
    )
    posted_object_2: SeasonModel = create_season(
        context, SeasonCreateModel(name=f"{matching_random_string}-matches")
    )
    posted_object_3: SeasonModel = create_season(
        context, SeasonCreateModel(name=f"{matching_random_string}-matches-suffix")
    )
    posted_object_4: SeasonModel = create_season(
        context,
        SeasonCreateModel(name=f"prefix-{matching_random_string}-matches-suffix"),
    )

    filters: SeasonSearchModel = SeasonSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        name=f"{matching_random_string}-matches",
    )

    result: PagedResponseItemList[SeasonModel] = get_seasons(context, filters)

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 1

    posted_item_2: list[SeasonModel] = [
        item for item in result.items if item.id == posted_object_2.id
    ]
    assert len(posted_item_2) == 1
    assert_objects_are_equal(posted_item_2[0], posted_object_2)


def test_gets_seasons_with_name_like_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    matching_random_string = generate_random_string(16).upper()
    non_matching_random_string = generate_random_string(16)

    posted_object_1: SeasonModel = create_season(
        context, SeasonCreateModel(name=f"prefix-{matching_random_string}-suffix")
    )
    posted_object_2: SeasonModel = create_season(
        context, SeasonCreateModel(name=f"{matching_random_string}-suffix")
    )
    posted_object_3: SeasonModel = create_season(
        context, SeasonCreateModel(name=f"not a match-{non_matching_random_string}")
    )
    posted_object_4: SeasonModel = create_season(
        context, SeasonCreateModel(name=f"prefix-{matching_random_string}")
    )

    filters: SeasonSearchModel = SeasonSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        name_like=f"{matching_random_string.lower()}",
    )

    result: PagedResponseItemList[SeasonModel] = get_seasons(context, filters)

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 3

    posted_item_1: list[SeasonModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(posted_item_1) == 1
    assert_objects_are_equal(posted_item_1[0], posted_object_1)

    posted_item_2: list[SeasonModel] = [
        item for item in result.items if item.id == posted_object_2.id
    ]
    assert len(posted_item_2) == 1
    assert_objects_are_equal(posted_item_2[0], posted_object_2)

    posted_item_4: list[SeasonModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(posted_item_4) == 1
    assert_objects_are_equal(posted_item_4[0], posted_object_4)


def test_gets_seasons_with_season_number_min_max_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    random_int = random.randint(1, 1000000000)

    posted_object_1: SeasonModel = create_season(
        context, SeasonCreateModel(season_number=random_int)
    )
    posted_object_2: SeasonModel = create_season(
        context, SeasonCreateModel(season_number=random_int + 1)
    )
    posted_object_3: SeasonModel = create_season(
        context, SeasonCreateModel(season_number=random_int + 2)
    )
    posted_object_4: SeasonModel = create_season(
        context, SeasonCreateModel(season_number=random_int + 3)
    )

    min_filters: SeasonSearchModel = SeasonSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        season_number_min=random_int + 1,
    )

    max_filters: SeasonSearchModel = SeasonSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        season_number_max=random_int + 2,
    )

    both_filters: SeasonSearchModel = SeasonSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        season_number_min=random_int + 1,
        season_number_max=random_int + 2,
    )

    min_result: PagedResponseItemList[SeasonModel] = get_seasons(context, min_filters)
    max_result: PagedResponseItemList[SeasonModel] = get_seasons(context, max_filters)
    both_result: PagedResponseItemList[SeasonModel] = get_seasons(context, both_filters)

    # assert min
    assert min_result is not None
    assert min_result.items is not None

    assert len(min_result.items) == 3

    min_posted_item_2: list[SeasonModel] = [
        item for item in min_result.items if item.id == posted_object_2.id
    ]
    assert len(min_posted_item_2) == 1
    assert_objects_are_equal(min_posted_item_2[0], posted_object_2)

    min_posted_item_3: list[SeasonModel] = [
        item for item in min_result.items if item.id == posted_object_3.id
    ]
    assert len(min_posted_item_3) == 1
    assert_objects_are_equal(min_posted_item_3[0], posted_object_3)

    min_posted_item_4: list[SeasonModel] = [
        item for item in min_result.items if item.id == posted_object_4.id
    ]
    assert len(min_posted_item_4) == 1
    assert_objects_are_equal(min_posted_item_4[0], posted_object_4)

    # assert max
    assert max_result is not None
    assert max_result.items is not None

    assert len(max_result.items) == 3

    max_posted_item_1: list[SeasonModel] = [
        item for item in max_result.items if item.id == posted_object_1.id
    ]
    assert len(max_posted_item_1) == 1
    assert_objects_are_equal(max_posted_item_1[0], posted_object_1)

    max_posted_item_2: list[SeasonModel] = [
        item for item in max_result.items if item.id == posted_object_2.id
    ]
    assert len(max_posted_item_2) == 1
    assert_objects_are_equal(max_posted_item_2[0], posted_object_2)

    max_posted_item_3: list[SeasonModel] = [
        item for item in max_result.items if item.id == posted_object_3.id
    ]
    assert len(max_posted_item_3) == 1
    assert_objects_are_equal(max_posted_item_3[0], posted_object_3)

    # assert both
    assert both_result is not None
    assert both_result.items is not None

    assert len(both_result.items) == 2

    both_posted_item_2: list[SeasonModel] = [
        item for item in both_result.items if item.id == posted_object_2.id
    ]
    assert len(both_posted_item_2) == 1
    assert_objects_are_equal(both_posted_item_2[0], posted_object_2)

    both_posted_item_3: list[SeasonModel] = [
        item for item in both_result.items if item.id == posted_object_3.id
    ]
    assert len(both_posted_item_3) == 1
    assert_objects_are_equal(both_posted_item_3[0], posted_object_3)
