from fastapi import Depends, FastAPI, HTTPException, Request, Response
from pydantic import UUID4
import uvicorn

from models.sales_intake_job_model import (
    SalesIntakeJobInboundCreateModel,
    SalesIntakeJobInboundSearchModel,
    SalesIntakeJobInboundUpdateModel,
    SalesIntakeJobOutboundModel,
)
from controllers.sales_intake_job_controller import SalesIntakeJobController
from models.common_model import (
    OutboundItemListResponse, )
from util.environment import Environment

controller: SalesIntakeJobController = SalesIntakeJobController()

def set_sales_intake_job_routes(app: FastAPI):

    @app.post(
        '/sales_intake_jobs',
        response_model=SalesIntakeJobOutboundModel,
        status_code=201,
    )
    def post_retailerlocation(
        inbound_create_model: SalesIntakeJobInboundCreateModel,
        request: Request
    ):
        result = controller.create(inbound_create_model, request.headers)

        return result

    @app.get(
        '/sales_intake_jobs',
        response_model=OutboundItemListResponse[SalesIntakeJobOutboundModel],
    )
    def get_sales_intake_jobs(
        request: Request,
        inbound_search_model: SalesIntakeJobInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[SalesIntakeJobOutboundModel]:

        result = controller.search(inbound_search_model, request.headers)

        return result

    @app.get('/sales_intake_jobs/{id}',
             response_model=SalesIntakeJobOutboundModel)
    def get_sales_intake_job_by_id(id: UUID4, request: Request):

        result = controller.get_by_id(id, request.headers)

        return result
    
    @app.post('/sales_intake_jobs/{id}/run',
             response_model=SalesIntakeJobOutboundModel)
    def run_sales_intake_job (id: UUID4, request: Request):

        result = controller.run(id, request.headers)

        return result

    @app.patch('/sales_intake_jobs/{id}',
               response_model=SalesIntakeJobOutboundModel)
    def patch_sales_intake_job(
        id: UUID4, 
        inbound_update_model: SalesIntakeJobInboundUpdateModel,
        request: Request
    ):
        result = controller.update(id, inbound_update_model, request.headers)

        return result

    @app.delete('/sales_intake_jobs/{id}',
                response_model=SalesIntakeJobOutboundModel)
    def delete_sales_intake_job(id: UUID4, request: Request):

        result = controller.delete(id, request.headers)

        return result
