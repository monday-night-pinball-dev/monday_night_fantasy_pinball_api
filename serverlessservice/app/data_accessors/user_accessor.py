from typing import Any
from uuid import UUID
from adapters.user_adapters import UserAdapter
from models.user_model import (
    UserCreateModel,
    UserModel,
    UserSearchModel,
    UserUpdateModel,
)
from models.common_model import ItemList
from util.common import RequestOperators
from util.configuration import get_global_configuration
from util.database import PagingModel, SearchTerm
from util.db_connection import SelectQueryResults


class UserAccessor:
    def __init__(
        self,
        adapter: UserAdapter = UserAdapter(),
    ) -> None:
        self.adapter = adapter

    def insert(
        self,
        model: UserCreateModel,
        request_operators: RequestOperators | None = None,
    ) -> UserModel:
        connection = get_global_configuration().pg_connection

        db_model: dict[str, Any] = (
            self.adapter.convert_from_create_model_to_database_model(model)
        )

        db_result: dict[str, Any] = connection.insert(
            "users", db_model, request_operators
        )

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def select_by_id(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> UserModel:
        connection = get_global_configuration().pg_connection

        db_result = connection.select_by_id("users", id, request_operators)

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def select(
        self,
        model: UserSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None,
    ) -> ItemList[UserModel]:
        connection = get_global_configuration().pg_connection

        search_terms: list[SearchTerm] = (
            self.adapter.convert_from_search_model_to_search_terms(model)
        )

        db_result: SelectQueryResults = connection.select(
            "users", search_terms, paging_model, request_operators
        )

        results: ItemList[UserModel] = ItemList[UserModel](db_result.paging)

        if db_result is None:
            return results

        for item in db_result.items:
            result_model = self.adapter.convert_from_database_model_to_model(item)
            results.items.append(result_model)

        return results

    def update(
        self,
        id: UUID,
        model: UserUpdateModel,
        request_operators: RequestOperators | None = None,
    ) -> UserModel:
        connection = get_global_configuration().pg_connection

        db_model: dict[str, Any] = (
            self.adapter.convert_from_update_model_to_database_model(model)
        )

        db_result = connection.update("users", id, db_model, request_operators)

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model

    def delete(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> UserModel:
        connection = get_global_configuration().pg_connection

        db_result = connection.delete("users", id, request_operators)

        if db_result is None:
            return None

        result_model = self.adapter.convert_from_database_model_to_model(db_result)

        return result_model
