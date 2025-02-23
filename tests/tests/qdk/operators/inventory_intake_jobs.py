import datetime
from typing import Any

from requests import Response
from tests.qdk.operators.inventory_intake_batch_jobs import (
    InventoryIntakeBatchJobCreateModel,
    InventoryIntakeBatchJobModel,
    create_inventory_intake_batch_job,
)
from tests.qdk.operators.pos_simulator_responses import (
    PosSimulatorResponseCreateModel,
    PosSimulatorResponseModel,
    create_pos_simulator_response,
)
from tests.qdk.operators.retailer_locations import (
    RetailerLocationCreateModel,
    RetailerLocationModel,
    create_retailer_location,
)
from tests.qdk.operators.retailers import RetailerCreateModel, RetailerModel
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


class InventoryIntakeJobCreateModel:
    def __init__(
        self,
        retailer_location_id: str | None = None,
        retailer_location: RetailerLocationCreateModel | None = None,
        parent_batch_job_id: str | None = None,
        parent_batch_job: InventoryIntakeBatchJobCreateModel | None = None,
        create_parent_batch_job_if_null: bool | None = False,
        simulator_response_id: str | None = None,
        simulator_response: PosSimulatorResponseCreateModel | None = None,
        create_simulator_response_if_null: bool | None = False,
        snapshot_hour: str | None = None,
        status: str | None = None,
        status_details: dict[str, Any] | None = None,
    ) -> None:
        self.retailer_location_id = retailer_location_id
        self.retailer_location = retailer_location

        self.parent_batch_job_id = parent_batch_job_id
        self.parent_batch_job = parent_batch_job
        self.create_parent_batch_job_if_null = create_parent_batch_job_if_null

        self.simulator_response_id = simulator_response_id
        self.simulator_response = simulator_response
        self.create_simulator_response_if_null = create_simulator_response_if_null

        self.snapshot_hour = snapshot_hour
        self.status = status
        self.status_details = status_details


class InventoryIntakeJobUpdateModel:
    def __init__(
        self,
        status: str | None = None,
        status_details: dict[str, Any] | None = None,
    ) -> None:
        self.status = status
        self.status_details = status_details


class InventoryIntakeJobModel:
    def __init__(
        self,
        id: str,
        retailer_location_id: str,
        retailer_id: str,
        parent_batch_job_id: str,
        simulator_response_id: str,
        snapshot_hour: str,
        status: str,
        created_at: datetime.datetime,
        retailer_location: RetailerLocationModel | None = None,
        parent_batch_job: InventoryIntakeBatchJobModel | None = None,
        simulator_response: PosSimulatorResponseModel | None = None,
        retailer: RetailerModel | None = None,
        status_details: dict[str, Any] | None = None,
        updated_at: datetime.datetime | None = None,
    ) -> None:
        self.id = id
        self.retailer_location_id = retailer_location_id
        self.retailer_id = retailer_id
        self.simulator_response_id = simulator_response_id
        self.snapshot_hour = snapshot_hour
        self.status = status
        self.parent_batch_job = (
            InventoryIntakeBatchJobModel(**parent_batch_job)
            if parent_batch_job is not None
            else None
        )
        self.parent_batch_job_id = parent_batch_job_id
        self.retailer = RetailerModel(**retailer) if retailer is not None else None
        self.retailer_location = (
            RetailerLocationModel(**retailer_location)
            if retailer_location is not None
            else None
        )
        self.simulator_response = (
            PosSimulatorResponseModel(**simulator_response)
            if simulator_response is not None
            else None
        )
        self.status_details = status_details
        self.created_at = created_at
        self.updated_at = updated_at


