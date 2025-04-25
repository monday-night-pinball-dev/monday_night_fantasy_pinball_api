from uuid import UUID
from fastapi import HTTPException
from fastapi.datastructures import Headers
from adapters.fantasy_team_season_link_adapters import FantasyTeamSeasonLinkAdapter
from adapters.common_adapters import CommonAdapters
from managers.fantasy_team_season_link_manager import FantasyTeamSeasonLinkManager
from models.fantasy_team_season_link_model import (
    FantasyTeamSeasonLinkCreateModel,
    FantasyTeamSeasonLinkInboundCreateModel,
    FantasyTeamSeasonLinkInboundSearchModel,
    FantasyTeamSeasonLinkModel,
    FantasyTeamSeasonLinkOutboundModel,
    FantasyTeamSeasonLinkSearchModel,
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)
from util.database import PagingModel


class FantasyTeamSeasonLinkController:
    def __init__(
        self,
        adapter: FantasyTeamSeasonLinkAdapter = FantasyTeamSeasonLinkAdapter(),
        common_adapter: CommonAdapters = CommonAdapters(),
        manager: FantasyTeamSeasonLinkManager = FantasyTeamSeasonLinkManager(),
    ) -> None:
        self.adapter = adapter
        self.common_adapter = common_adapter
        self.manager = manager

    def create(
        self,
        inbound_model: FantasyTeamSeasonLinkInboundCreateModel,
        headers: dict[str, str],
    ) -> FantasyTeamSeasonLinkOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        model: FantasyTeamSeasonLinkCreateModel = (
            self.adapter.convert_from_inbound_create_model_to_create_model(
                inbound_model
            )
        )

        result = self.manager.create_fantasy_team_season_link(model, request_operators)

        if result is None:
            raise Exception("Received no model from create operation.")

        response_model: FantasyTeamSeasonLinkOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model

    def get_by_id(
        self, id: UUID, headers: dict[str, str]
    ) -> FantasyTeamSeasonLinkOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        result = self.manager.get_fantasy_team_season_link_by_id(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404, detail=f"FantasyTeamSeasonLink with id {id} not found."
            )

        response_model: FantasyTeamSeasonLinkOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model

    def search(
        self,
        inbound_model: FantasyTeamSeasonLinkInboundSearchModel,
        headers: dict[str, str],
    ) -> OutboundItemListResponse[FantasyTeamSeasonLinkOutboundModel]:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        paging_model: PagingModel = (
            self.common_adapter.convert_from_paged_inbound_model_to_paging_model(
                inbound_model
            )
        )

        search_model: FantasyTeamSeasonLinkSearchModel = (
            self.adapter.convert_from_inbound_search_model_to_search_model(
                inbound_model
            )
        )

        results: ItemList[FantasyTeamSeasonLinkModel] = (
            self.manager.search_fantasy_team_season_links(
                search_model, paging_model, request_operators
            )
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

    def delete(
        self, id: UUID, headers: dict[str, str]
    ) -> FantasyTeamSeasonLinkOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        result = self.manager.delete_fantasy_team_season_link(id, request_operators)

        if result is None:
            raise HTTPException(
                status_code=404, detail=f"FantasyTeamSeasonLink with id {id} not found."
            )

        response_model: FantasyTeamSeasonLinkOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model
