from uuid import UUID
from fastapi import HTTPException
from adapters.common_adapters import CommonAdapters
from adapters.league_player_fantasy_team_season_link_adapters import (
    LeaguePlayerFantasyTeamSeasonLinkAdapter,
)
from managers.league_player_fantasy_team_season_link_manager import (
    LeaguePlayerFantasyTeamSeasonLinkManager,
)
from models.common_model import (
    ItemList,
    OutboundItemListResponse,
    OutboundResultantPagingModel,
)
from models.league_player_fantasy_team_season_link_model import (
    LeaguePlayerFantasyTeamSeasonLinkCreateModel,
    LeaguePlayerFantasyTeamSeasonLinkInboundCreateModel,
    LeaguePlayerFantasyTeamSeasonLinkInboundSearchModel,
    LeaguePlayerFantasyTeamSeasonLinkModel,
    LeaguePlayerFantasyTeamSeasonLinkOutboundModel,
    LeaguePlayerFantasyTeamSeasonLinkSearchModel,
)
from util.database import PagingModel


class LeaguePlayerFantasyTeamSeasonLinkController:
    def __init__(
        self,
        adapter: LeaguePlayerFantasyTeamSeasonLinkAdapter = LeaguePlayerFantasyTeamSeasonLinkAdapter(),
        common_adapter: CommonAdapters = CommonAdapters(),
        manager: LeaguePlayerFantasyTeamSeasonLinkManager = LeaguePlayerFantasyTeamSeasonLinkManager(),
    ) -> None:
        self.adapter = adapter
        self.common_adapter = common_adapter
        self.manager = manager

    def create(
        self,
        inbound_model: LeaguePlayerFantasyTeamSeasonLinkInboundCreateModel,
        headers: dict[str, str],
    ) -> LeaguePlayerFantasyTeamSeasonLinkOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        model: LeaguePlayerFantasyTeamSeasonLinkCreateModel = (
            self.adapter.convert_from_inbound_create_model_to_create_model(
                inbound_model
            )
        )

        result = self.manager.create_league_player_fantasy_team_season_link(
            model, request_operators
        )

        if result is None:
            raise Exception("Received no model from create operation.")

        response_model: LeaguePlayerFantasyTeamSeasonLinkOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model

    def get_by_id(
        self, id: UUID, headers: dict[str, str]
    ) -> LeaguePlayerFantasyTeamSeasonLinkOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        result = self.manager.get_league_player_fantasy_team_season_link_by_id(
            id, request_operators
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"LeaguePlayerFantasyTeamSeasonLink with id {id} not found.",
            )

        response_model: LeaguePlayerFantasyTeamSeasonLinkOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model

    def search(
        self,
        inbound_model: LeaguePlayerFantasyTeamSeasonLinkInboundSearchModel,
        headers: dict[str, str],
    ) -> OutboundItemListResponse[LeaguePlayerFantasyTeamSeasonLinkOutboundModel]:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        paging_model: PagingModel = (
            self.common_adapter.convert_from_paged_inbound_model_to_paging_model(
                inbound_model
            )
        )

        search_model: LeaguePlayerFantasyTeamSeasonLinkSearchModel = (
            self.adapter.convert_from_inbound_search_model_to_search_model(
                inbound_model
            )
        )

        results: ItemList[LeaguePlayerFantasyTeamSeasonLinkModel] = (
            self.manager.search_league_player_fantasy_team_season_links(
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
    ) -> LeaguePlayerFantasyTeamSeasonLinkOutboundModel | None:
        request_operators = self.common_adapter.convert_from_headers_to_operators(
            headers
        )

        result = self.manager.delete_league_player_fantasy_team_season_link(
            id, request_operators
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"LeaguePlayerFantasyTeamSeasonLink with id {id} not found.",
            )

        response_model: LeaguePlayerFantasyTeamSeasonLinkOutboundModel = (
            self.adapter.convert_from_model_to_outbound_model(result)
        )

        return response_model
