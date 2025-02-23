from fastapi import Depends, FastAPI, HTTPException, Request, Response
from pydantic import UUID4
import uvicorn

from models.product_model import (
    ProductInboundCreateModel,
    ProductInboundSearchModel,
    ProductInboundUpdateModel,
    ProductOutboundModel,
)
from controllers.product_controller import ProductController
from models.common_model import (
    CommonOutboundResponseModel,
    OutboundItemListResponse,
)
from util.environment import Environment

controller: ProductController = ProductController()


def set_product_routes(app: FastAPI):

    @app.post(
        '/products',
        response_model=ProductOutboundModel,
        status_code=201,
    )
    def post_product(
        inbound_create_model: ProductInboundCreateModel, 
        request: Request
    ):
        result = controller.create(inbound_create_model, request.headers)

        return result

    @app.get(
        '/products',
        response_model=OutboundItemListResponse[ProductOutboundModel],
    )
    def get_products(
        request: Request,
        inbound_search_model: ProductInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[ProductOutboundModel]:

        result = controller.search(inbound_search_model, request.headers)

        return result

    @app.get(
        '/products/{id}',
        response_model=ProductOutboundModel,
    )
    def get_product_by_id(
        id: UUID4, 
        request: Request
    ):

        result = controller.get_by_id(id, request.headers)

        return result

    @app.patch(
        '/products/{id}',
        response_model=ProductOutboundModel,
    )
    def patch_product(
        id: UUID4,
        inbound_update_model: ProductInboundUpdateModel,
        request: Request
    ):
        result = controller.update(id, inbound_update_model, request.headers)

        return result

    @app.delete(
        '/products/{id}',
        response_model=ProductOutboundModel,
    )
    def delete_product(id: UUID4, request: Request):

        result = controller.delete(id, request.headers)

        return result
