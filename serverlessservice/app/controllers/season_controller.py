from uuid import UUID
from fastapi import HTTPException
from adapters.season_adapters import SeasonAdapter
from adapters.common_adapters import CommonAdapters
from managers.season_manager import SeasonManager
from models.season_model import (
    SeasonCreateModel,
    SeasonInboundCreateModel,
    SeasonInboundSearchModel,
    SeasonInboundUpdateModel,
    SeasonModel,
    SeasonOutboundModel,
    SeasonSearchModel,
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)
from util.database import PagingModel


class SeasonController:
    def __init__(
        self,
        adapter: SeasonAdapter = SeasonAdapter(),
        common_adapter: CommonAdapters = CommonAdapters(),
        manager: SeasonManager = SeasonManager(),
    ) -> None:
        self.adapter = adapter
        self.common_adapter = common_adapter
        self.manager = manager

    def create(
        self, inbound_model: SeasonInboundCreateModel, headers: dict[str, str]
    ) -> SeasonOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        model: SeasonCreateModel = (
            self.adapter.convert_from_inbound_create_model_to_create_model(
                inbound_model
            )
        )

        result = self.manager.create_season(model, request_operators)

        if result is None:
            raise Exception("Received no model from create operation.")

        response_model: SeasonOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model

    def get_by_id(
        self, id: UUID, headers: dict[str, str]
    ) -> SeasonOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        result = self.manager.get_season_by_id(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404, detail=f"Season with id {id} not found."
            )

        response_model: SeasonOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model

    def search(
        self, inbound_model: SeasonInboundSearchModel, headers: dict[str, str]
    ) -> OutboundItemListResponse[SeasonOutboundModel]:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        paging_model: PagingModel = (
            self.common_adapter.convert_from_paged_inbound_model_to_paging_model(
                inbound_model
            )
        )

        search_model: SeasonSearchModel = (
            self.adapter.convert_from_inbound_search_model_to_search_model(
                inbound_model
            )
        )

        results: ItemList[SeasonModel] = self.manager.search_seasons(
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

    def update(
        self,
        id: UUID,
        inbound_model: SeasonInboundUpdateModel,
        headers: dict[str, str],
    ) -> SeasonOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        model: SeasonCreateModel = (
            self.adapter.convert_from_inbound_update_model_to_create_model(
                inbound_model
            )
        )

        result = self.manager.update_season(id, model, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404, detail=f"Season with id {id} not found."
            )

        response_model: SeasonOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model

    def delete(self, id: UUID, headers: dict[str, str]) -> SeasonOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        result = self.manager.delete_season(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404, detail=f"Season with id {id} not found."
            )

        response_model: SeasonOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model
