import datetime

from requests import Response
from tests.qdk.qa_requests import qa_get, qa_post
from tests.qdk.types import (
    PagedResponseItemList,
    PagingResponseModel,
    PagingRequestModel,
    RequestOperators,
    TestContext,
)
from tests.qdk.utils import (
    assert_objects_are_equal,
    copy_object_when_appropriate,
    generate_random_string,
)


class VenueCreateModel:
    def __init__(
        self,
        name: str | None = None,
    ) -> None:
        self.name = name


class VenueModel:
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


class VenueSearchModel(PagingRequestModel):
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


def mint_default_venue(
    context: TestContext,
    overrides: VenueCreateModel | None = None,
    request_operators: RequestOperators | None = None,
) -> VenueCreateModel:
    random_string = generate_random_string()

    overrides = overrides or VenueCreateModel()

    default_venue: VenueCreateModel = VenueCreateModel(
        name=random_string + "_venue_name",
    )

    copy_object_when_appropriate(default_venue, overrides)

    return default_venue


def create_venue(
    context: TestContext,
    overrides: VenueCreateModel | None = None,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
) -> VenueModel:
    post_object: VenueCreateModel = mint_default_venue(
        context=context, overrides=overrides, request_operators=request_operators
    )

    result: Response = qa_post(
        context.api_url + "/venues", post_object, request_operators
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

    return_object = VenueModel(**result.json())

    return return_object


def get_venue_by_id(
    context: TestContext,
    id: str,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
) -> VenueModel:
    url: str = f"{context.api_url}/venues/{id}"

    result: Response = qa_get(url)

    return_object = VenueModel(**result.json())

    return return_object


def get_venues(
    context: TestContext,
    search_model: VenueSearchModel | None,
    request_operators: RequestOperators | None = None,
) -> PagedResponseItemList[VenueModel]:
    url: str = f"{context.api_url}/venues"

    result: Response = qa_get(
        url=url,
        query_params=search_model if search_model is not None else {},
        request_operators=request_operators,
    )

    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict["paging"])

    return_items: list[VenueModel] = [VenueModel(**obj) for obj in result_dict["items"]]

    return_object = PagedResponseItemList[VenueModel](
        items=return_items, paging=return_paging_object
    )

    return return_object
