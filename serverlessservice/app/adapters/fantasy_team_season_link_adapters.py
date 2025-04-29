from typing import Any
from uuid import UUID
from models.fantasy_team_season_link_model import (
    FantasyTeamSeasonLinkCreateModel,
    FantasyTeamSeasonLinkInboundCreateModel,
    FantasyTeamSeasonLinkInboundSearchModel,
    FantasyTeamSeasonLinkModel,
    FantasyTeamSeasonLinkOutboundModel,
    FantasyTeamSeasonLinkSearchModel,
)
from adapters.fantasy_team_adapters import FantasyTeamAdapter
from adapters.season_adapters import SeasonAdapter
from adapters.user_adapters import UserAdapter
from adapters.fantasy_league_adapters import FantasyLeagueAdapter
from util.common import CommonUtilities
from util.database import (
    InListSearchTerm,
    SearchTerm,
)


class FantasyTeamSeasonLinkAdapter:
    def __init__(
        self,
        fantasy_team_adapter: FantasyTeamAdapter = FantasyTeamAdapter(),
        season_adapter: SeasonAdapter = SeasonAdapter(),
        user_adapter: UserAdapter = UserAdapter(),
        fantasy_league_adapter: FantasyLeagueAdapter = FantasyLeagueAdapter(),
        common_utilities: CommonUtilities = CommonUtilities(),
    ) -> None:
        self.fantasy_team_adapter = fantasy_team_adapter
        self.season_adapter = season_adapter
        self.user_adapter = user_adapter
        self.fantasy_league_adapter = fantasy_league_adapter
        self.common_utilities = common_utilities

    def convert_from_inbound_create_model_to_create_model(
        self, inbound_create_model: FantasyTeamSeasonLinkInboundCreateModel
    ) -> FantasyTeamSeasonLinkCreateModel:
        model = FantasyTeamSeasonLinkCreateModel(
            season_id=inbound_create_model.season_id,
            fantasy_team_id=inbound_create_model.fantasy_team_id,
        )
        return model

    def convert_from_inbound_search_model_to_search_model(
        self, inbound_search_model: FantasyTeamSeasonLinkInboundSearchModel
    ) -> FantasyTeamSeasonLinkSearchModel:
        model = FantasyTeamSeasonLinkSearchModel(
            ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.ids
                )
                if inbound_search_model.ids is not None
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
        self, model: FantasyTeamSeasonLinkSearchModel
    ) -> list[SearchTerm]:
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(
                InListSearchTerm(
                    "id",
                    self.common_utilities.convert_uuid_list_to_string_list(model.ids),
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
        self, model: FantasyTeamSeasonLinkCreateModel
    ) -> dict[str, Any]:
        database_model: dict[str, Any] = {
            "season_id": str(model.season_id),
            "fantasy_team_id": str(model.fantasy_team_id),
            "fantasy_team_owner_id_dn": str(model.fantasy_team_owner_id),
            "fantasy_league_id_dn": str(model.fantasy_league_id),
        }
        return database_model

    def convert_from_database_model_to_model(
        self, database_model: dict[str, Any]
    ) -> FantasyTeamSeasonLinkModel:
        model = FantasyTeamSeasonLinkModel(
            id=UUID(database_model["id"]),
            season_id=UUID(database_model["season_id"]),
            fantasy_team_id=UUID(database_model["fantasy_team_id"]),
            fantasy_team_owner_id=UUID(database_model["fantasy_team_owner_id_dn"]),
            fantasy_league_id=UUID(database_model["fantasy_league_id_dn"]),
            created_at=database_model["created_at"],
            updated_at=database_model["updated_at"],
        )
        return model

    def convert_from_model_to_outbound_model(
        self, model: FantasyTeamSeasonLinkModel
    ) -> FantasyTeamSeasonLinkOutboundModel:
        outbound_model = FantasyTeamSeasonLinkOutboundModel(
            id=model.id,
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
            fantasy_team_owner=self.user_adapter.convert_from_model_to_outbound_model(
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
