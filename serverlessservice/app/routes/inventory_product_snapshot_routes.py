from fastapi import Depends, FastAPI, HTTPException, Request, Response
from pydantic import UUID4
import uvicorn

from models.inventory_product_snapshot_model import (
    InventoryProductSnapshotInboundCreateModel,
    InventoryProductSnapshotInboundSearchModel, 
    InventoryProductSnapshotOutboundModel,
)
from controllers.inventory_product_snapshot_controller import InventoryProductSnapshotController
from models.common_model import (
    OutboundItemListResponse
) 

controller: InventoryProductSnapshotController = InventoryProductSnapshotController()


def set_inventory_product_snapshot_routes(app: FastAPI):

    @app.post(
        '/inventory_product_snapshots',
        response_model=InventoryProductSnapshotOutboundModel,
        status_code=201,
    )
    def post_inventory_product_snapshot(
        inbound_create_model: InventoryProductSnapshotInboundCreateModel,
        request: Request):
        
        result = controller.create(inbound_create_model, request.headers)

        return result

    @app.get(
        '/inventory_product_snapshots',
        response_model=OutboundItemListResponse[InventoryProductSnapshotOutboundModel],
    )
    def get_retailer_locations(
        request: Request,
        inbound_search_model: InventoryProductSnapshotInboundSearchModel = Depends(),
    ) -> OutboundItemListResponse[InventoryProductSnapshotOutboundModel]:

        result = controller.search(inbound_search_model, request.headers)

        return result

    @app.get(
        '/inventory_product_snapshots/{id}',
        response_model=InventoryProductSnapshotOutboundModel
    )
    def get_inventory_product_snapshot_by_id(id: UUID4, request: Request):

        result = controller.get_by_id(id, request.headers)

        return result
 
    @app.delete('/inventory_product_snapshots/{id}',
                response_model=InventoryProductSnapshotOutboundModel)
    def delete_inventory_product_snapshot(id: UUID4, request: Request):

        result = controller.delete(id, request.headers)

        return result
