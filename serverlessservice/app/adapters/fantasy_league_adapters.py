from typing import Any

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
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm,
    LikeComparatorModes,
    LikeSearchTerm,
    SearchTerm,
)


class FantasyLeagueAdapter:
    def __init__(self, common_utilities: CommonUtilities = CommonUtilities()) -> None:
        self.common_utilities = common_utilities

    def convert_from_inbound_create_model_to_create_model(
        self,
        inbound_create_model: FantasyLeagueInboundCreateModel,
    ) -> FantasyLeagueCreateModel:
        model = FantasyLeagueCreateModel(
            name=inbound_create_model.name,
        )

        return model

    def convert_from_inbound_update_model_to_update_model(
        self, inbound_update_model: FantasyLeagueInboundUpdateModel
    ) -> FantasyLeagueUpdateModel:
        model = FantasyLeagueUpdateModel(
            name=inbound_update_model.name,
        )

        return model

    def convert_from_inbound_search_model_to_search_model(
        self, inbound_search_model: FantasyLeagueInboundSearchModel
    ) -> FantasyLeagueSearchModel:
        model = FantasyLeagueSearchModel(
            ids=(
                self.common_utilities.convert_comma_delimited_ids_to_uuid_list(
                    inbound_search_model.ids
                )
                if inbound_search_model.ids is not None
                else None
            ),
            name=inbound_search_model.name,
            name_like=inbound_search_model.name_like,
        )

        return model

    def convert_from_search_model_to_search_terms(
        self, model: FantasyLeagueSearchModel
    ) -> list[SearchTerm]:
        search_terms: list[SearchTerm] = []

        if model.ids is not None:
            search_terms.append(
                InListSearchTerm(
                    "id",
                    self.common_utilities.convert_uuid_list_to_string_list(model.ids),
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
        self, model: FantasyLeagueCreateModel
    ) -> dict[str, Any]:
        database_model: dict[str, Any] = {
            "name": model.name,
        }

        return database_model

    def convert_from_update_model_to_database_model(
        self, model: FantasyLeagueUpdateModel
    ) -> dict[str, Any]:
        database_model: dict[str, Any] = {
            "name": model.name,
        }

        return database_model

    def convert_from_database_model_to_model(
        self, database_model: dict[str, Any]
    ) -> FantasyLeagueModel:
        model = FantasyLeagueModel(
            id=database_model["id"],
            name=database_model["name"],
            created_at=database_model["created_at"],
            updated_at=database_model["updated_at"],
        )

        return model

    def convert_from_model_to_outbound_model(
        self, model: FantasyLeagueModel
    ) -> FantasyLeagueOutboundModel:
        outbound_model = FantasyLeagueOutboundModel(
            id=model.id,
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
