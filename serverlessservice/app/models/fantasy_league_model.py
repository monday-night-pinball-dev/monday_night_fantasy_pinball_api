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
class FantasyLeagueInboundCreateModel(BaseModel):
    name: str = Field(..., max_length=64)


# Pydantic causes these class variables to safely be instance variables.
class FantasyLeagueInboundUpdateModel(BaseModel):
    name: str = Field(..., max_length=64)


# Pydantic causes these class variables to safely be instance variables.
class FantasyLeagueInboundSearchModel(CommonInboundSearchModel):
    name: Optional[str] = Query(default=None)
    name_like: Optional[str] = Query(default=None)


class FantasyLeagueCreateModel:
    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name


class FantasyLeagueUpdateModel:
    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name


class FantasyLeagueSearchModel(CommonSearchModel):
    def __init__(
        self,
        ids: list[UUID] | None = None,
        name: str | None = None,
        name_like: str | None = None,
    ) -> None:
        super().__init__(ids)

        self.name = name
        self.name_like = name_like


class FantasyLeagueDatabaseModel(CommonDatabaseModel):
    def __init__(
        self,
        id: UUID,
        name: str,
        created_at: datetime,
        updated_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at)

        self.name = name


class FantasyLeagueModel(CommonModel):
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
class FantasyLeagueOutboundModel(CommonOutboundResponseModel):
    name: str
