from datetime import datetime
from typing import Optional
from uuid import UUID
from fastapi import Query
from pydantic import BaseModel, Field

from models.common_model import (
    CommonDatabaseModel,
    CommonInboundSearchModel,
    CommonModel,
    CommonOutboundResponseModel,
    CommonSearchModel,
)


# Pydantic causes these class variables to safely be instance variables.
class VenueInboundCreateModel(BaseModel):
    name: str = Field(..., max_length=255)


# Pydantic causes these class variables to safely be instance variables.
class VenueInboundSearchModel(CommonInboundSearchModel):
    name: Optional[str] = Query(default=None)
    name_like: Optional[str] = Query(default=None)


class VenueCreateModel:
    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name


class VenueSearchModel(CommonSearchModel):
    def __init__(
        self,
        ids: list[UUID] | None = None,
        name: str | None = None,
        name_like: str | None = None,
    ) -> None:
        super().__init__(ids)

        self.name = name
        self.name_like = name_like


class VenueModel(CommonModel):
    def __init__(
        self,
        id: UUID,
        name: str,
        created_at: datetime,
        updated_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at)

        self.name = name


# Pydantic causes these class variables to safely be instance variables.
class VenueOutboundModel(CommonOutboundResponseModel):
    name: str
