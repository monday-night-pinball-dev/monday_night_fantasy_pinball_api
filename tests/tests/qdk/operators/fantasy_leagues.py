import datetime

from requests import Response
from tests.qdk.qa_requests import qa_get, qa_patch, qa_post
from tests.qdk.types import (
    PagedResponseItemList,
    PagingResponseModel,
    PagingRequestModel,
    RequestOperators,
    TestContext,
)
from tests.qdk.utils import (
    assert_object_was_updated,
    assert_objects_are_equal,
    copy_object_when_appropriate,
    generate_random_string,
)


class FantasyLeagueCreateModel:
    def __init__(
        self,
        name: str | None = None,
    ) -> None:
        self.name = name


class FantasyLeagueModel:
    def __init__(
        self,
        id: str,
        name: str,
        created_at: datetime.datetime,
        updated_at: datetime.datetime | None = None,
    ) -> None:
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.name = name


class FantasyLeagueSearchModel(PagingRequestModel):
    def __init__(
        self,
        ids: str | None = None,
        name: str | None = None,
        name_like: str | None = None,
        page: int | None = None,
        page_length: int | None = None,
        is_sort_descending: bool | None = None,
        sort_by: str | None = None,
    ) -> None:
        super().__init__(
            page=page,
            page_length=page_length,
            is_sort_descending=is_sort_descending,
            sort_by=sort_by,
        )

        self.ids = ids
        self.name = name
        self.name_like = name_like


class FantasyLeagueUpdateModel:
    def __init__(
        self,
        name: str | None = None,
    ) -> None:
        self.name = name


def mint_default_fantasy_league(
    context: TestContext,
    overrides: FantasyLeagueCreateModel | None = None,
    request_operators: RequestOperators | None = None,
) -> FantasyLeagueCreateModel:
    random_string = generate_random_string()

    overrides = overrides or FantasyLeagueCreateModel()

    default_fantasy_league: FantasyLeagueCreateModel = FantasyLeagueCreateModel(
        name=random_string + "_fantasy_league_name",
    )

    copy_object_when_appropriate(default_fantasy_league, overrides)

    return default_fantasy_league


def create_fantasy_league(
    context: TestContext,
    overrides: FantasyLeagueCreateModel | None = None,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
) -> FantasyLeagueModel:
    post_object: FantasyLeagueCreateModel = mint_default_fantasy_league(
        context=context, overrides=overrides, request_operators=request_operators
    )

    result: Response = qa_post(
        context.api_url + "/fantasy_leagues", post_object, request_operators
    )

    if allow_failures == False:
        assert result.status_code == 201

        result_dict = result.json()

        assert_objects_are_equal(
            result_dict, post_object.__dict__, ["id", "created_at", "updated_at"]
        )

        assert result_dict["id"] is not None
        assert result_dict["created_at"] is not None
        assert result_dict["updated_at"] is None

    return_object = FantasyLeagueModel(**result.json())

    return return_object


def get_fantasy_league_by_id(
    context: TestContext,
    id: str,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
) -> FantasyLeagueModel:
    url: str = f"{context.api_url}/fantasy_leagues/{id}"

    result: Response = qa_get(url)

    return_object = FantasyLeagueModel(**result.json())

    return return_object


def get_fantasy_leagues(
    context: TestContext,
    search_model: FantasyLeagueSearchModel | None,
    request_operators: RequestOperators | None = None,
) -> PagedResponseItemList[FantasyLeagueModel]:
    url: str = f"{context.api_url}/fantasy_leagues"

    result: Response = qa_get(
        url=url,
        query_params=search_model if search_model is not None else {},
        request_operators=request_operators,
    )

    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict["paging"])

    return_items: list[FantasyLeagueModel] = [
        FantasyLeagueModel(**obj) for obj in result_dict["items"]
    ]

    return_object = PagedResponseItemList[FantasyLeagueModel](
        items=return_items, paging=return_paging_object
    )

    return return_object


def update_fantasy_league(
    context: TestContext,
    id: str,
    update_model: FantasyLeagueUpdateModel | None = None,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
):
    original_object: FantasyLeagueModel = get_fantasy_league_by_id(
        context, id, request_operators
    )

    result = qa_patch(
        f"{context.api_url}/fantasy_leagues/{id}", update_model, request_operators
    )

    if allow_failures == False:
        assert result.status_code == 200

        result_dict = result.json()

        assert_object_was_updated(
            original_object.__dict__,
            update_model.__dict__,
            result_dict,
            ["updated_at"],
        )

        assert result_dict["updated_at"] is not None

    return_object = FantasyLeagueModel(**result.json())

    return return_object
