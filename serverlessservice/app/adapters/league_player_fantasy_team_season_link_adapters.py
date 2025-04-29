from typing import Any
from uuid import UUID
from adapters.fantasy_league_adapters import FantasyLeagueAdapter
from adapters.fantasy_team_adapters import FantasyTeamAdapter
from adapters.fantasy_team_season_link_adapters import FantasyTeamSeasonLinkAdapter
from adapters.league_player_adapters import LeaguePlayerAdapter
from adapters.league_team_adapters import LeagueTeamAdapter
from adapters.season_adapters import SeasonAdapter
from adapters.user_adapters import UserAdapter
from models.league_player_fantasy_team_season_link_model import (
    LeaguePlayerFantasyTeamSeasonLinkCreateModel,
    LeaguePlayerFantasyTeamSeasonLinkInboundCreateModel,
    LeaguePlayerFantasyTeamSeasonLinkInboundSearchModel,
    LeaguePlayerFantasyTeamSeasonLinkModel,
    LeaguePlayerFantasyTeamSeasonLinkOutboundModel,
    LeaguePlayerFantasyTeamSeasonLinkSearchModel,
)
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm,
    SearchTerm,
)


class LeaguePlayerFantasyTeamSeasonLinkAdapter:
    def __init__(
        self,
        league_player_adapter: LeaguePlayerAdapter = LeaguePlayerAdapter(),
        league_team_adapter: LeagueTeamAdapter = LeagueTeamAdapter(),
        fantasy_team_season_link_adapter: FantasyTeamSeasonLinkAdapter = FantasyTeamSeasonLinkAdapter(),
        season_adapter: SeasonAdapter = SeasonAdapter(),
        fantasy_team_adapter: FantasyTeamAdapter = FantasyTeamAdapter(),
        fantasy_team_owner_adapter: UserAdapter = UserAdapter(),
        fantasy_league_adapter: FantasyLeagueAdapter = FantasyLeagueAdapter(),
        common_utilities: CommonUtilities = CommonUtilities(),
    ) -> None:
        self.common_utilities = common_utilities
        self.league_player_adapter = league_player_adapter
        self.league_team_adapter = league_team_adapter
        self.fantasy_team_season_link_adapter = fantasy_team_season_link_adapter
        self.season_adapter = season_adapter
        self.fantasy_team_adapter = fantasy_team_adapter
        self.fantasy_team_owner_adapter = fantasy_team_owner_adapter
        self.fantasy_league_adapter = fantasy_league_adapter

    def convert_from_inbound_create_model_to_create_model(
        self, inbound_create_model: LeaguePlayerFantasyTeamSeasonLinkInboundCreateModel
    ) -> LeaguePlayerFantasyTeamSeasonLinkCreateModel:
        model = LeaguePlayerFantasyTeamSeasonLinkCreateModel(
            league_player_id=inbound_create_model.league_player_id,
            fantasy_team_season_link_id=inbound_create_model.fantasy_team_season_link_id,
        )
        return model

    def convert_from_inbound_search_model_to_search_model(
        self, inbound_search_model: LeaguePlayerFantasyTeamSeasonLinkInboundSearchModel
    ) -> LeaguePlayerFantasyTeamSeasonLinkSearchModel:
        model = LeaguePlayerFantasyTeamSeasonLinkSearchModel(
            ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.ids
                )
                if inbound_search_model.ids is not None
                else None
            ),
            league_player_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.league_player_ids
                )
                if inbound_search_model.league_player_ids is not None
                else None
            ),
            league_team_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.league_team_ids
                )
                if inbound_search_model.league_team_ids is not None
                else None
            ),
            fantasy_team_season_link_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.fantasy_team_season_link_ids
                )
                if inbound_search_model.fantasy_team_season_link_ids is not None
                else None
            ),
            season_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.season_ids
                )
                if inbound_search_model.season_ids is not None
                else None
            ),
            fantasy_team_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.fantasy_team_ids
                )
                if inbound_search_model.fantasy_team_ids is not None
                else None
            ),
            fantasy_team_owner_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.fantasy_team_owner_ids
                )
                if inbound_search_model.fantasy_team_owner_ids is not None
                else None
            ),
            fantasy_league_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.fantasy_league_ids
                )
                if inbound_search_model.fantasy_league_ids is not None
                else None
            ),
        )
        return model

    def convert_from_search_model_to_search_terms(
        self, model: LeaguePlayerFantasyTeamSeasonLinkSearchModel
    ) -> list[SearchTerm]:
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(
                InListSearchTerm(
                    "id",
                    self.common_utilities.convert_uuid_list_to_string_list(model.ids),
                )
            )
        if model.league_player_ids is not None:
            search_terms.append(
                InListSearchTerm(
                    "league_player_id",
                    self.common_utilities.convert_uuid_list_to_string_list(
                        model.league_player_ids
                    ),
                )
            )
        if model.league_team_ids is not None:
            search_terms.append(
                InListSearchTerm(
                    "league_team_id_dn",
                    self.common_utilities.convert_uuid_list_to_string_list(
                        model.league_team_ids
                    ),
                )
            )

        if model.fantasy_team_season_link_ids is not None:
            search_terms.append(
                InListSearchTerm(
                    "fantasy_team_season_link_id",
                    self.common_utilities.convert_uuid_list_to_string_list(
                        model.fantasy_team_season_link_ids
                    ),
                )
            )

        if model.season_ids is not None:
            search_terms.append(
                InListSearchTerm(
                    "season_id_dn",
                    self.common_utilities.convert_uuid_list_to_string_list(
                        model.season_ids
                    ),
                )
            )

        if model.fantasy_team_ids is not None:
            search_terms.append(
                InListSearchTerm(
                    "fantasy_team_id_dn",
                    self.common_utilities.convert_uuid_list_to_string_list(
                        model.fantasy_team_ids
                    ),
                )
            )

        if model.fantasy_team_owner_ids is not None:
            search_terms.append(
                InListSearchTerm(
                    "fantasy_team_owner_id_dn",
                    self.common_utilities.convert_uuid_list_to_string_list(
                        model.fantasy_team_owner_ids
                    ),
                )
            )

        if model.fantasy_league_ids is not None:
            search_terms.append(
                InListSearchTerm(
                    "fantasy_league_id_dn",
                    self.common_utilities.convert_uuid_list_to_string_list(
                        model.fantasy_league_ids
                    ),
                )
            )

        return search_terms

    def convert_from_create_model_to_database_model(
        self, model: LeaguePlayerFantasyTeamSeasonLinkCreateModel
    ) -> dict[str, Any]:
        database_model: dict[str, Any] = {
            "league_player_id": str(model.league_player_id)
            if model.league_player_id
            else None,
            "league_team_id_dn": str(model.league_team_id)
            if model.league_team_id
            else None,
            "fantasy_team_season_link_id": str(model.fantasy_team_season_link_id)
            if model.fantasy_team_season_link_id
            else None,
            "season_id_dn": str(model.season_id) if model.season_id else None,
            "fantasy_team_id_dn": str(model.fantasy_team_id)
            if model.fantasy_team_id
            else None,
            "fantasy_team_owner_id_dn": str(model.fantasy_team_owner_id)
            if model.fantasy_team_owner_id
            else None,
            "fantasy_league_id_dn": str(model.fantasy_league_id)
            if model.fantasy_league_id
            else None,
        }
        return database_model

    def convert_from_database_model_to_model(
        self, database_model: dict[str, Any]
    ) -> LeaguePlayerFantasyTeamSeasonLinkModel:
        model = LeaguePlayerFantasyTeamSeasonLinkModel(
            id=UUID(database_model["id"]),
            league_player_id=UUID(database_model["league_player_id"]),
            league_team_id=UUID(database_model["league_team_id_dn"])
            if database_model.get("league_team_id_dn") is not None
            else None,
            fantasy_team_season_link_id=UUID(
                database_model["fantasy_team_season_link_id"]
            ),
            season_id=UUID(database_model["season_id_dn"]),
            fantasy_team_id=UUID(database_model["fantasy_team_id_dn"]),
            fantasy_team_owner_id=UUID(database_model["fantasy_team_owner_id_dn"]),
            fantasy_league_id=UUID(database_model["fantasy_league_id_dn"]),
            created_at=database_model["created_at"],
            updated_at=database_model["updated_at"],
        )
        return model

    def convert_from_model_to_outbound_model(
        self, model: LeaguePlayerFantasyTeamSeasonLinkModel
    ) -> LeaguePlayerFantasyTeamSeasonLinkOutboundModel:
        outbound_model = LeaguePlayerFantasyTeamSeasonLinkOutboundModel(
            id=model.id,
            league_player_id=model.league_player_id,
            league_player=self.league_player_adapter.convert_from_model_to_outbound_model(
                model.league_player
            )
            if model.league_player is not None
            else None,
            league_team_id=model.league_team_id,
            league_team=self.league_team_adapter.convert_from_model_to_outbound_model(
                model.league_team
            )
            if model.league_team is not None
            else None,
            fantasy_team_season_link_id=model.fantasy_team_season_link_id,
            fantasy_team_season_link=self.fantasy_team_season_link_adapter.convert_from_model_to_outbound_model(
                model.fantasy_team_season_link
            )
            if model.fantasy_team_season_link is not None
            else None,
            season_id=model.season_id,
            season=self.season_adapter.convert_from_model_to_outbound_model(
                model.season
            )
            if model.season is not None
            else None,
            fantasy_team_id=model.fantasy_team_id,
            fantasy_team=self.fantasy_team_adapter.convert_from_model_to_outbound_model(
                model.fantasy_team
            )
            if model.fantasy_team is not None
            else None,
            fantasy_team_owner_id=model.fantasy_team_owner_id,
            fantasy_team_owner=self.fantasy_team_owner_adapter.convert_from_model_to_outbound_model(
                model.fantasy_team_owner
            )
            if model.fantasy_team_owner is not None
            else None,
            fantasy_league_id=model.fantasy_league_id,
            fantasy_league=self.fantasy_league_adapter.convert_from_model_to_outbound_model(
                model.fantasy_league
            )
            if model.fantasy_league is not None
            else None,
            created_at=model.created_at.isoformat(timespec="milliseconds").replace(
                "+00:00", "Z"
            ),
            updated_at=model.updated_at.isoformat(timespec="milliseconds").replace(
                "+00:00", "Z"
            )
            if model.updated_at is not None
            else None,
        )
        return outbound_model
