from uuid import UUID
from fastapi import HTTPException
from fastapi.datastructures import Headers
from adapters.fantasy_league_adapters import FantasyLeagueAdapter
from adapters.common_adapters import CommonAdapters
from managers.fantasy_league_manager import FantasyLeagueManager
from models.fantasy_league_model import (
    FantasyLeagueCreateModel,
    FantasyLeagueInboundCreateModel,
    FantasyLeagueInboundSearchModel,
    FantasyLeagueInboundUpdateModel,
    FantasyLeagueModel,
    FantasyLeagueOutboundModel,
    FantasyLeagueSearchModel,
    FantasyLeagueUpdateModel,
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)
from util.database import PagingModel


class FantasyLeagueController:
    def __init__(
        self,
        adapter: FantasyLeagueAdapter = FantasyLeagueAdapter(),
        common_adapter: CommonAdapters = CommonAdapters(),
        manager: FantasyLeagueManager = FantasyLeagueManager(),
    ) -> None:
        self.adapter = adapter
        self.common_adapter = common_adapter
        self.manager = manager

    def create(
        self, inbound_model: FantasyLeagueInboundCreateModel, headers: dict[str, str]
    ) -> FantasyLeagueOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        model: FantasyLeagueCreateModel = (
            self.adapter.convert_from_inbound_create_model_to_create_model(
                inbound_model
            )
        )

        result = self.manager.create_fantasy_league(model, request_operators)

        if result is None:
            raise Exception("Received no model from create operation.")

        response_model: FantasyLeagueOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model

    def get_by_id(
        self, id: UUID, headers: dict[str, str]
    ) -> FantasyLeagueOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        result = self.manager.get_fantasy_league_by_id(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404, detail=f"FantasyLeague with id {id} not found."
            )

        response_model: FantasyLeagueOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model

    def search(
        self, inbound_model: FantasyLeagueInboundSearchModel, headers: dict[str, str]
    ) -> OutboundItemListResponse[FantasyLeagueOutboundModel]:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        paging_model: PagingModel = (
            self.common_adapter.convert_from_paged_inbound_model_to_paging_model(
                inbound_model
            )
        )

        search_model: FantasyLeagueSearchModel = (
            self.adapter.convert_from_inbound_search_model_to_search_model(
                inbound_model
            )
        )

        results: ItemList[FantasyLeagueModel] = self.manager.search_fantasy_leagues(
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
        inbound_model: FantasyLeagueInboundUpdateModel,
        headers: Headers,
    ):
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        model: FantasyLeagueUpdateModel = (
            self.adapter.convert_from_inbound_update_model_to_update_model(
                inbound_model
            )
        )

        result: None | FantasyLeagueModel = self.manager.update_league_player(
            id, model, request_operators
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"LeaguePlayer with id {id} not found.",
            )

        response_model: FantasyLeagueOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model

    def delete(
        self, id: UUID, headers: dict[str, str]
    ) -> FantasyLeagueOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        result = self.manager.delete_fantasy_league(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404, detail=f"FantasyLeague with id {id} not found."
            )

        response_model: FantasyLeagueOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model
