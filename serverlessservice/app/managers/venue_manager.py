from uuid import UUID
from data_accessors.venue_accessor import VenueAccessor
from models.common_model import ItemList
from models.venue_model import VenueCreateModel, VenueModel, VenueSearchModel
from util.common import CommonUtilities, RequestOperators
from util.database import PagingModel


class VenueManager:
    def __init__(
        self,
        venue_accessor: VenueAccessor = VenueAccessor(),
        common_utilities: CommonUtilities = CommonUtilities(),
    ) -> None:
        self.venue_accessor = venue_accessor
        self.common_utilities = common_utilities

    def create_venue(
        self,
        inbound_model: VenueCreateModel,
        request_operators: RequestOperators | None = None,
    ) -> VenueModel | None:
        result = self.venue_accessor.insert(
            model=inbound_model, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_venues([result], request_operators)

        return result

    def get_venue_by_id(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> VenueModel | None:
        result = self.venue_accessor.select_by_id(
            id=id, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_venues([result], request_operators)

        return result

    def search_venues(
        self,
        model: VenueSearchModel,
        paging_model: PagingModel | None = None,
        request_operators: RequestOperators | None = None,
    ) -> ItemList[VenueModel]:
        result = self.venue_accessor.select(
            model=model, paging_model=paging_model, request_operators=request_operators
        )

        from managers.hydrator import Hydrator

        hydrator = Hydrator()
        hydrator.hydrate_venues(result.items, request_operators)

        return result

    def delete_venue(
        self, id: UUID, request_operators: RequestOperators | None = None
    ) -> VenueModel | None:
        result: None | VenueModel = self.venue_accessor.delete(
            id=id, request_operators=request_operators
        )

        return result
