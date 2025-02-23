from fastapi import Depends, FastAPI, HTTPException, Request, Response
from pydantic import UUID4
import uvicorn

from models.inventory_intake_batch_job_model import (
    InventoryIntakeBatchJobInboundCreateModel,
    InventoryIntakeBatchJobInboundSearchModel,
    InventoryIntakeBatchJobInboundUpdateModel,
    InventoryIntakeBatchJobOutboundModel,
)
from controllers.inventory_intake_batch_job_controller import InventoryIntakeBatchJobController
from models.common_model import (
    OutboundItemListResponse, )
from util.environment import Environment

controller: InventoryIntakeBatchJobController = InventoryIntakeBatchJobController()


def set_inventory_intake_batch_job_routes(app: FastAPI):

    @app.post(
        '/inventory_intake_batch_jobs',
        response_model=InventoryIntakeBatchJobOutboundModel,
        status_code=201,
    )
    def post_retailerlocation(
        inbound_create_model: InventoryIntakeBatchJobInboundCreateModel,     
        request: Request
    ):
        result = controller.create(inbound_create_model, request.headers)

        return result

    @app.get(
        '/inventory_intake_batch_jobs',
        response_model=OutboundItemListResponse[InventoryIntakeBatchJobOutboundModel],
    )
    def get_inventory_intake_batch_jobs(
        request: Request,
        inbound_search_model: InventoryIntakeBatchJobInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[InventoryIntakeBatchJobOutboundModel]:

        result = controller.search(inbound_search_model , request.headers)

        return result

    @app.get(
        '/inventory_intake_batch_jobs/{id}',
        response_model=InventoryIntakeBatchJobOutboundModel
    )
    def get_inventory_intake_batch_job_by_id(
        id: UUID4, 
        request: Request
    ) -> InventoryIntakeBatchJobOutboundModel | None:

        result = controller.get_by_id(id, request.headers)

        return result
    
    @app.post(
        '/inventory_intake_batch_jobss/{id}/run',
        response_model=InventoryIntakeBatchJobOutboundModel
    )
    def run_inventory_intake_batch_job (
        id: UUID4, 
        request: Request
    ):

        result = controller.run(id, request.headers)

        return result

    @app.patch(
        '/inventory_intake_batch_jobs/{id}',
        response_model=InventoryIntakeBatchJobOutboundModel
    )
    def patch_inventory_intake_batch_job(
            id: UUID4, 
            inbound_update_model: InventoryIntakeBatchJobInboundUpdateModel,
            request: Request
    ) -> InventoryIntakeBatchJobOutboundModel | None:
        
        result = controller.update(id, inbound_update_model, request.headers)

        return result

    @app.delete(
        '/inventory_intake_batch_jobs/{id}',
        response_model=InventoryIntakeBatchJobOutboundModel
    )
    def delete_inventory_intake_batch_job(id: UUID4, request: Request):

        result = controller.delete(id, request.headers)

        return result
