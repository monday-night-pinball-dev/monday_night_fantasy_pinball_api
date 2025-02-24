from typing import Any
from adapters.league_player_adapters import LeaguePlayerAdapter
from models.user_model import (
    UserCreateModel,
    UserInboundCreateModel,
    UserInboundSearchModel,
    UserInboundUpdateModel,
    UserModel,
    UserOutboundModel,
    UserSearchModel,
    UserUpdateModel,
)
from util.common import CommonUtilities
from util.database import (
    ExactMatchSearchTerm,
    InListSearchTerm,
    LikeComparatorModes,
    LikeSearchTerm,
    SearchTerm,
)


class UserAdapter:
    def __init__(
        self,
        common_utilities: CommonUtilities = CommonUtilities(),
        league_player_adapter: LeaguePlayerAdapter = LeaguePlayerAdapter(),
    ) -> None:
        self.common_utilities = common_utilities
        self.league_player_adapter = league_player_adapter

    def convert_from_inbound_create_model_to_create_model(
        self,
        inbound_create_model: UserInboundCreateModel,
    ) -> UserCreateModel:
        model = UserCreateModel(
            name=inbound_create_model.name,
            username=inbound_create_model.username,
            role=inbound_create_model.role,
            league_player_id=inbound_create_model.league_player_id,
        )

        return model

    def convert_from_inbound_update_model_to_update_model(
        self,
        inbound_update_model: UserInboundUpdateModel,
    ) -> UserUpdateModel:
        model = UserUpdateModel(
            name=inbound_update_model.name,
            role=inbound_update_model.role,
        )

        return model

    def convert_from_inbound_search_model_to_search_model(
        self, inbound_search_model: UserInboundSearchModel
    ) -> UserSearchModel:
        model = UserSearchModel(
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
            role=inbound_search_model.role,
            name=inbound_search_model.name,
            name_like=inbound_search_model.name_like,
            username_like=inbound_search_model.username_like,
            username=inbound_search_model.username,
        )

        return model

    def convert_from_search_model_to_search_terms(
        self, model: UserSearchModel
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

        if model.role is not None:
            search_terms.append(ExactMatchSearchTerm("role", model.role.value, True))

        if model.name_like is not None:
            search_terms.append(
                LikeSearchTerm("name", model.name_like, LikeComparatorModes.Like, True)
            )

        if model.name is not None:
            search_terms.append(ExactMatchSearchTerm("name", model.name))

        if model.username is not None:
            search_terms.append(ExactMatchSearchTerm("username", model.username, True))

        if model.username_like is not None:
            search_terms.append(
                LikeSearchTerm(
                    "username", model.username_like, LikeComparatorModes.Like, True
                )
            )

        return search_terms

    def convert_from_create_model_to_database_model(
        self, model: UserCreateModel
    ) -> dict[str, Any]:
        database_model: dict[str, Any] = {
            "name": model.name,
            "username": model.username,
            "role": model.role.value if model.role is not None else None,
            "league_player_id": str(model.league_player_id)
            if model.league_player_id is not None
            else None,
        }

        return database_model

    def convert_from_update_model_to_database_model(
        self, model: UserUpdateModel
    ) -> dict[str, Any]:
        database_model: dict[str, Any] = {
            "name": model.name,
            "role": model.role.value if model.role is not None else None,
        }

        return database_model

    def convert_from_database_model_to_model(
        self, database_model: dict[str, Any]
    ) -> UserModel:
        model = UserModel(
            id=database_model["id"],
            name=database_model["name"],
            role=database_model["role"],
            username=database_model["username"],
            league_player_id=database_model["league_player_id"],
            created_at=database_model["created_at"],
            updated_at=database_model["updated_at"],
        )

        return model

    def convert_from_model_to_outbound_model(
        self, model: UserModel
    ) -> UserOutboundModel:
        outbound_model = UserOutboundModel(
            id=model.id,
            name=model.name,
            username=model.username,
            role=model.role,
            league_player_id=model.league_player_id,
            league_player=self.league_player_adapter.convert_from_model_to_outbound_model(
                model.league_player
            )
            if model.league_player is not None
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
