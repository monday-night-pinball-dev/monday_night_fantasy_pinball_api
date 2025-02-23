from fastapi import Depends, FastAPI, HTTPException, Request, Response
from pydantic import UUID4
import uvicorn

from models.historical_sale_model import (
    HistoricalSaleInboundCreateModel,
    HistoricalSaleInboundSearchModel, 
    HistoricalSaleOutboundModel,
)
from controllers.historical_sale_controller import HistoricalSaleController
from models.common_model import (
    OutboundItemListResponse, )
from util.environment import Environment

controller: HistoricalSaleController = HistoricalSaleController()


def set_historical_sale_routes(app: FastAPI):

    @app.post(
        '/historical_sales',
        response_model=HistoricalSaleOutboundModel,
        status_code=201,
    )
    def post_historical_sale(
        inbound_create_model: HistoricalSaleInboundCreateModel,  
        request: Request
    ) -> HistoricalSaleOutboundModel | None:
        
        result = controller.create(inbound_create_model, request.headers)

        return result

    @app.get(
        '/historical_sales',
        response_model=OutboundItemListResponse[HistoricalSaleOutboundModel],
    )
    def get_retailer_locations(
        request: Request,
        inbound_search_model: HistoricalSaleInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[HistoricalSaleOutboundModel]:

        result = controller.search(inbound_search_model , request.headers)

        return result

    @app.get(
        '/historical_sales/{id}',
        response_model=HistoricalSaleOutboundModel
    )
    def get_historical_sale_by_id(
        id: UUID4,    
        request: Request
    ):

        result = controller.get_by_id(id, request.headers)

        return result
 
    @app.delete(
        '/historical_sales/{id}',
        response_model=HistoricalSaleOutboundModel
    )
    def delete_historical_sale(
        id: UUID4,
        request: Request
    ):

        result = controller.delete(id, request.headers)

        return result
