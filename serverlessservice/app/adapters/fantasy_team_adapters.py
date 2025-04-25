from typing import Any
from models.fantasy_team_model import (
    FantasyTeamCreateModel,
    FantasyTeamInboundCreateModel,
    FantasyTeamInboundSearchModel,
    FantasyTeamInboundUpdateModel,
    FantasyTeamModel,
    FantasyTeamOutboundModel,
    FantasyTeamSearchModel,
    FantasyTeamUpdateModel,
)
from adapters.fantasy_league_adapters import FantasyLeagueAdapter
from adapters.user_adapters import UserAdapter
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm,
    LikeComparatorModes,
    LikeSearchTerm,
    SearchTerm,
)


class FantasyTeamAdapter:
    def __init__(
        self,
        fantasy_league_adapter: FantasyLeagueAdapter = FantasyLeagueAdapter(),
        user_adapter: UserAdapter = UserAdapter(),
        common_utilities: CommonUtilities = CommonUtilities(),
    ) -> None:
        self.common_utilities = common_utilities
        self.fantasy_league_adapter = fantasy_league_adapter
        self.user_adapter = user_adapter

    def convert_from_inbound_create_model_to_create_model(
        self, inbound_create_model: FantasyTeamInboundCreateModel
    ) -> FantasyTeamCreateModel:
        model = FantasyTeamCreateModel(
            name=inbound_create_model.name,
            owner_id=inbound_create_model.owner_id,
            fantasy_league_id=inbound_create_model.fantasy_league_id,
        )

        return model

    def convert_from_inbound_update_model_to_update_model(
        self, inbound_update_model: FantasyTeamInboundUpdateModel
    ) -> FantasyTeamUpdateModel:
        model = FantasyTeamUpdateModel(
            name=inbound_update_model.name,
            owner_id=inbound_update_model.owner_id,
        )

        return model

    def convert_from_inbound_search_model_to_search_model(
        self, inbound_search_model: FantasyTeamInboundSearchModel
    ) -> FantasyTeamSearchModel:
        model = FantasyTeamSearchModel(
            ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.ids
                )
                if inbound_search_model.ids is not None
                else None
            ),
            owner_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.owner_ids
                )
                if inbound_search_model.owner_ids is not None
                else None
            ),
            fantasy_league_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.fantasy_league_ids
                )
                if inbound_search_model.fantasy_league_ids is not None
                else None
            ),
            name=inbound_search_model.name,
            name_like=inbound_search_model.name_like,
        )

        return model

    def convert_from_search_model_to_search_terms(
        self, model: FantasyTeamSearchModel
    ) -> list[SearchTerm]:
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(
                InListSearchTerm(
                    "id",
                    self.common_utilities.convert_uuid_list_to_string_list(model.ids),
                )
            )
        if model.owner_ids is not None:
            search_terms.append(
                InListSearchTerm(
                    "owner_id",
                    self.common_utilities.convert_uuid_list_to_string_list(
                        model.owner_ids
                    ),
                )
            )
        if model.fantasy_league_ids is not None:
            search_terms.append(
                InListSearchTerm(
                    "fantasy_league_id",
                    self.common_utilities.convert_uuid_list_to_string_list(
                        model.fantasy_league_ids
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
        self, model: FantasyTeamCreateModel
    ) -> dict[str, Any]:
        database_model: dict[str, Any] = {
            "name": model.name,
            "owner_id": str(model.owner_id),
            "fantasy_league_id": str(model.fantasy_league_id),
        }

        return database_model

    def convert_from_update_model_to_database_model(
        self, model: FantasyTeamUpdateModel
    ) -> dict[str, Any]:
        database_model: dict[str, Any] = {
            "name": model.name,
            "owner_id": str(model.owner_id) if model.owner_id is not None else None,
        }

        return database_model

    def convert_from_database_model_to_model(
        self, database_model: dict[str, Any]
    ) -> FantasyTeamModel:
        model = FantasyTeamModel(
            id=database_model["id"],
            name=database_model["name"],
            fantasy_league_id=database_model["fantasy_league_id"],
            owner_id=database_model["owner_id"],
            created_at=database_model["created_at"],
            updated_at=database_model["updated_at"],
        )

        return model

    def convert_from_model_to_outbound_model(
        self, model: FantasyTeamModel
    ) -> FantasyTeamOutboundModel:
        outbound_model = FantasyTeamOutboundModel(
            id=model.id,
            fantasy_league_id=model.fantasy_league_id,
            fantasy_league=self.fantasy_league_adapter.convert_from_model_to_outbound_model(
                model.fantasy_league
            )
            if model.fantasy_league is not None
            else None,
            owner_id=model.owner_id,
            owner=self.user_adapter.convert_from_model_to_outbound_model(model.owner)
            if model.owner is not None
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