class InventoryIntakeJobSearchModel(PagingRequestModel):
    def __init__(
        self,
        ids: str | None = None,
        retailer_ids: str | None = None,
        retailer_location_ids: str | None = None,
        parent_batch_job_ids: str | None = None,
        snapshot_hour_min: str | None = None,
        snapshot_hour_max: str | None = None,
        status: str | None = None,
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
        self.retailer_ids = retailer_ids
        self.retailer_location_ids = retailer_location_ids
        self.parent_batch_job_ids = parent_batch_job_ids

        self.snapshot_hour_min = snapshot_hour_min
        self.snapshot_hour_max = snapshot_hour_max
        self.status = status


def mint_default_inventory_intake_job(
    context: TestContext,
    overrides: InventoryIntakeJobCreateModel | None = None,
    request_operators: RequestOperators | None = None,
) -> InventoryIntakeJobCreateModel:
    random_string = generate_random_string()

    overrides = overrides or InventoryIntakeJobCreateModel()

    if overrides.retailer_location_id is None:
        new_retailer_location = create_retailer_location(
            context, overrides.retailer_location, request_operators=request_operators
        )
        overrides.retailer_location_id = new_retailer_location.id

        del overrides.retailer_location

    if (
        overrides.parent_batch_job_id is None
        and overrides.create_parent_batch_job_if_null is True
    ):
        new_parent_batch_job = create_inventory_intake_batch_job(
            context, overrides.parent_batch_job, request_operators=request_operators
        )
        overrides.parent_batch_job_id = new_parent_batch_job.id

        del overrides.parent_batch_job

    if (
        overrides.simulator_response_id is None
        and overrides.create_simulator_response_if_null is True
    ):
        new_simulator_response = create_pos_simulator_response(
            context, overrides.simulator_response, request_operators=request_operators
        )
        overrides.simulator_response_id = new_simulator_response.id

        del overrides.simulator_response

    default_inventory_intake_job: InventoryIntakeJobCreateModel = (
        InventoryIntakeJobCreateModel(
            snapshot_hour="2024-11-01T11:00:00.111Z",
            status="Requested",
            status_details={"key": "value"},
        )
    )

    copy_object_when_appropriate(default_inventory_intake_job, overrides)

    return default_inventory_intake_job


def create_inventory_intake_job(
    context: TestContext,
    overrides: InventoryIntakeJobCreateModel | None = None,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
) -> InventoryIntakeJobModel:
    post_object: InventoryIntakeJobCreateModel = mint_default_inventory_intake_job(
        context=context, overrides=overrides, request_operators=request_operators
    )

    result: Response = qa_post(
        context.api_url + "/inventory_intake_jobs", post_object, request_operators
    )

    if allow_failures == False:
        assert result.status_code == 201

        result_dict = result.json()

        assert_objects_are_equal(
            result_dict,
            post_object.__dict__,
            [
                "id",
                "created_at",
                "updated_at",
                "retailer_id",
                "retailer",
                "retailer_location_id",
                "retailer_location",
                "parent_batch_job_id",
                "parent_batch_job",
                "simulator_response_id",
                "simulator_response",
                "status",
                "status_details",
            ],
        )

        assert result_dict["id"] is not None
        assert result_dict["created_at"] is not None
        assert result_dict["updated_at"] is None

        if post_object.status is None:
            assert result_dict["status"] == "Requested"
        else:
            assert result_dict["status"] == post_object.status

        if post_object.status_details is None:
            assert result_dict["status_details"] == {}
        else:
            assert result_dict["status_details"] == post_object.status_details

    return_object = InventoryIntakeJobModel(**result.json())

    return return_object


def run_inventory_intake_job(
    context: TestContext,
    id: str,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
) -> InventoryIntakeJobModel:
    url: str = f"{context.api_url}/inventory_intake_jobs/{id}/run"

    result: Response = qa_post(url, {}, request_operators=request_operators)

    return_object = InventoryIntakeJobModel(**result.json())

    return return_object


def get_inventory_intake_job_by_id(
    context: TestContext,
    id: str,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
) -> InventoryIntakeJobModel:
    url: str = f"{context.api_url}/inventory_intake_jobs/{id}"

    result: Response = qa_get(url, request_operators=request_operators)

    return_object = InventoryIntakeJobModel(**result.json())

    return return_object


def get_inventory_intake_jobs(
    context: TestContext,
    search_model: InventoryIntakeJobSearchModel | None,
    request_operators: RequestOperators | None = None,
) -> PagedResponseItemList[InventoryIntakeJobModel]:
    url: str = f"{context.api_url}/inventory_intake_jobs"

    result: Response = qa_get(
        url=url,
        query_params=search_model if search_model is not None else {},
        request_operators=request_operators,
    )

    result_dict = result.json()

    return_paging_object = PagingResponseModel(**result_dict["paging"])

    return_items: list[InventoryIntakeJobModel] = [
        InventoryIntakeJobModel(**obj) for obj in result_dict["items"]
    ]

    return_object = PagedResponseItemList[InventoryIntakeJobModel](
        items=return_items, paging=return_paging_object
    )

    return return_object


def update_inventory_intake_job(
    context: TestContext,
    id: str,
    update_model: InventoryIntakeJobUpdateModel | None = None,
    request_operators: RequestOperators | None = None,
    allow_failures: bool = False,
) -> InventoryIntakeJobModel:
    original_object: InventoryIntakeJobModel = get_inventory_intake_job_by_id(
        context, id, request_operators
    )

    result: Response = qa_patch(
        f"{context.api_url}/inventory_intake_jobs/{id}", update_model, request_operators
    )

    if allow_failures == False:
        assert result.status_code == 200

        result_dict = result.json()

        assert_object_was_updated(
            original_object.__dict__,
            update_model.__dict__,
            result_dict,
            [
                "updated_at",
                "parent_batch_job",
                "retailer",
                "retailer_location",
                "simulator_response",
            ],
        )

        assert result_dict["updated_at"] is not None

    return_object = InventoryIntakeJobModel(**result.json())

    return return_object


def inventory_intake_job_hydration_check(intake_job: InventoryIntakeJobModel) -> None:
    assert intake_job.retailer_location is not None
    assert intake_job.retailer_location.id is not None
    assert intake_job.retailer_location.id == intake_job.retailer_location_id

    assert intake_job.retailer is not None
    assert intake_job.retailer.id is not None
    assert intake_job.retailer.id == intake_job.retailer_id

    assert intake_job.parent_batch_job is not None
    assert intake_job.parent_batch_job.id is not None
    assert intake_job.parent_batch_job.id == intake_job.parent_batch_job_id

    assert intake_job.simulator_response is not None
    assert intake_job.simulator_response.id is not None
    assert intake_job.simulator_response.id == intake_job.simulator_response_id
