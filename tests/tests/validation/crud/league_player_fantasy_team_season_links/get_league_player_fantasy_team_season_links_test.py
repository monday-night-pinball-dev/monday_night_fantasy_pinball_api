from time import sleep
from typing import Any


from tests.qdk.operators.league_player_fantasy_team_season_links import (
    LeaguePlayerFantasyTeamSeasonLinkCreateModel,
    LeaguePlayerFantasyTeamSeasonLinkModel,
    LeaguePlayerFantasyTeamSeasonLinkSearchModel,
    league_player_fantasy_team_season_link_hydration_check,
)
from tests.qdk.operators.league_player_fantasy_team_season_links import (
    create_league_player_fantasy_team_season_link,
    get_league_player_fantasy_team_season_link_by_id,
    get_league_player_fantasy_team_season_links,
)
from tests.qdk.operators.league_players import LeaguePlayerCreateModel
from tests.qdk.qa_requests import qa_get
from tests.qdk.types import PagedResponseItemList, RequestOperators, TestContext
from tests.qdk.utils import assert_objects_are_equal
from util.configuration import (
    get_global_configuration,
    populate_configuration_if_not_exists,
)


def test_gets_league_player_fantasy_team_season_link_by_id() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object = create_league_player_fantasy_team_season_link(context)

    result = get_league_player_fantasy_team_season_link_by_id(context, posted_object.id)

    assert result is not None
    assert result.id == posted_object.id


def test_gets_league_player_fantasy_team_season_links_invalid_inputs() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    result = qa_get(
        f"{context.api_url}/league_player_fantasy_team_season_links",
        query_params={
            "ids": "not an id,also not an id",
            "league_player_ids": "not an id,also not an id",
            "league_team_ids": "not an id,also not an id",
            "fantasy_team_season_link_ids": "not an id,also not an id",
            "season_ids": "not an id,also not an id",
            "fantasy_team_ids": "not an id,also not an id",
            "fantasy_team_owner_ids": "not an id,also not an id",
            "fantasy_league_ids": "not an id,also not an id",
            "page": "not a page num",
            "page_length": "not a length num",
            "is_sort_descending": "not a bool",
        },
    )

    assert result.status_code == 422

    errors = result.json()

    assert len(errors["detail"]) == 11

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
        if "query" in error["loc"] and "season_ids" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "invalid_id_list"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "query" in error["loc"] and "league_player_ids" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "invalid_id_list"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "query" in error["loc"] and "league_team_ids" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "invalid_id_list"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "query" in error["loc"] and "fantasy_team_season_link_ids" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "invalid_id_list"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "query" in error["loc"] and "season_ids" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "invalid_id_list"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "query" in error["loc"] and "fantasy_team_ids" in error["loc"]
    ]
    assert len(error) == 1
    assert error[0]["type"] == "invalid_id_list"

    error: list[Any] = [
        error
        for error in errors["detail"]
        if "query" in error["loc"] and "fantasy_team_owner_ids" in error["loc"]
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


def test_gets_league_player_fantasy_team_season_links_with_ids_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )
    posted_object_2: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )
    posted_object_3: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )
    posted_object_4: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )
    create_league_player_fantasy_team_season_link(context)

    filters: LeaguePlayerFantasyTeamSeasonLinkSearchModel = LeaguePlayerFantasyTeamSeasonLinkSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )

    result: PagedResponseItemList[LeaguePlayerFantasyTeamSeasonLinkModel] = (
        get_league_player_fantasy_team_season_links(context, filters)
    )

    assert result is not None
    assert result.items is not None

    assert result.paging is not None
    assert result.paging.page == 1
    assert result.paging.page_length == 25
    assert result.paging.sort_by == "created_at"
    assert result.paging.is_sort_descending == False

    assert len(result.items) == 4

    result_item_1: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(result_item_1) == 1
    assert_objects_are_equal(result_item_1[0], posted_object_1)

    result_item_2: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_2.id
    ]
    assert len(result_item_2) == 1
    assert_objects_are_equal(result_item_2[0], posted_object_2)

    result_item_3: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(result_item_3) == 1
    assert_objects_are_equal(result_item_3[0], posted_object_3)

    result_item_4: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(result_item_4) == 1
    assert_objects_are_equal(result_item_4[0], posted_object_4)


