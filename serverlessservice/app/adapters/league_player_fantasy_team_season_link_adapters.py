from typing import Any
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
    def __init__(self, common_utilities: CommonUtilities = CommonUtilities()) -> None:
        self.common_utilities = common_utilities

    def convert_from_inbound_create_model_to_create_model(
        self, inbound_create_model: LeaguePlayerFantasyTeamSeasonLinkInboundCreateModel
    ) -> LeaguePlayerFantasyTeamSeasonLinkCreateModel:
        model = LeaguePlayerFantasyTeamSeasonLinkCreateModel(
            fantasy_team_season_link_id=inbound_create_model.fantasy_team_season_link_id,
            season_id=inbound_create_model.season_id,
            fantasy_team_id=inbound_create_model.fantasy_team_id,
            fantasy_team_owner_id=inbound_create_model.fantasy_team_owner_id,
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
                    "season_id",
                    self.common_utilities.convert_uuid_list_to_string_list(
                        model.season_ids
                    ),
                )
            )

        if model.fantasy_team_ids is not None:
            search_terms.append(
                InListSearchTerm(
                    "fantasy_team_id",
                    self.common_utilities.convert_uuid_list_to_string_list(
                        model.fantasy_team_ids
                    ),
                )
            )

        if model.fantasy_team_owner_ids is not None:
            search_terms.append(
                InListSearchTerm(
                    "fantasy_team_owner_id",
                    self.common_utilities.convert_uuid_list_to_string_list(
                        model.fantasy_team_owner_ids
                    ),
                )
            )

        return search_terms

    def convert_from_create_model_to_database_model(
        self, model: LeaguePlayerFantasyTeamSeasonLinkCreateModel
    ) -> dict[str, Any]:
        database_model: dict[str, Any] = {
            "fantasy_team_season_link_id": model.fantasy_team_season_link_id,
            "season_id": model.season_id,
            "fantasy_team_id": model.fantasy_team_id,
            "fantasy_team_owner_id": model.fantasy_team_owner_id,
        }
        return database_model

    def convert_from_database_model_to_model(
        self, database_model: dict[str, Any]
    ) -> LeaguePlayerFantasyTeamSeasonLinkModel:
        model = LeaguePlayerFantasyTeamSeasonLinkModel(
            id=database_model["id"],
            fantasy_team_season_link_id=database_model["fantasy_team_season_link_id"],
            season_id=database_model["season_id"],
            fantasy_team_id=database_model["fantasy_team_id"],
            fantasy_team_owner_id=database_model["fantasy_team_owner_id"],
            created_at=database_model["created_at"],
            updated_at=database_model["updated_at"],
        )
        return model

    def convert_from_model_to_outbound_model(
        self, model: LeaguePlayerFantasyTeamSeasonLinkModel
    ) -> LeaguePlayerFantasyTeamSeasonLinkOutboundModel:
        outbound_model = LeaguePlayerFantasyTeamSeasonLinkOutboundModel(
            id=model.id,
            fantasy_team_season_link_id=model.fantasy_team_season_link_id,
            season_id=model.season_id,
            fantasy_team_id=model.fantasy_team_id,
            fantasy_team_owner_id=model.fantasy_team_owner_id,
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
