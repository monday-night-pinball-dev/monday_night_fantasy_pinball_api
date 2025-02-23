from typing import Any
from adapters.league_team_adapters import LeagueTeamAdapter
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
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm,
    LikeComparatorModes,
    LikeSearchTerm,
    SearchTerm,
)


class LeaguePlayerAdapter:
    def __init__(
        self,
        league_team_adapter: LeagueTeamAdapter = LeagueTeamAdapter(),
        common_utilities: CommonUtilities = CommonUtilities(),
    ) -> None:
        self.league_team_adapter = league_team_adapter
        self.common_utilities = common_utilities

    def convert_from_inbound_create_model_to_create_model(
        self, inbound_create_model: LeaguePlayerInboundCreateModel
    ) -> LeaguePlayerCreateModel:
        model = LeaguePlayerCreateModel(
            name=inbound_create_model.name,
            league_team_id=inbound_create_model.league_team_id,
        )

        return model

    def convert_from_inbound_update_model_to_update_model(
        self, inbound_update_model: LeaguePlayerInboundUpdateModel
    ) -> LeaguePlayerUpdateModel:
        model = LeaguePlayerUpdateModel(
            name=inbound_update_model.name,
            league_team_id=inbound_update_model.league_team_id,
        )

        return model

    def convert_from_inbound_search_model_to_search_model(
        self, inbound_search_model: LeaguePlayerInboundSearchModel
    ) -> LeaguePlayerSearchModel:
        model = LeaguePlayerSearchModel(
            ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.ids
                )
                if inbound_search_model.ids is not None
                else None
            ),
            league_team_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.league_team_ids
                )
                if inbound_search_model.league_team_ids is not None
                else None
            ),
            name=inbound_search_model.name,
            name_like=inbound_search_model.name_like,
        )

        return model

    def convert_from_search_model_to_search_terms(
        self, model: LeaguePlayerSearchModel
    ) -> list[SearchTerm]:
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(
                InListSearchTerm(
                    "id",
                    self.common_utilities.convert_uuid_list_to_string_list(model.ids),
                )
            )

        if model.league_team_ids is not None:
            search_terms.append(
                InListSearchTerm(
                    "league_team_id",
                    self.common_utilities.convert_uuid_list_to_string_list(
                        model.league_team_ids
                    ),
                )
            )

        if model.name is not None:
            search_terms.append(ExactMatchSearchTerm("name", model.name, True))

        if model.name_like is not None:
            search_terms.append(
                LikeSearchTerm("name", model.name_like, LikeComparatorModes.Like, True)
            )

        return search_terms

    def convert_from_create_model_to_database_model(
        self, model: LeaguePlayerCreateModel
    ) -> dict[str, Any]:
        database_model: dict[str, Any] = {
            "name": model.name,
            "league_team_id": str(model.league_team_id)
            if model.league_team_id is not None
            else None,
        }

        return database_model

    def convert_from_update_model_to_database_model(
        self, model: LeaguePlayerUpdateModel
    ) -> dict[str, Any]:
        database_model: dict[str, Any] = {
            "name": model.name,
            "league_team_id": str(model.league_team_id)
            if model.league_team_id is not None
            else None,
        }

        return database_model

    def convert_from_database_model_to_model(
        self, database_model: dict[str, Any]
    ) -> LeaguePlayerModel:
        model = LeaguePlayerModel(
            id=database_model["id"],
            name=database_model["name"],
            league_team_id=database_model["league_team_id"],
            created_at=database_model["created_at"],
            updated_at=database_model["updated_at"],
        )

        return model

    def convert_from_model_to_outbound_model(
        self, model: LeaguePlayerModel
    ) -> LeaguePlayerOutboundModel:
        outbound_model = LeaguePlayerOutboundModel(
            id=model.id,
            league_team_id=model.league_team_id,
            league_team=self.league_team_adapter.convert_from_model_to_outbound_model(
                model.league_team
            )
            if model.league_team is not None
            else None,
            name=model.name,
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