def test_gets_league_players_with_ids_filter_with_hydration() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(
            context,
            LeaguePlayerFantasyTeamSeasonLinkCreateModel(
                league_player=LeaguePlayerCreateModel(create_league_team_if_null=True)
            ),
        )
    )

    posted_object_2: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(
            context,
            LeaguePlayerFantasyTeamSeasonLinkCreateModel(
                league_player=LeaguePlayerCreateModel(create_league_team_if_null=True)
            ),
        )
    )
    posted_object_3: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(
            context,
            LeaguePlayerFantasyTeamSeasonLinkCreateModel(
                league_player=LeaguePlayerCreateModel(create_league_team_if_null=True)
            ),
        )
    )
    posted_object_4: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(
            context,
            LeaguePlayerFantasyTeamSeasonLinkCreateModel(
                league_player=LeaguePlayerCreateModel(create_league_team_if_null=True)
            ),
        )
    )

    filters: LeaguePlayerFantasyTeamSeasonLinkSearchModel = LeaguePlayerFantasyTeamSeasonLinkSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}"
    )

    result: PagedResponseItemList[LeaguePlayerFantasyTeamSeasonLinkModel] = (
        get_league_player_fantasy_team_season_links(
            context,
            filters,
            request_operators=RequestOperators(
                hydration_properties=[
                    "league_player",
                    "league_team",
                    "fantasy_team_season_link",
                    "season",
                    "fantasy_team",
                    "fantasy_team_owner",
                    "fantasy_league",
                ]
            ),
        )
    )

    assert result is not None
    assert result.items is not None

    assert result.paging is not None
    assert result.paging.page == 1
    assert result.paging.page_length == 25
    assert result.paging.sort_by == "created_at"
    assert result.paging.is_sort_descending == False

    assert len(result.items) == 4

    result_item_1: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(result_item_1) == 1
    assert_objects_are_equal(
        result_item_1[0],
        posted_object_1,
        [
            "league_player",
            "league_team",
            "fantasy_team_season_link",
            "season",
            "fantasy_team",
            "fantasy_team_owner",
            "fantasy_league",
        ],
    )

    league_player_fantasy_team_season_link_hydration_check(result_item_1[0])

    result_item_2: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_2.id
    ]
    assert len(result_item_2) == 1
    assert_objects_are_equal(
        result_item_2[0],
        posted_object_2,
        [
            "league_player",
            "league_team",
            "fantasy_team_season_link",
            "season",
            "fantasy_team",
            "fantasy_team_owner",
            "fantasy_league",
        ],
    )

    league_player_fantasy_team_season_link_hydration_check(result_item_2[0])

    result_item_3: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(result_item_3) == 1
    assert_objects_are_equal(
        result_item_3[0],
        posted_object_3,
        [
            "league_player",
            "league_team",
            "fantasy_team_season_link",
            "season",
            "fantasy_team",
            "fantasy_team_owner",
            "fantasy_league",
        ],
    )

    league_player_fantasy_team_season_link_hydration_check(result_item_3[0])

    result_item_4: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(result_item_4) == 1
    assert_objects_are_equal(
        result_item_4[0],
        posted_object_4,
        [
            "league_player",
            "league_team",
            "fantasy_team_season_link",
            "season",
            "fantasy_team",
            "fantasy_team_owner",
            "fantasy_league",
        ],
    )

    league_player_fantasy_team_season_link_hydration_check(result_item_4[0])


def test_gets_league_player_fantasy_team_season_links_with_paging() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )
    posted_object_2: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )

    sleep(1)

    posted_object_3: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )
    posted_object_4: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )

    filters_1: LeaguePlayerFantasyTeamSeasonLinkSearchModel = LeaguePlayerFantasyTeamSeasonLinkSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page=1,
        page_length=2,
    )

    filters_2: LeaguePlayerFantasyTeamSeasonLinkSearchModel = LeaguePlayerFantasyTeamSeasonLinkSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        page=2,
        page_length=2,
    )

    result_page_1: PagedResponseItemList[LeaguePlayerFantasyTeamSeasonLinkModel] = (
        get_league_player_fantasy_team_season_links(context, filters_1)
    )
    result_page_2: PagedResponseItemList[LeaguePlayerFantasyTeamSeasonLinkModel] = (
        get_league_player_fantasy_team_season_links(context, filters_2)
    )

    ## Page 1

    assert result_page_1 is not None
    assert result_page_1.items is not None

    assert result_page_1.paging is not None
    assert result_page_1.paging.page == 1
    assert result_page_1.paging.page_length == 2
    assert result_page_1.paging.sort_by == "created_at"
    assert result_page_1.paging.is_sort_descending == False

    result_item_page_1_item_1: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result_page_1.items if item.id == posted_object_1.id
    ]
    assert len(result_item_page_1_item_1) == 1
    assert_objects_are_equal(result_item_page_1_item_1[0], posted_object_1)

    result_item_page_1_item_2: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
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

    result_item_page_2_item_1: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result_page_2.items if item.id == posted_object_3.id
    ]
    assert len(result_item_page_2_item_1) == 1
    assert_objects_are_equal(result_item_page_2_item_1[0], posted_object_3)

    result_item_page_2_item_2: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result_page_2.items if item.id == posted_object_4.id
    ]
    assert len(result_item_page_2_item_2) == 1
    assert_objects_are_equal(result_item_page_2_item_2[0], posted_object_4)


