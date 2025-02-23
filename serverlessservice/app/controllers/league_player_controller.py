from uuid import UUID

from fastapi import HTTPException
from adapters.league_player_adapters import LeaguePlayerAdapter
from adapters.common_adapters import CommonAdapters
from managers.league_player_manager import LeaguePlayerManager
from models.league_player_model import (
    LeaguePlayerCreateModel,
    LeaguePlayerInboundCreateModel,
    LeaguePlayerInboundSearchModel,
    LeaguePlayerInboundUpdateModel,
    LeaguePlayerModel,
    LeaguePlayerOutboundModel,
    LeaguePlayerSearchModel,
    LeaguePlayerUpdateModel,
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)

from fastapi.datastructures import Headers
from util.database import PagingModel


class LeaguePlayerController:
    def __init__(
        self,
        adapter: LeaguePlayerAdapter = LeaguePlayerAdapter(),
        common_adapter: CommonAdapters = CommonAdapters(),
        manager: LeaguePlayerManager = LeaguePlayerManager(),
    ) -> None:
        self.adapter = adapter
        self.common_adapter = common_adapter
        self.manager = manager

    def create(
        self, inbound_model: LeaguePlayerInboundCreateModel, headers: Headers
    ) -> LeaguePlayerOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        model: LeaguePlayerCreateModel = (
            self.adapter.convert_from_inbound_create_model_to_create_model(
                inbound_model
            )
        )

        result = self.manager.create_league_player(model, request_operators)

        if result is None:
            raise Exception("Received no model from create operation.")

        response_model: LeaguePlayerOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model

    def get_by_id(self, id: UUID, headers: Headers) -> LeaguePlayerOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        result = self.manager.get_league_player_by_id(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"LeaguePlayer with id {id} not found.",
            )

        response_model: LeaguePlayerOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model

    def search(
        self, inbound_model: LeaguePlayerInboundSearchModel, headers: Headers
    ) -> OutboundItemListResponse[LeaguePlayerOutboundModel]:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        paging_model: PagingModel = (
            self.common_adapter.convert_from_paged_inbound_model_to_paging_model(
                inbound_model
            )
        )

        search_model: LeaguePlayerSearchModel = (
            self.adapter.convert_from_inbound_search_model_to_search_model(
                inbound_model
            )
        )

        results: ItemList[LeaguePlayerModel] = self.manager.search_league_players(
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
        inbound_model: LeaguePlayerInboundUpdateModel,
        headers: Headers,
    ):
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        model: LeaguePlayerUpdateModel = (
            self.adapter.convert_from_inbound_update_model_to_update_model(
                inbound_model
            )
        )

        result: None | LeaguePlayerModel = self.manager.update_league_player(
            id, model, request_operators
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"LeaguePlayer with id {id} not found.",
            )

        response_model: LeaguePlayerOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model

    def delete(self, id: UUID, headers: Headers) -> LeaguePlayerOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        result = self.manager.delete_league_player(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"LeaguePlayer with id {id} not found.",
            )

        response_model: LeaguePlayerOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model
