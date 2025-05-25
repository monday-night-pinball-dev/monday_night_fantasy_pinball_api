from uuid import UUID
from data_accessors.season_accessor import SeasonAccessor
from models.common_model import ItemList
from models.season_model import (
    SeasonCreateModel,
    SeasonModel,
    SeasonSearchModel,
    SeasonUpdateModel,
)
from util.common import CommonUtilities, RequestOperators
from util.database import PagingModel


class SeasonManager:
    def __init__(
        self,
        season_accessor: SeasonAccessor = SeasonAccessor(),
        common_utilities: CommonUtilities = CommonUtilities(),
    ) -> None:
        self.season_accessor = season_accessor
        self.common_utilities = common_utilities

    def create_season(
        self,
        inbound_model: SeasonCreateModel,
        request_operators: RequestOperators | None = None,
    ) -> SeasonModel | None:
        result = self.season_accessor.insert(
            model=inbound_model, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_seasons([result], request_operators)

        return result

    def get_season_by_id(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> SeasonModel | None:
        result = self.season_accessor.select_by_id(
            id=id, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_seasons([result], request_operators)

        return result

    def search_seasons(
        self,
        model: SeasonSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None,
    ) -> ItemList[SeasonModel]:
        result = self.season_accessor.select(
            model=model, paging_model=paging_model, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_seasons(result.items, request_operators)

        return result

    def update_season(
        self,
        id: UUID,
        model: SeasonUpdateModel,
        request_operators: RequestOperators | None = None,
    ) -> SeasonModel | None:
        result = self.season_accessor.update(
            id=id, model=model, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_seasons([result], request_operators)

        return result

    def delete_season(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> SeasonModel | None:
        result: None | SeasonModel = self.season_accessor.delete(
            id=id, request_operators=request_operators
        )

        return result
