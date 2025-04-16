from typing import Any
from adapters.venue_adapters import VenueAdapter
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
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm,
    LikeComparatorModes,
    LikeSearchTerm,
    SearchTerm,
)


class LeagueTeamAdapter:
    def __init__(
        self,
        venue_adapter: VenueAdapter = VenueAdapter(),
        common_utilities: CommonUtilities = CommonUtilities(),
    ) -> None:
        self.venue_adapter = venue_adapter
        self.common_utilities = common_utilities

    def convert_from_inbound_create_model_to_create_model(
        self, inbound_create_model: LeagueTeamInboundCreateModel
    ) -> LeagueTeamCreateModel:
        model = LeagueTeamCreateModel(
            name=inbound_create_model.name,
            home_venue_id=inbound_create_model.home_venue_id,
            global_mnp_id=inbound_create_model.global_mnp_id,
            short_name=inbound_create_model.short_name,
        )

        return model

    def convert_from_inbound_update_model_to_update_model(
        self, inbound_update_model: LeagueTeamInboundUpdateModel
    ) -> LeagueTeamUpdateModel:
        model = LeagueTeamUpdateModel(
            name=inbound_update_model.name,
            home_venue_id=inbound_update_model.home_venue_id,
            short_name=inbound_update_model.short_name,
        )

        return model

    def convert_from_inbound_search_model_to_search_model(
        self, inbound_search_model: LeagueTeamInboundSearchModel
    ) -> LeagueTeamSearchModel:
        model = LeagueTeamSearchModel(
            ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.ids
                )
                if inbound_search_model.ids is not None
                else None
            ),
            home_venue_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.home_venue_ids
                )
                if inbound_search_model.home_venue_ids is not None
                else None
            ),
            global_mnp_ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.global_mnp_ids
                )
                if inbound_search_model.global_mnp_ids is not None
                else None
            ),
            name=inbound_search_model.name,
            name_like=inbound_search_model.name_like,
            short_name=inbound_search_model.short_name,
        )

        return model

    def convert_from_search_model_to_search_terms(
        self, model: LeagueTeamSearchModel
    ) -> list[SearchTerm]:
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(
                InListSearchTerm(
                    "id",
                    self.common_utilities.convert_uuid_list_to_string_list(model.ids),
                )
            )

        if model.home_venue_ids is not None:
            search_terms.append(
                InListSearchTerm(
                    "home_venue_id",
                    self.common_utilities.convert_uuid_list_to_string_list(
                        model.home_venue_ids
                    ),
                )
            )

        if model.global_mnp_ids is not None:
            search_terms.append(
                InListSearchTerm(
                    "global_mnp_id",
                    self.common_utilities.convert_uuid_list_to_string_list(
                        model.global_mnp_ids
                    ),
                )
            )

        if model.name is not None:
            search_terms.append(ExactMatchSearchTerm("name", model.name, True))

        if model.name_like is not None:
            search_terms.append(
                LikeSearchTerm("name", model.name_like, LikeComparatorModes.Like, True)
            )

        if model.short_name is not None:
            search_terms.append(
                ExactMatchSearchTerm("short_name", model.short_name, True)
            )

        return search_terms

    def convert_from_create_model_to_database_model(
        self, model: LeagueTeamCreateModel
    ) -> dict[str, Any]:
        database_model: dict[str, Any] = {
            "name": model.name,
            "home_venue_id": str(model.home_venue_id)
            if model.home_venue_id is not None
            else None,
            "global_mnp_id": str(model.global_mnp_id)
            if model.global_mnp_id is not None
            else None,
            "short_name": model.short_name,
        }

        return database_model

    def convert_from_update_model_to_database_model(
        self, model: LeagueTeamUpdateModel
    ) -> dict[str, Any]:
        database_model: dict[str, Any] = {
            "name": model.name,
            "home_venue_id": str(model.home_venue_id)
            if model.home_venue_id is not None
            else None,
            "short_name": model.short_name,
        }

        return database_model

    def convert_from_database_model_to_model(
        self, database_model: dict[str, Any]
    ) -> LeagueTeamModel:
        model = LeagueTeamModel(
            id=database_model["id"],
            name=database_model["name"],
            home_venue_id=database_model["home_venue_id"],
            global_mnp_id=database_model["global_mnp_id"],
            short_name=database_model["short_name"],
            created_at=database_model["created_at"],
            updated_at=database_model["updated_at"],
        )

        return model

    def convert_from_model_to_outbound_model(
        self, model: LeagueTeamModel
    ) -> LeagueTeamOutboundModel:
        outbound_model = LeagueTeamOutboundModel(
            id=model.id,
            home_venue_id=model.home_venue_id,
            global_mnp_id=model.global_mnp_id,
            home_venue=self.venue_adapter.convert_from_model_to_outbound_model(
                model.home_venue
            )
            if model.home_venue is not None
            else None,
            name=model.name,
            short_name=model.short_name,
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
