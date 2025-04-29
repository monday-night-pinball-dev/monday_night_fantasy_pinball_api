from time import sleep
from typing import Any

from tests.qdk.operators.league_players import (
    LeaguePlayerCreateModel,
    LeaguePlayerModel,
    LeaguePlayerSearchModel,
    create_league_player,
    get_league_player_by_id,
    get_league_players,
    league_player_hydration_check,
)
from tests.qdk.qa_requests import qa_get
from tests.qdk.types import PagedResponseItemList, RequestOperators, TestContext
from tests.qdk.utils import assert_objects_are_equal, generate_random_string
from util.configuration import (
    get_global_configuration,
    populate_configuration_if_not_exists,
)


def test_gets_league_player_by_id() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object = create_league_player(context)

    result = get_league_player_by_id(context, posted_object.id)

    assert result is not None
    assert result.id == posted_object.id


def test_gets_league_player_by_id_with_hydration() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object = create_league_player(
        context, LeaguePlayerCreateModel(create_league_team_if_null=True)
    )

    result = get_league_player_by_id(
        context,
        posted_object.id,
        request_operators=RequestOperators(hydration_properties=["league_team"]),
    )

    assert result is not None
    assert result.id == posted_object.id

    league_player_hydration_check(result)


def test_gets_league_players_invalid_inputs() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    result = qa_get(
        f"{context.api_url}/league_players",
        query_params={
            "ids": "not an id,also not an id",
            "league_team_ids": "not valid,at all,cmon man",
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
        if "query" in error["loc"] and "league_team_ids" in error["loc"]
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


def test_gets_league_players_with_ids_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: LeaguePlayerModel = create_league_player(context)
    posted_object_2: LeaguePlayerModel = create_league_player(context)
    posted_object_3: LeaguePlayerModel = create_league_player(context)
    posted_object_4: LeaguePlayerModel = create_league_player(context)
    create_league_player(context)

    filters: LeaguePlayerSearchModel = LeaguePlayerSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )

    result: PagedResponseItemList[LeaguePlayerModel] = get_league_players(
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

    result_item_1: list[LeaguePlayerModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(result_item_1) == 1
    assert_objects_are_equal(result_item_1[0], posted_object_1)

    result_item_2: list[LeaguePlayerModel] = [
        item for item in result.items if item.id == posted_object_2.id
    ]
    assert len(result_item_2) == 1
    assert_objects_are_equal(result_item_2[0], posted_object_2)

    result_item_3: list[LeaguePlayerModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(result_item_3) == 1
    assert_objects_are_equal(result_item_3[0], posted_object_3)

    result_item_4: list[LeaguePlayerModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(result_item_4) == 1
    assert_objects_are_equal(result_item_4[0], posted_object_4)


def test_gets_league_players_with_ids_filter_with_hydration() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: LeaguePlayerModel = create_league_player(
        context, LeaguePlayerCreateModel(create_league_team_if_null=True)
    )
    posted_object_2: LeaguePlayerModel = create_league_player(
        context, LeaguePlayerCreateModel(create_league_team_if_null=True)
    )
    posted_object_3: LeaguePlayerModel = create_league_player(
        context, LeaguePlayerCreateModel(create_league_team_if_null=True)
    )
    posted_object_4: LeaguePlayerModel = create_league_player(
        context, LeaguePlayerCreateModel(create_league_team_if_null=True)
    )
    create_league_player(context)

    filters: LeaguePlayerSearchModel = LeaguePlayerSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )

    result: PagedResponseItemList[LeaguePlayerModel] = get_league_players(
        context,
        filters,
        request_operators=RequestOperators(hydration_properties=["league_team"]),
    )

    assert result is not None
    assert result.items is not None

    assert result.paging is not None
    assert result.paging.page == 1
    assert result.paging.page_length == 25
    assert result.paging.sort_by == "created_at"
    assert result.paging.is_sort_descending == False

    assert len(result.items) == 4

    result_item_1: list[LeaguePlayerModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(result_item_1) == 1
    assert_objects_are_equal(result_item_1[0], posted_object_1, ["league_team"])

    assert result_item_1[0].league_team is not None
    assert result_item_1[0].league_team.id is not None
    assert result_item_1[0].league_team.id == result_item_1[0].league_team_id

    result_item_2: list[LeaguePlayerModel] = [
        item for item in result.items if item.id == posted_object_2.id
    ]
    assert len(result_item_2) == 1
    assert_objects_are_equal(result_item_2[0], posted_object_2, ["league_team"])

    assert result_item_2[0].league_team is not None
    assert result_item_2[0].league_team.id is not None
    assert result_item_2[0].league_team.id == result_item_2[0].league_team_id

    result_item_3: list[LeaguePlayerModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(result_item_3) == 1
    assert_objects_are_equal(result_item_3[0], posted_object_3, ["league_team"])

    assert result_item_3[0].league_team is not None
    assert result_item_3[0].league_team.id is not None
    assert result_item_3[0].league_team.id == result_item_3[0].league_team_id

    result_item_4: list[LeaguePlayerModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(result_item_4) == 1
    assert_objects_are_equal(result_item_4[0], posted_object_4, ["league_team"])

    assert result_item_4[0].league_team is not None
    assert result_item_4[0].league_team.id is not None
    assert result_item_4[0].league_team.id == result_item_4[0].league_team_id


def test_gets_league_players_with_paging() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: LeaguePlayerModel = create_league_player(context)
    posted_object_2: LeaguePlayerModel = create_league_player(context)

    sleep(1)

    posted_object_3: LeaguePlayerModel = create_league_player(context)
    posted_object_4: LeaguePlayerModel = create_league_player(context)

    filters_1: LeaguePlayerSearchModel = LeaguePlayerSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page=1,
        page_length=2,
    )

    filters_2: LeaguePlayerSearchModel = LeaguePlayerSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page=2,
        page_length=2,
    )

    result_page_1: PagedResponseItemList[LeaguePlayerModel] = get_league_players(
        context, filters_1
    )
    result_page_2: PagedResponseItemList[LeaguePlayerModel] = get_league_players(
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

    result_item_page_1_item_1: list[LeaguePlayerModel] = [
        item for item in result_page_1.items if item.id == posted_object_1.id
    ]
    assert len(result_item_page_1_item_1) == 1
    assert_objects_are_equal(result_item_page_1_item_1[0], posted_object_1)

    result_item_page_1_item_2: list[LeaguePlayerModel] = [
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

    result_item_page_2_item_1: list[LeaguePlayerModel] = [
        item for item in result_page_2.items if item.id == posted_object_3.id
    ]
    assert len(result_item_page_2_item_1) == 1
    assert_objects_are_equal(result_item_page_2_item_1[0], posted_object_3)

    result_item_page_2_item_2: list[LeaguePlayerModel] = [
        item for item in result_page_2.items if item.id == posted_object_4.id
    ]
    assert len(result_item_page_2_item_2) == 1
    assert_objects_are_equal(result_item_page_2_item_2[0], posted_object_4)


def test_gets_league_players_with_name_exact_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    matching_random_string = generate_random_string(16)

    posted_object_1: LeaguePlayerModel = create_league_player(
        context,
        LeaguePlayerCreateModel(name=f"prefix-{matching_random_string}-matches"),
    )
    posted_object_2: LeaguePlayerModel = create_league_player(
        context, LeaguePlayerCreateModel(name=f"{matching_random_string}-matches")
    )
    posted_object_3: LeaguePlayerModel = create_league_player(
        context,
        LeaguePlayerCreateModel(name=f"{matching_random_string}-matches-suffix"),
    )
    posted_object_4: LeaguePlayerModel = create_league_player(
        context,
        LeaguePlayerCreateModel(name=f"prefix-{matching_random_string}-matches-suffix"),
    )

    filters: LeaguePlayerSearchModel = LeaguePlayerSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        name=f"{matching_random_string}-matches",
    )

    result: PagedResponseItemList[LeaguePlayerModel] = get_league_players(
        context, filters
    )

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 1

    result_item_2: list[LeaguePlayerModel] = [
        item for item in result.items if item.id == posted_object_2.id
    ]
    assert len(result_item_2) == 1
    assert_objects_are_equal(result_item_2[0], posted_object_2)


def test_gets_league_players_with_name_like_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    matching_random_string = generate_random_string(16).upper()
    non_matching_random_string = generate_random_string(16)

    posted_object_1: LeaguePlayerModel = create_league_player(
        context,
        LeaguePlayerCreateModel(name=f"prefix-{matching_random_string}-suffix"),
    )
    posted_object_2: LeaguePlayerModel = create_league_player(
        context, LeaguePlayerCreateModel(name=f"{matching_random_string}-suffix")
    )
    posted_object_3: LeaguePlayerModel = create_league_player(
        context,
        LeaguePlayerCreateModel(name=f"not a match-{non_matching_random_string}"),
    )
    posted_object_4: LeaguePlayerModel = create_league_player(
        context, LeaguePlayerCreateModel(name=f"prefix-{matching_random_string}")
    )

    filters: LeaguePlayerSearchModel = LeaguePlayerSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        name_like=f"{matching_random_string.lower()}",
    )

    result: PagedResponseItemList[LeaguePlayerModel] = get_league_players(
        context, filters
    )

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 3

    result_item_1: list[LeaguePlayerModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(result_item_1) == 1
    assert_objects_are_equal(result_item_1[0], posted_object_1)

    result_item_2: list[LeaguePlayerModel] = [
        item for item in result.items if item.id == posted_object_2.id
    ]
    assert len(result_item_2) == 1
    assert_objects_are_equal(result_item_2[0], posted_object_2)

    result_item_4: list[LeaguePlayerModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(result_item_4) == 1
    assert_objects_are_equal(result_item_4[0], posted_object_4)


def test_gets_league_players_with_league_team_ids_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: LeaguePlayerModel = create_league_player(
        context, LeaguePlayerCreateModel(create_league_team_if_null=True)
    )
    posted_object_2: LeaguePlayerModel = create_league_player(
        context, LeaguePlayerCreateModel(create_league_team_if_null=True)
    )
    posted_object_3: LeaguePlayerModel = create_league_player(
        context, LeaguePlayerCreateModel(league_team_id=posted_object_1.league_team_id)
    )
    posted_object_4: LeaguePlayerModel = create_league_player(
        context, LeaguePlayerCreateModel(create_league_team_if_null=True)
    )

    filters: LeaguePlayerSearchModel = LeaguePlayerSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        league_team_ids=f"{posted_object_1.league_team_id},{posted_object_4.league_team_id}",
    )

    result: PagedResponseItemList[LeaguePlayerModel] = get_league_players(
        context, filters
    )

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 3

    result_item_1: list[LeaguePlayerModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(result_item_1) == 1
    assert_objects_are_equal(result_item_1[0], posted_object_1)

    result_item_3: list[LeaguePlayerModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(result_item_3) == 1
    assert_objects_are_equal(result_item_3[0], posted_object_3)

    result_item_4: list[LeaguePlayerModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(result_item_4) == 1
    assert_objects_are_equal(result_item_4[0], posted_object_4)
