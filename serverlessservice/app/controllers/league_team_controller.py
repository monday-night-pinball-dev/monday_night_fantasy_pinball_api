from uuid import UUID

from fastapi import HTTPException
from adapters.league_team_adapters import LeagueTeamAdapter
from adapters.common_adapters import CommonAdapters
from managers.league_team_manager import LeagueTeamManager
from models.league_team_model import (
    LeagueTeamCreateModel,
    LeagueTeamInboundCreateModel,
    LeagueTeamInboundSearchModel,
    LeagueTeamInboundUpdateModel,
    LeagueTeamModel,
    LeagueTeamOutboundModel,
    LeagueTeamSearchModel,
    LeagueTeamUpdateModel,
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)

from fastapi.datastructures import Headers
from util.database import PagingModel


class LeagueTeamController:
    def __init__(
        self,
        adapter: LeagueTeamAdapter = LeagueTeamAdapter(),
        common_adapter: CommonAdapters = CommonAdapters(),
        manager: LeagueTeamManager = LeagueTeamManager(),
    ) -> None:
        self.adapter = adapter
        self.common_adapter = common_adapter
        self.manager = manager

    def create(
        self, inbound_model: LeagueTeamInboundCreateModel, headers: Headers
    ) -> LeagueTeamOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        model: LeagueTeamCreateModel = (
            self.adapter.convert_from_inbound_create_model_to_create_model(
                inbound_model
            )
        )

        result = self.manager.create_league_team(model, request_operators)

        if result is None:
            raise Exception("Received no model from create operation.")

        response_model: LeagueTeamOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model

    def get_by_id(self, id: UUID, headers: Headers) -> LeagueTeamOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        result = self.manager.get_league_team_by_id(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"LeagueTeam with id {id} not found.",
            )

        response_model: LeagueTeamOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model

    def search(
        self, inbound_model: LeagueTeamInboundSearchModel, headers: Headers
    ) -> OutboundItemListResponse[LeagueTeamOutboundModel]:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        paging_model: PagingModel = (
            self.common_adapter.convert_from_paged_inbound_model_to_paging_model(
                inbound_model
            )
        )

        search_model: LeagueTeamSearchModel = (
            self.adapter.convert_from_inbound_search_model_to_search_model(
                inbound_model
            )
        )

        results: ItemList[LeagueTeamModel] = self.manager.search_league_teams(
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
        inbound_model: LeagueTeamInboundUpdateModel,
        headers: Headers,
    ):
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        model: LeagueTeamUpdateModel = (
            self.adapter.convert_from_inbound_update_model_to_update_model(
                inbound_model
            )
        )

        result: None | LeagueTeamModel = self.manager.update_league_team(
            id, model, request_operators
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"LeagueTeam with id {id} not found.",
            )

        response_model: LeagueTeamOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model

    def delete(self, id: UUID, headers: Headers) -> LeagueTeamOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        result = self.manager.delete_league_team(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"LeagueTeam with id {id} not found.",
            )

        response_model: LeagueTeamOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model