def test_gets_league_player_fantasy_team_season_links_with_league_player_ids_filter() -> (
    None
):
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )
    posted_object_2: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )
    posted_object_3: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(
            context,
            LeaguePlayerFantasyTeamSeasonLinkCreateModel(
                league_player_id=posted_object_1.league_player_id
            ),
        )
    )
    posted_object_4: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )

    filters: LeaguePlayerFantasyTeamSeasonLinkSearchModel = LeaguePlayerFantasyTeamSeasonLinkSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        league_player_ids=f"{posted_object_1.league_player_id},{posted_object_4.league_player_id}",
    )

    result: PagedResponseItemList[LeaguePlayerFantasyTeamSeasonLinkModel] = (
        get_league_player_fantasy_team_season_links(context, filters)
    )

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 3

    result_item_1: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(result_item_1) == 1
    assert_objects_are_equal(result_item_1[0], posted_object_1)

    result_item_3: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(result_item_3) == 1
    assert_objects_are_equal(result_item_3[0], posted_object_3)

    result_item_4: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(result_item_4) == 1
    assert_objects_are_equal(result_item_4[0], posted_object_4)


def test_gets_league_player_fantasy_team_season_links_with_league_team_ids_filter() -> (
    None
):
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(
            context,
            LeaguePlayerFantasyTeamSeasonLinkCreateModel(
                league_player=LeaguePlayerCreateModel(create_league_team_if_null=True)
            ),
        )
    )
    posted_object_2: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(
            context,
            LeaguePlayerFantasyTeamSeasonLinkCreateModel(
                league_player=LeaguePlayerCreateModel(create_league_team_if_null=True)
            ),
        )
    )
    posted_object_3: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(
            context,
            LeaguePlayerFantasyTeamSeasonLinkCreateModel(
                league_player_id=posted_object_1.league_player_id
            ),
        )
    )
    posted_object_4: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(
            context,
            LeaguePlayerFantasyTeamSeasonLinkCreateModel(
                league_player=LeaguePlayerCreateModel(create_league_team_if_null=True)
            ),
        )
    )

    filters: LeaguePlayerFantasyTeamSeasonLinkSearchModel = LeaguePlayerFantasyTeamSeasonLinkSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        league_team_ids=f"{posted_object_1.league_team_id},{posted_object_4.league_team_id}",
    )

    result: PagedResponseItemList[LeaguePlayerFantasyTeamSeasonLinkModel] = (
        get_league_player_fantasy_team_season_links(context, filters)
    )

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 3

    result_item_1: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(result_item_1) == 1
    assert_objects_are_equal(result_item_1[0], posted_object_1)

    result_item_3: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(result_item_3) == 1
    assert_objects_are_equal(result_item_3[0], posted_object_3)

    result_item_4: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(result_item_4) == 1
    assert_objects_are_equal(result_item_4[0], posted_object_4)


def test_gets_league_player_fantasy_team_season_links_with_fantasy_team_season_link_ids_filter() -> (
    None
):
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )
    posted_object_2: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )
    posted_object_3: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(
            context,
            LeaguePlayerFantasyTeamSeasonLinkCreateModel(
                fantasy_team_season_link_id=posted_object_1.fantasy_team_season_link_id
            ),
        )
    )
    posted_object_4: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )

    filters: LeaguePlayerFantasyTeamSeasonLinkSearchModel = LeaguePlayerFantasyTeamSeasonLinkSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        fantasy_team_season_link_ids=f"{posted_object_1.fantasy_team_season_link_id},{posted_object_4.fantasy_team_season_link_id}",
    )

    result: PagedResponseItemList[LeaguePlayerFantasyTeamSeasonLinkModel] = (
        get_league_player_fantasy_team_season_links(context, filters)
    )

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 3

    result_item_1: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(result_item_1) == 1
    assert_objects_are_equal(result_item_1[0], posted_object_1)

    result_item_3: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(result_item_3) == 1
    assert_objects_are_equal(result_item_3[0], posted_object_3)

    result_item_4: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(result_item_4) == 1
    assert_objects_are_equal(result_item_4[0], posted_object_4)


def test_gets_league_player_fantasy_team_season_links_with_season_ids_filter() -> None:
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )
    posted_object_2: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )
    posted_object_3: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(
            context,
            LeaguePlayerFantasyTeamSeasonLinkCreateModel(
                fantasy_team_season_link_id=posted_object_1.fantasy_team_season_link_id
            ),
        )
    )
    posted_object_4: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )

    filters: LeaguePlayerFantasyTeamSeasonLinkSearchModel = LeaguePlayerFantasyTeamSeasonLinkSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        season_ids=f"{posted_object_1.season_id},{posted_object_4.season_id}",
    )

    result: PagedResponseItemList[LeaguePlayerFantasyTeamSeasonLinkModel] = (
        get_league_player_fantasy_team_season_links(context, filters)
    )

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 3

    result_item_1: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(result_item_1) == 1
    assert_objects_are_equal(result_item_1[0], posted_object_1)

    result_item_3: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(result_item_3) == 1
    assert_objects_are_equal(result_item_3[0], posted_object_3)

    result_item_4: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(result_item_4) == 1
    assert_objects_are_equal(result_item_4[0], posted_object_4)


