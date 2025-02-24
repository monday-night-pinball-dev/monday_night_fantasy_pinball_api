from time import sleep
from typing import Any

from tests.qdk.operators.league_teams import (
    LeagueTeamCreateModel,
    LeagueTeamModel,
    LeagueTeamSearchModel,
    create_league_team,
    get_league_team_by_id,
    get_league_teams,
    league_team_hydration_check,
)
from tests.qdk.qa_requests import qa_get
from tests.qdk.types import PagedResponseItemList, RequestOperators, TestContext
from tests.qdk.utils import assert_objects_are_equal, generate_random_string
from util.configuration import (
    get_global_configuration,
    populate_configuration_if_not_exists,
)


def test_gets_league_team_by_id() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object = create_league_team(context)

    result = get_league_team_by_id(context, posted_object.id)

    assert result is not None
    assert result.id == posted_object.id


def test_gets_league_team_by_id_with_hydration() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object = create_league_team(context)

    result = get_league_team_by_id(
        context,
        posted_object.id,
        request_operators=RequestOperators(hydration_properties=["home_venue"]),
    )

    assert result is not None
    assert result.id == posted_object.id

    league_team_hydration_check(result)


def test_gets_league_teams_invalid_inputs() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    result = qa_get(
        f"{context.api_url}/league_teams",
        query_params={
            "ids": "not an id,also not an id",
            "home_venue_ids": "not valid,at all,cmon man",
            "page": "not a page num",
            "page_length": "not a length num",
            "is_sort_descending": "not a bool",
        },
    )

    assert result.status_code == 422

    errors = result.json()

    assert len(errors["detail"]) == 5

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
        if "query" in error["loc"] and "home_venue_ids" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "invalid_id_list"
    assert (
        error[0]["msg"]
        == "Property must be a valid list of v4 uuids. Invalid values received: [\n\t0: not valid,\n\t1: at all,\n\t2: cmon man\n]."
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


def test_gets_league_teams_with_ids_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: LeagueTeamModel = create_league_team(context)
    posted_object_2: LeagueTeamModel = create_league_team(context)
    posted_object_3: LeagueTeamModel = create_league_team(context)
    posted_object_4: LeagueTeamModel = create_league_team(context)
    create_league_team(context)

    filters: LeagueTeamSearchModel = LeagueTeamSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )

    result: PagedResponseItemList[LeagueTeamModel] = get_league_teams(context, filters)

    assert result is not None
    assert result.items is not None

    assert result.paging is not None
    assert result.paging.page == 1
    assert result.paging.page_length == 25
    assert result.paging.sort_by == "created_at"
    assert result.paging.is_sort_descending == False

    assert len(result.items) == 4

    posted_item_1: list[LeagueTeamModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(posted_item_1) == 1
    assert_objects_are_equal(posted_item_1[0], posted_object_1)

    posted_item_2: list[LeagueTeamModel] = [
        item for item in result.items if item.id == posted_object_2.id
    ]
    assert len(posted_item_2) == 1
    assert_objects_are_equal(posted_item_2[0], posted_object_2)

    posted_item_3: list[LeagueTeamModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(posted_item_3) == 1
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[LeagueTeamModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(posted_item_4) == 1
    assert_objects_are_equal(posted_item_4[0], posted_object_4)


def test_gets_league_teams_with_ids_filter_with_hydration() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: LeagueTeamModel = create_league_team(context)
    posted_object_2: LeagueTeamModel = create_league_team(context)
    posted_object_3: LeagueTeamModel = create_league_team(context)
    posted_object_4: LeagueTeamModel = create_league_team(context)
    create_league_team(context)

    filters: LeagueTeamSearchModel = LeagueTeamSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )

    result: PagedResponseItemList[LeagueTeamModel] = get_league_teams(
        context,
        filters,
        request_operators=RequestOperators(hydration_properties=["home_venue"]),
    )

    assert result is not None
    assert result.items is not None

    assert result.paging is not None
    assert result.paging.page == 1
    assert result.paging.page_length == 25
    assert result.paging.sort_by == "created_at"
    assert result.paging.is_sort_descending == False

    assert len(result.items) == 4

    posted_item_1: list[LeagueTeamModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(posted_item_1) == 1
    assert_objects_are_equal(posted_item_1[0], posted_object_1, ["home_venue"])

    assert posted_item_1[0].home_venue is not None
    assert posted_item_1[0].home_venue.id is not None
    assert posted_item_1[0].home_venue.id == posted_item_1[0].home_venue_id

    posted_item_2: list[LeagueTeamModel] = [
        item for item in result.items if item.id == posted_object_2.id
    ]
    assert len(posted_item_2) == 1
    assert_objects_are_equal(posted_item_2[0], posted_object_2, ["home_venue"])

    assert posted_item_2[0].home_venue is not None
    assert posted_item_2[0].home_venue.id is not None
    assert posted_item_2[0].home_venue.id == posted_item_2[0].home_venue_id

    posted_item_3: list[LeagueTeamModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(posted_item_3) == 1
    assert_objects_are_equal(posted_item_3[0], posted_object_3, ["home_venue"])

    assert posted_item_3[0].home_venue is not None
    assert posted_item_3[0].home_venue.id is not None
    assert posted_item_3[0].home_venue.id == posted_item_3[0].home_venue_id

    posted_item_4: list[LeagueTeamModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(posted_item_4) == 1
    assert_objects_are_equal(posted_item_4[0], posted_object_4, ["home_venue"])

    assert posted_item_4[0].home_venue is not None
    assert posted_item_4[0].home_venue.id is not None
    assert posted_item_4[0].home_venue.id == posted_item_4[0].home_venue_id


def test_gets_league_teams_with_paging() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: LeagueTeamModel = create_league_team(context)
    posted_object_2: LeagueTeamModel = create_league_team(context)

    sleep(1)

    posted_object_3: LeagueTeamModel = create_league_team(context)
    posted_object_4: LeagueTeamModel = create_league_team(context)

    filters_1: LeagueTeamSearchModel = LeagueTeamSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page=1,
        page_length=2,
    )

    filters_2: LeagueTeamSearchModel = LeagueTeamSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page=2,
        page_length=2,
    )

    result_page_1: PagedResponseItemList[LeagueTeamModel] = get_league_teams(
        context, filters_1
    )
    result_page_2: PagedResponseItemList[LeagueTeamModel] = get_league_teams(
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

    posted_item_page_1_item_1: list[LeagueTeamModel] = [
        item for item in result_page_1.items if item.id == posted_object_1.id
    ]
    assert len(posted_item_page_1_item_1) == 1
    assert_objects_are_equal(posted_item_page_1_item_1[0], posted_object_1)

    posted_item_page_1_item_2: list[LeagueTeamModel] = [
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

    posted_item_page_2_item_1: list[LeagueTeamModel] = [
        item for item in result_page_2.items if item.id == posted_object_3.id
    ]
    assert len(posted_item_page_2_item_1) == 1
    assert_objects_are_equal(posted_item_page_2_item_1[0], posted_object_3)

    posted_item_page_2_item_2: list[LeagueTeamModel] = [
        item for item in result_page_2.items if item.id == posted_object_4.id
    ]
    assert len(posted_item_page_2_item_2) == 1
    assert_objects_are_equal(posted_item_page_2_item_2[0], posted_object_4)


def test_gets_league_teams_with_name_exact_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    matching_random_string = generate_random_string(16)

    posted_object_1: LeagueTeamModel = create_league_team(
        context,
        LeagueTeamCreateModel(name=f"prefix-{matching_random_string}-matches"),
    )
    posted_object_2: LeagueTeamModel = create_league_team(
        context, LeagueTeamCreateModel(name=f"{matching_random_string}-matches")
    )
    posted_object_3: LeagueTeamModel = create_league_team(
        context,
        LeagueTeamCreateModel(name=f"{matching_random_string}-matches-suffix"),
    )
    posted_object_4: LeagueTeamModel = create_league_team(
        context,
        LeagueTeamCreateModel(name=f"prefix-{matching_random_string}-matches-suffix"),
    )

    filters: LeagueTeamSearchModel = LeagueTeamSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        name=f"{matching_random_string}-matches",
    )

    result: PagedResponseItemList[LeagueTeamModel] = get_league_teams(context, filters)

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 1

    posted_item_2: list[LeagueTeamModel] = [
        item for item in result.items if item.id == posted_object_2.id
    ]
    assert len(posted_item_2) == 1
    assert_objects_are_equal(posted_item_2[0], posted_object_2)


def test_gets_league_teams_with_name_like_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    matching_random_string = generate_random_string(16).upper()
    non_matching_random_string = generate_random_string(16)

    posted_object_1: LeagueTeamModel = create_league_team(
        context,
        LeagueTeamCreateModel(name=f"prefix-{matching_random_string}-suffix"),
    )
    posted_object_2: LeagueTeamModel = create_league_team(
        context, LeagueTeamCreateModel(name=f"{matching_random_string}-suffix")
    )
    posted_object_3: LeagueTeamModel = create_league_team(
        context,
        LeagueTeamCreateModel(name=f"not a match-{non_matching_random_string}"),
    )
    posted_object_4: LeagueTeamModel = create_league_team(
        context, LeagueTeamCreateModel(name=f"prefix-{matching_random_string}")
    )

    filters: LeagueTeamSearchModel = LeagueTeamSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        name_like=f"{matching_random_string.lower()}",
    )

    result: PagedResponseItemList[LeagueTeamModel] = get_league_teams(context, filters)

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 3

    posted_item_1: list[LeagueTeamModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(posted_item_1) == 1
    assert_objects_are_equal(posted_item_1[0], posted_object_1)

    posted_item_2: list[LeagueTeamModel] = [
        item for item in result.items if item.id == posted_object_2.id
    ]
    assert len(posted_item_2) == 1
    assert_objects_are_equal(posted_item_2[0], posted_object_2)

    posted_item_4: list[LeagueTeamModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(posted_item_4) == 1
    assert_objects_are_equal(posted_item_4[0], posted_object_4)


def test_gets_league_teams_with_home_venue_ids_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: LeagueTeamModel = create_league_team(context)
    posted_object_2: LeagueTeamModel = create_league_team(context)
    posted_object_3: LeagueTeamModel = create_league_team(
        context, LeagueTeamCreateModel(home_venue_id=posted_object_1.home_venue_id)
    )
    posted_object_4: LeagueTeamModel = create_league_team(context)

    filters: LeagueTeamSearchModel = LeagueTeamSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        home_venue_ids=f"{posted_object_1.home_venue_id},{posted_object_4.home_venue_id}",
    )

    result: PagedResponseItemList[LeagueTeamModel] = get_league_teams(context, filters)

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 3

    posted_item_1: list[LeagueTeamModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(posted_item_1) == 1
    assert_objects_are_equal(posted_item_1[0], posted_object_1)

    posted_item_3: list[LeagueTeamModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(posted_item_3) == 1
    assert_objects_are_equal(posted_item_3[0], posted_object_3)

    posted_item_4: list[LeagueTeamModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(posted_item_4) == 1
    assert_objects_are_equal(posted_item_4[0], posted_object_4)


def test_gets_league_teams_with_short_name_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: LeagueTeamModel = create_league_team(
        context, LeagueTeamCreateModel(short_name=f"AAA")
    )
    posted_object_2: LeagueTeamModel = create_league_team(
        context, LeagueTeamCreateModel(short_name=f"BBB")
    )
    posted_object_3: LeagueTeamModel = create_league_team(
        context, LeagueTeamCreateModel(short_name=f"AAA")
    )
    posted_object_4: LeagueTeamModel = create_league_team(
        context, LeagueTeamCreateModel(short_name=f"CCC")
    )

    filters: LeagueTeamSearchModel = LeagueTeamSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        short_name=f"AAA",
    )

    result: PagedResponseItemList[LeagueTeamModel] = get_league_teams(context, filters)

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 2

    posted_item_1: list[LeagueTeamModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(posted_item_1) == 1
    assert_objects_are_equal(posted_item_1[0], posted_object_1)

    posted_item_3: list[LeagueTeamModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(posted_item_3) == 1
    assert_objects_are_equal(posted_item_3[0], posted_object_3)
