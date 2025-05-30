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
from models.league_team_model import LeagueTeamModel, LeagueTeamOutboundModel


# Pydantic causes these class variables to safely be instance variables.
class LeaguePlayerInboundCreateModel(BaseModel):
    league_team_id: Optional[Annotated[UUID4, Strict(False)]] = Field(default=None)
    global_mnp_id: Annotated[UUID4, Strict(False)] = Field(...)
    name: str = Field(..., strip_whitespace=True, min_length=1, max_length=255)


# Pydantic causes these class variables to safely be instance variables.
class LeaguePlayerInboundUpdateModel(BaseModel):
    league_team_id: Optional[Annotated[UUID4, Strict(False)]] = Field(default=None)
    name: Optional[str] = Field(
        default=None, strip_whitespace=True, min_length=1, max_length=255
    )


# Pydantic causes these class variables to safely be instance variables.
class LeaguePlayerInboundSearchModel(CommonInboundSearchModel):
    name: Optional[str] = Query(default=None)
    name_like: Optional[str] = Query(default=None)
    league_team_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(
        default=None
    )
    global_mnp_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(
        default=None
    )


class LeaguePlayerCreateModel:
    def __init__(
        self,
        name: str,
        league_team_id: UUID,
        global_mnp_id: UUID,
    ) -> None:
        self.name = name
        self.league_team_id = league_team_id
        self.global_mnp_id = global_mnp_id


class LeaguePlayerUpdateModel:
    def __init__(
        self,
        name: str,
        league_team_id: UUID,
    ) -> None:
        self.name = name
        self.league_team_id = league_team_id


class LeaguePlayerSearchModel(CommonSearchModel):
    def __init__(
        self,
        ids: list[UUID] | None = None,
        league_team_ids: list[UUID] | None = None,
        global_mnp_ids: list[UUID] | None = None,
        name: str | None = None,
        name_like: str | None = None,
    ) -> None:
        super().__init__(ids)

        self.name = name
        self.name_like = name_like
        self.league_team_ids = league_team_ids
        self.global_mnp_ids = global_mnp_ids


class LeaguePlayerModel(CommonModel):
    def __init__(
        self,
        id: UUID,
        name: str,
        created_at: datetime,
        league_team_id: UUID | None = None,
        league_team: LeagueTeamModel | None = None,
        global_mnp_id: UUID | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at)

        self.name = name
        self.league_team_id = league_team_id
        self.league_team = league_team
        self.global_mnp_id = global_mnp_id


# Pydantic causes these class variables to safely be instance variables.
class LeaguePlayerOutboundModel(CommonOutboundResponseModel):
    name: str
    global_mnp_id: UUID
    league_team_id: UUID | None
    league_team: LeagueTeamOutboundModel | None = None