def test_gets_league_player_fantasy_team_season_links_with_fantasy_team_ids_filter() -> (
    None
):
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )
    posted_object_2: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )
    posted_object_3: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(
            context,
            LeaguePlayerFantasyTeamSeasonLinkCreateModel(
                fantasy_team_season_link_id=posted_object_1.fantasy_team_season_link_id
            ),
        )
    )
    posted_object_4: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )

    filters: LeaguePlayerFantasyTeamSeasonLinkSearchModel = LeaguePlayerFantasyTeamSeasonLinkSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        fantasy_team_ids=f"{posted_object_1.fantasy_team_id},{posted_object_4.fantasy_team_id}",
    )

    result: PagedResponseItemList[LeaguePlayerFantasyTeamSeasonLinkModel] = (
        get_league_player_fantasy_team_season_links(context, filters)
    )

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 3

    result_item_1: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(result_item_1) == 1
    assert_objects_are_equal(result_item_1[0], posted_object_1)

    result_item_3: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(result_item_3) == 1
    assert_objects_are_equal(result_item_3[0], posted_object_3)

    result_item_4: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(result_item_4) == 1
    assert_objects_are_equal(result_item_4[0], posted_object_4)


def test_gets_league_player_fantasy_team_season_links_with_fantasy_team_owner_ids_filter() -> (
    None
):
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )
    posted_object_2: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )
    posted_object_3: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(
            context,
            LeaguePlayerFantasyTeamSeasonLinkCreateModel(
                fantasy_team_season_link_id=posted_object_1.fantasy_team_season_link_id
            ),
        )
    )
    posted_object_4: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )

    filters: LeaguePlayerFantasyTeamSeasonLinkSearchModel = LeaguePlayerFantasyTeamSeasonLinkSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        fantasy_team_owner_ids=f"{posted_object_1.fantasy_team_owner_id},{posted_object_4.fantasy_team_owner_id}",
    )

    result: PagedResponseItemList[LeaguePlayerFantasyTeamSeasonLinkModel] = (
        get_league_player_fantasy_team_season_links(context, filters)
    )

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 3

    result_item_1: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(result_item_1) == 1
    assert_objects_are_equal(result_item_1[0], posted_object_1)

    result_item_3: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(result_item_3) == 1
    assert_objects_are_equal(result_item_3[0], posted_object_3)

    result_item_4: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(result_item_4) == 1
    assert_objects_are_equal(result_item_4[0], posted_object_4)


def test_gets_league_player_fantasy_team_season_links_with_fantasy_league_ids_filter() -> (
    None
):
    populate_configuration_if_not_exists()

    context: TestContext = TestContext(api_url=get_global_configuration().API_URL)

    posted_object_1: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )
    posted_object_2: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )
    posted_object_3: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(
            context,
            LeaguePlayerFantasyTeamSeasonLinkCreateModel(
                fantasy_team_season_link_id=posted_object_1.fantasy_team_season_link_id
            ),
        )
    )
    posted_object_4: LeaguePlayerFantasyTeamSeasonLinkModel = (
        create_league_player_fantasy_team_season_link(context)
    )

    filters: LeaguePlayerFantasyTeamSeasonLinkSearchModel = LeaguePlayerFantasyTeamSeasonLinkSearchModel(
        ids=f"{posted_object_1.id},{posted_object_2.id},{posted_object_3.id},{posted_object_4.id}",
        fantasy_league_ids=f"{posted_object_1.fantasy_league_id},{posted_object_4.fantasy_league_id}",
    )

    result: PagedResponseItemList[LeaguePlayerFantasyTeamSeasonLinkModel] = (
        get_league_player_fantasy_team_season_links(context, filters)
    )

    assert result is not None
    assert result.items is not None

    assert len(result.items) == 3

    result_item_1: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_1.id
    ]
    assert len(result_item_1) == 1
    assert_objects_are_equal(result_item_1[0], posted_object_1)

    result_item_3: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_3.id
    ]
    assert len(result_item_3) == 1
    assert_objects_are_equal(result_item_3[0], posted_object_3)

    result_item_4: list[LeaguePlayerFantasyTeamSeasonLinkModel] = [
        item for item in result.items if item.id == posted_object_4.id
    ]
    assert len(result_item_4) == 1
    assert_objects_are_equal(result_item_4[0], posted_object_4)
