from fastapi import Depends, FastAPI, HTTPException, Request, Response
from pydantic import UUID4
import uvicorn

from models.inventory_intake_job_model import (
    InventoryIntakeJobInboundCreateModel,
    InventoryIntakeJobInboundSearchModel,
    InventoryIntakeJobInboundUpdateModel,
    InventoryIntakeJobOutboundModel,
)
from controllers.inventory_intake_job_controller import InventoryIntakeJobController
from models.common_model import (
    OutboundItemListResponse, )
from util.environment import Environment

controller: InventoryIntakeJobController = InventoryIntakeJobController()


def set_inventory_intake_job_routes(app: FastAPI):

    @app.post(
        '/inventory_intake_jobs',
        response_model=InventoryIntakeJobOutboundModel,
        status_code=201,
    )
    def post_retailerlocation(
        inbound_create_model: InventoryIntakeJobInboundCreateModel,
        request: Request
    ) -> InventoryIntakeJobOutboundModel | None:
        
        result = controller.create(inbound_create_model, request.headers)

        return result

    @app.get(
        '/inventory_intake_jobs',
        response_model=OutboundItemListResponse[InventoryIntakeJobOutboundModel],
    )
    def get_inventory_intake_jobs(
        request: Request,
        inbound_search_model: InventoryIntakeJobInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[InventoryIntakeJobOutboundModel]:

        result = controller.search(inbound_search_model, request.headers)

        return result

    @app.get(
        '/inventory_intake_jobs/{id}',
        response_model=InventoryIntakeJobOutboundModel
    )
    def get_inventory_intake_job_by_id(id: UUID4, request: Request):

        result = controller.get_by_id(id, request.headers)

        return result
    
    @app.post(
        '/inventory_intake_jobs/{id}/run',
        response_model=InventoryIntakeJobOutboundModel
    )
    def run_inventory_intake_job (id: UUID4, request: Request):

        result = controller.run(id, request.headers)

        return result

    @app.patch(
        '/inventory_intake_jobs/{id}',
        response_model=InventoryIntakeJobOutboundModel
    )
    def patch_inventory_intake_job(
            id: UUID4, inbound_update_model: InventoryIntakeJobInboundUpdateModel,
            request: Request
        ) -> InventoryIntakeJobOutboundModel | None:
        
        result = controller.update(id, inbound_update_model, request.headers)

        return result

    @app.delete('/inventory_intake_jobs/{id}',
                response_model=InventoryIntakeJobOutboundModel)
    def delete_inventory_intake_job(id: UUID4, request: Request):

        result = controller.delete(id, request.headers)

        return result
