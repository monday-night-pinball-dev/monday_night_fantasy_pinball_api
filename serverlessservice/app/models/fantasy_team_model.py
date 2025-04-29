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
from models.fantasy_league_model import (
    FantasyLeagueModel,
    FantasyLeagueOutboundModel,
)
from models.user_model import UserModel, UserOutboundModel


# Pydantic causes these class variables to safely be instance variables.
class FantasyTeamInboundCreateModel(BaseModel):
    owner_id: Annotated[UUID4, Strict(False)] = Field(...)
    fantasy_league_id: Annotated[UUID4, Strict(False)] = Field(...)
    name: str = Field(..., max_length=64)


# Pydantic causes these class variables to safely be instance variables.
class FantasyTeamInboundUpdateModel(BaseModel):
    name: Optional[str] = Field(default=None, max_length=64)
    owner_id: Optional[Annotated[UUID4, Strict(False)]] = Field(
        default=None,
    )


# Pydantic causes these class variables to safely be instance variables.
class FantasyTeamInboundSearchModel(CommonInboundSearchModel):
    name: Optional[str] = Query(default=None)
    name_like: Optional[str] = Query(default=None)
    owner_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(
        default=None
    )
    fantasy_league_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(
        default=None
    )


class FantasyTeamCreateModel:
    def __init__(
        self,
        name: str,
        owner_id: UUID,
        fantasy_league_id: UUID,
    ) -> None:
        self.name = name
        self.owner_id = owner_id
        self.fantasy_league_id = fantasy_league_id


class FantasyTeamUpdateModel:
    def __init__(
        self,
        name: str | None = None,
        owner_id: UUID | None = None,
    ) -> None:
        self.name = name
        self.owner_id = owner_id


class FantasyTeamSearchModel(CommonSearchModel):
    def __init__(
        self,
        ids: list[UUID] | None = None,
        owner_ids: list[UUID] | None = None,
        fantasy_league_ids: list[UUID] | None = None,
        name: str | None = None,
        name_like: str | None = None,
    ) -> None:
        super().__init__(ids)

        self.name = name
        self.name_like = name_like
        self.owner_ids = owner_ids
        self.fantasy_league_ids = fantasy_league_ids


class FantasyTeamModel(CommonModel):
    def __init__(
        self,
        id: UUID,
        owner_id: UUID,
        fantasy_league_id: UUID,
        name: str,
        created_at: datetime,
        owner: UserModel | None = None,
        fantasy_league: FantasyLeagueModel | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at)

        self.name = name
        self.owner_id = owner_id
        self.owner = owner
        self.fantasy_league_id = fantasy_league_id
        self.fantasy_league = fantasy_league


# Pydantic causes these class variables to safely be instance variables.
class FantasyTeamOutboundModel(CommonOutboundResponseModel):
    name: str
    owner_id: UUID
    owner: UserOutboundModel | None = None
    fantasy_league_id: UUID
    fantasy_league: FantasyLeagueOutboundModel | None = None
