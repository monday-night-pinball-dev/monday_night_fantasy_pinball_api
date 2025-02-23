from uuid import UUID
from fastapi import HTTPException
from adapters.venue_adapters import VenueAdapter
from adapters.common_adapters import CommonAdapters
from managers.venue_manager import VenueManager
from models.venue_model import (
    VenueCreateModel,
    VenueInboundCreateModel,
    VenueInboundSearchModel,
    VenueModel,
    VenueOutboundModel,
    VenueSearchModel,
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)
from util.database import PagingModel


class VenueController:
    def __init__(
        self,
        adapter: VenueAdapter = VenueAdapter(),
        common_adapter: CommonAdapters = CommonAdapters(),
        manager: VenueManager = VenueManager(),
    ) -> None:
        self.adapter = adapter
        self.common_adapter = common_adapter
        self.manager = manager

    def create(
        self, inbound_model: VenueInboundCreateModel, headers: dict[str, str]
    ) -> VenueOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        model: VenueCreateModel = (
            self.adapter.convert_from_inbound_create_model_to_create_model(
                inbound_model
            )
        )

        result = self.manager.create_venue(model, request_operators)

        if result is None:
            raise Exception("Received no model from create operation.")

        response_model: VenueOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model

    def get_by_id(self, id: UUID, headers: dict[str, str]) -> VenueOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        result = self.manager.get_venue_by_id(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404, detail=f"Venue with id {id} not found."
            )

        response_model: VenueOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model

    def search(
        self, inbound_model: VenueInboundSearchModel, headers: dict[str, str]
    ) -> OutboundItemListResponse[VenueOutboundModel]:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        paging_model: PagingModel = (
            self.common_adapter.convert_from_paged_inbound_model_to_paging_model(
                inbound_model
            )
        )

        search_model: VenueSearchModel = (
            self.adapter.convert_from_inbound_search_model_to_search_model(
                inbound_model
            )
        )

        results: ItemList[VenueModel] = self.manager.search_venues(
            search_model, paging_model, request_operators
        )

        return_result_list = list(
            map(
                lambda x: self.adapter.convert_from_model_to_outbound_model(x),
                results.items,
            )
        )

        outbound_paging: OutboundResultantPagingModel = (
            self.common_adapter.convert_from_paging_model_to_outbound_paging_model(
                results.paging
            )
        )

        return_result = OutboundItemListResponse(
            items=return_result_list, paging=outbound_paging
        )

        return return_result

    def delete(self, id: UUID, headers: dict[str, str]) -> VenueOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        result = self.manager.delete_venue(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404, detail=f"Venue with id {id} not found."
            )

        response_model: VenueOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model
