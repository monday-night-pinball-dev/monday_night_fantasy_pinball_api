from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID
from fastapi import Query
from pydantic import UUID4, BaseModel, BeforeValidator, Field, Strict

from models.common_model import (
    CommonDatabaseModel,
    CommonInboundSearchModel,
    CommonModel,
    CommonOutboundResponseModel,
    CommonSearchModel,
    validate_ids,
)
from models.venue_model import (
    VenueModel,
    VenueOutboundModel,
)


# Pydantic causes these class variables to safely be instance variables.
class LeagueTeamInboundCreateModel(BaseModel):
    home_venue_id: Annotated[UUID4, Strict(False)] = Field(...)
    short_name: str = Field(..., max_length=3)
    name: str = Field(..., max_length=64)


# Pydantic causes these class variables to safely be instance variables.
class LeagueTeamInboundUpdateModel(BaseModel):
    name: Optional[str] = Field(default=None, max_length=64)
    home_venue_id: Optional[Annotated[UUID4, Strict(False)]] = Field(
        default=None,
    )
    short_name: Optional[str] = Field(default=None, max_length=3)


# Pydantic causes these class variables to safely be instance variables.
class LeagueTeamInboundSearchModel(CommonInboundSearchModel):
    name: Optional[str] = Query(default=None)
    name_like: Optional[str] = Query(default=None)
    short_name: Optional[str] = Query(default=None)
    home_venue_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(
        default=None
    )


class LeagueTeamCreateModel:
    def __init__(
        self,
        name: str,
        short_name: str,
        home_venue_id: UUID,
    ) -> None:
        self.name = name
        self.short_name = short_name
        self.home_venue_id = home_venue_id


class LeagueTeamUpdateModel:
    def __init__(
        self,
        name: str | None = None,
        short_name: str | None = None,
        home_venue_id: UUID | None = None,
    ) -> None:
        self.name = name
        self.short_name = short_name
        self.home_venue_id = home_venue_id


class LeagueTeamSearchModel(CommonSearchModel):
    def __init__(
        self,
        ids: list[UUID] | None = None,
        home_venue_ids: list[UUID] | None = None,
        name: str | None = None,
        name_like: str | None = None,
        short_name: str | None = None,
    ) -> None:
        super().__init__(ids)

        self.name = name
        self.name_like = name_like
        self.home_venue_ids = home_venue_ids
        self.short_name = short_name


class LeagueTeamDatabaseModel(CommonDatabaseModel):
    def __init__(
        self,
        id: UUID,
        home_venue_id: UUID,
        name: str,
        short_name: str,
        created_at: datetime,
        updated_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at)

        self.name = name
        self.short_name = short_name
        self.home_venue_id = home_venue_id


class LeagueTeamModel(CommonModel):
    def __init__(
        self,
        id: UUID,
        home_venue_id: UUID,
        name: str,
        short_name: str,
        created_at: datetime,
        home_venue: VenueModel | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at)

        self.name = name
        self.short_name = short_name
        self.home_venue_id = home_venue_id
        self.home_venue = home_venue


# Pydantic causes these class variables to safely be instance variables.
class LeagueTeamOutboundModel(CommonOutboundResponseModel):
    name: str
    home_venue_id: UUID
    home_venue: VenueOutboundModel | None = None
