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
class SeasonInboundCreateModel(BaseModel):
    name: str = Field(..., max_length=255)
    season_number: int = Field(...)

    # Pydantic causes these class variables to safely be instance variables.


class SeasonInboundUpdateModel(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255)


# Pydantic causes these class variables to safely be instance variables.
class SeasonInboundSearchModel(CommonInboundSearchModel):
    name: Optional[str] = Query(default=None)
    name_like: Optional[str] = Query(default=None)
    season_number_min: Optional[int] = Query(default=None)
    season_number_max: Optional[int] = Query(default=None)


class SeasonCreateModel:
    def __init__(
        self,
        name: str,
        season_number: int,
    ) -> None:
        self.name = name
        self.season_number = season_number


class SeasonUpdateModel:
    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name


class SeasonSearchModel(CommonSearchModel):
    def __init__(
        self,
        ids: list[UUID] | None = None,
        name: str | None = None,
        name_like: str | None = None,
        season_number_min: int | None = None,
        season_number_max: int | None = None,
    ) -> None:
        super().__init__(ids)

        self.name = name
        self.name_like = name_like
        self.season_number_min = season_number_min
        self.season_number_max = season_number_max


class SeasonDatabaseModel(CommonDatabaseModel):
    def __init__(
        self,
        id: UUID,
        name: str,
        season_number: int,
        created_at: datetime,
        updated_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at)

        self.name = name
        self.season_number = season_number


class SeasonModel(CommonModel):
    def __init__(
        self,
        id: UUID,
        name: str,
        season_number: int,
        created_at: datetime,
        updated_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at)

        self.name = name
        self.season_number = season_number


# Pydantic causes these class variables to safely be instance variables.
class SeasonOutboundModel(CommonOutboundResponseModel):
    name: str
    season_number: int
