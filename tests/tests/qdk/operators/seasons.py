import datetime
import random

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


class SeasonCreateModel:
    def __init__(
        self,
        name: str | None = None,
        season_number: int | None = None,
    ) -> None:
        self.name = name
        self.season_number = season_number


class SeasonUpdateModel:
    def __init__(
        self,
        name: str | None = None,
    ) -> None:
        self.name = name


class SeasonModel:
    def __init__(
        self,
        id: str,
        name: str,
        season_number: int,
        created_at: datetime.datetime,
        updated_at: datetime.datetime | None = None,
    ) -> None:
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.name = name
        self.season_number = season_number


class SeasonSearchModel(PagingRequestModel):
    def __init__(
        self,
        ids: str | None = None,
        name: str | None = None,
        name_like: str | None = None,
        season_number_min: int | None = None,
        season_number_max: int | None = None,
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
        self.season_number_min = season_number_min
        self.season_number_max = season_number_max


def mint_default_season(
    context: TestContext,
    overrides: SeasonCreateModel | None = None,
    request_operators: RequestOperators | None = None,
) -> SeasonCreateModel:
    random_string = generate_random_string()

    random_int = random.randint(1, 1000000000)

    overrides = overrides or SeasonCreateModel()

    default_season: SeasonCreateModel = SeasonCreateModel(
        name=random_string + "_season_name", season_number=random_int
    )

    copy_object_when_appropriate(default_season, overrides)

    return default_season


def create_season(
    context: TestContext,
    overrides: SeasonCreateModel | None = None,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
) -> SeasonModel:
    post_object: SeasonCreateModel = mint_default_season(
        context=context, overrides=overrides, request_operators=request_operators
    )

    result: Response = qa_post(
        context.api_url + "/seasons", post_object, request_operators
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

    return_object = SeasonModel(**result.json())

    return return_object


def get_season_by_id(
    context: TestContext,
    id: str,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
) -> SeasonModel:
    url: str = f"{context.api_url}/seasons/{id}"

    result: Response = qa_get(url)

    return_object = SeasonModel(**result.json())

    return return_object


def get_seasons(
    context: TestContext,
    search_model: SeasonSearchModel | None,
    request_operators: RequestOperators | None = None,
) -> PagedResponseItemList[SeasonModel]:
    url: str = f"{context.api_url}/seasons"

    result: Response = qa_get(
        url=url,
        query_params=search_model if search_model is not None else {},
        request_operators=request_operators,
    )

    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict["paging"])

    return_items: list[SeasonModel] = [
        SeasonModel(**obj) for obj in result_dict["items"]
    ]

    return_object = PagedResponseItemList[SeasonModel](
        items=return_items, paging=return_paging_object
    )

    return return_object


def update_season(
    context: TestContext,
    id: str,
    update_model: SeasonUpdateModel | None = None,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
):
    original_object: SeasonModel = get_season_by_id(context, id, request_operators)

    result = qa_patch(
        f"{context.api_url}/seasons/{id}", update_model, request_operators
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

    return_object = SeasonModel(**result.json())

    return return_object
