from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from pydantic import UUID4, Strict
import uvicorn

from models.vendor_model import (
    VendorInboundCreateModel,
    VendorInboundSearchModel,
    VendorInboundUpdateModel,
    VendorOutboundModel,
)

from controllers.vendor_controller import VendorController

from models.common_model import ( 
    OutboundItemListResponse,
)
from util.environment import Environment

controller: VendorController = VendorController() 

def set_vendor_routes(app: FastAPI):

    @app.post('/vendors', response_model=VendorOutboundModel, status_code=201)
    def post_vendor(inbound_create_model: VendorInboundCreateModel, request: Request):
        result = controller.create(inbound_create_model, request.headers)

        return result

    @app.get(
        '/vendors',
        response_model=OutboundItemListResponse[VendorOutboundModel],
    )
    def get_vendors(
        request: Request,
        inbound_search_model: VendorInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[VendorOutboundModel]:

        result = controller.search(inbound_search_model, request.headers)

        return result

    @app.get('/vendors/{id}', response_model=VendorOutboundModel)
    def get_vendor_by_id(id: UUID4, request: Request):

        result = controller.get_by_id(id, request.headers)

        return result

    @app.patch('/vendors/{id}', response_model=VendorOutboundModel)
    def patch_vendor(
        id: UUID4,
        inbound_update_model: VendorInboundUpdateModel,
        request: Request
    ):
        result = controller.update(id, inbound_update_model, request.headers)

        return result

    @app.delete('/vendors/{id}', response_model=VendorOutboundModel)
    def delete_vendor(id: UUID4, request: Request):

        result = controller.delete(id, request.headers)

        return result
