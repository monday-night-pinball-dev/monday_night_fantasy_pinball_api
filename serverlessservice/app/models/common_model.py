from datetime import datetime
from typing import Annotated, Generic, Optional, TypeVar
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel, BeforeValidator
from pydantic_core import PydanticCustomError

from util.common import CommonUtilities
from util.database import ResultantPagingModel

from pydantic_extra_types.phone_numbers import PhoneNumber


class DicsPhoneNumber(PhoneNumber):
    default_region_code = 'US'
    phone_format = 'E164'


def validate_ids(value: str | list[str] | None):
    if value is not None:
        
        common_utilities: CommonUtilities = CommonUtilities()
        results: dict[int, str] | None = common_utilities.validate_comma_delimited_ids(value)

        if results is not None:
            message = (common_utilities.generate_invalid_comma_delimited_ids_message(results))

            raise PydanticCustomError(
                'invalid_id_list', 
                '{message}', 
                dict(message=message)
            )

        return value


class CommonOutboundResponseModel(BaseModel):
    id: UUID
    created_at: str
    updated_at: Optional[str]


class CommonSearchModel:

    def __init__(self, ids: list[UUID] | None) -> None:

        self.ids: list[UUID] | None = ids


class CommonDatabaseModel:

    def __init__(
        self, 
        id: UUID, 
        created_at: datetime,
        updated_at: datetime | None
    ) -> None:

        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at


class CommonModel:

    def __init__(
        self, 
        id: UUID, 
        created_at: datetime,
        updated_at: datetime | None
    ) -> None:

        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at


T = TypeVar('T')
TResponse = TypeVar('TResponse', bound=CommonOutboundResponseModel)


# Pydantic causes these class variables to safely be instance variables.
class CommonInboundPagedModel(BaseModel):

    page: Optional[int] = Query(default=None)
    page_length: Optional[int] = Query(default=None)
    sort_by: Optional[str] = Query(default=None)
    is_sort_descending: Optional[bool] = Query(default=None)


# Pydantic causes these class variables to safely be instance variables.
class CommonInboundSearchModel(CommonInboundPagedModel):
    ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = None


class ItemList(Generic[T]):

    def __init__(
        self,
        paging: ResultantPagingModel,
        items: list[T] | None = None
    ) -> None:
        
        super().__init__()

        self.items = items or []
        self.paging = paging


class OutboundResultantPagingModel(BaseModel):
    page: Optional[int] = None
    page_length: Optional[int] = None
    sort_by: Optional[str] = None
    is_sort_descending: Optional[bool] = None
    total_record_count: Optional[int] = None


class OutboundItemListResponse(BaseModel, Generic[TResponse]):
    items: Optional[list[TResponse]]
    paging: Optional[OutboundResultantPagingModel]
