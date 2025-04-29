from datetime import datetime
from enum import Enum, StrEnum
from typing import Annotated, Optional
from uuid import UUID
from fastapi import Query
from pydantic import UUID4, BaseModel, BeforeValidator, EmailStr, Field, Strict

from models.common_model import (
    CommonDatabaseModel,
    CommonInboundSearchModel,
    CommonModel,
    CommonOutboundResponseModel,
    CommonSearchModel,
    validate_ids,
)
from models.league_player_model import LeaguePlayerModel, LeaguePlayerOutboundModel


# Pydantic causes these class variables to safely be instance variables.
class UserInboundCreateModel(BaseModel):
    league_player_id: Optional[Annotated[UUID4, Strict(False)]] = Field(default=None)
    name: str = Field(..., max_length=255)
    username: EmailStr = Field(..., max_length=320)


# Pydantic causes these class variables to safely be instance variables.
class UserInboundUpdateModel(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255)


# Pydantic causes these class variables to safely be instance variables.
class UserInboundSearchModel(CommonInboundSearchModel):
    username_like: Optional[str] = Query(default=None)
    username: Optional[str] = Query(default=None)
    name: Optional[str] = Query(default=None)
    name_like: Optional[str] = Query(default=None)
    league_player_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(
        default=None
    )


class UserCreateModel:
    def __init__(
        self,
        username: str,
        name: str,
        league_player_id: UUID | None = None,
    ) -> None:
        self.league_player_id = league_player_id
        self.username = username
        self.name = name


class UserUpdateModel:
    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name


class UserSearchModel(CommonSearchModel):
    def __init__(
        self,
        ids: list[UUID] | None = None,
        league_player_ids: list[UUID] | None = None,
        name: str | None = None,
        name_like: str | None = None,
        username_like: str | None = None,
        username: str | None = None,
    ) -> None:
        super().__init__(ids)
        self.league_player_ids = league_player_ids
        self.name = name
        self.name_like = name_like
        self.username = username
        self.username_like = username_like


class UserModel(CommonModel):
    def __init__(
        self,
        id: UUID,
        username: str,
        name: str,
        created_at: datetime,
        league_player_id: UUID | None = None,
        league_player: LeaguePlayerModel | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at)

        self.username = username
        self.name = name
        self.league_player_id = league_player_id
        self.league_player = league_player


# Pydantic causes these class variables to safely be instance variables.
class UserOutboundModel(CommonOutboundResponseModel):
    league_player_id: UUID | None = None
    league_player: LeaguePlayerOutboundModel | None = None

    username: str
    name: str
