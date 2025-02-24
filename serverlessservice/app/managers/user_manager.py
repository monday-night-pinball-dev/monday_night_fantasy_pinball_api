from uuid import UUID
from data_accessors.user_accessor import UserAccessor
from models.common_model import ItemList
from models.user_model import (
    UserCreateModel,
    UserModel,
    UserSearchModel,
    UserUpdateModel,
)
from util.common import CommonUtilities, RequestOperators
from util.database import PagingModel


class UserManager:
    def __init__(
        self,
        user_accessor: UserAccessor = UserAccessor(),
        common_utilities: CommonUtilities = CommonUtilities(),
    ) -> None:
        self.user_accessor = user_accessor
        self.common_utilities = common_utilities

    def create_user(
        self,
        inbound_model: UserCreateModel,
        request_operators: RequestOperators | None = None,
    ) -> UserModel | None:
        result = self.user_accessor.insert(
            model=inbound_model, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_users([result], request_operators)

        return result

    def get_user_by_id(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> UserModel | None:
        result = self.user_accessor.select_by_id(
            id=id, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_users([result], request_operators)

        return result

    def search_users(
        self,
        model: UserSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None,
    ) -> ItemList[UserModel]:
        result = self.user_accessor.select(
            model=model, paging_model=paging_model, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_users(result.items, request_operators)

        return result

    def update_user(
        self,
        id: UUID,
        model: UserUpdateModel,
        request_operators: RequestOperators | None = None,
    ) -> UserModel | None:
        result = self.user_accessor.update(id, model, request_operators)

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_users([result], request_operators)

        return result

    def delete_user(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> UserModel | None:
        result: None | UserModel = self.user_accessor.delete(
            id=id, request_operators=request_operators
        )

        return result
