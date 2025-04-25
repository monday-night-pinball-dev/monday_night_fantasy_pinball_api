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


# Pydantic causes these class variables to safely be instance variables.
class LeaguePlayerFantasyTeamSeasonLinkInboundCreateModel(BaseModel):
    fantasy_team_season_link_id: Annotated[UUID4, Strict(False)] = Field(...)
    season_id: Annotated[UUID4, Strict(False)] = Field(...)
    fantasy_team_id: Annotated[UUID4, Strict(False)] = Field(...)
    fantasy_team_owner_id: Annotated[UUID4, Strict(False)] = Field(...)


# Pydantic causes these class variables to safely be instance variables.
class LeaguePlayerFantasyTeamSeasonLinkInboundSearchModel(CommonInboundSearchModel):
    fantasy_team_season_link_ids: Annotated[
        Optional[str], BeforeValidator(validate_ids)
    ] = Query(default=None)
    season_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(
        default=None
    )
    fantasy_team_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(
        default=None
    )
    fantasy_team_owner_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = (
        Query(default=None)
    )


class LeaguePlayerFantasyTeamSeasonLinkCreateModel:
    def __init__(
        self,
        fantasy_team_season_link_id: UUID,
        season_id: UUID,
        fantasy_team_id: UUID,
        fantasy_team_owner_id: UUID,
    ) -> None:
        self.fantasy_team_season_link_id = fantasy_team_season_link_id
        self.season_id = season_id
        self.fantasy_team_id = fantasy_team_id
        self.fantasy_team_owner_id = fantasy_team_owner_id


class LeaguePlayerFantasyTeamSeasonLinkSearchModel(CommonSearchModel):
    def __init__(
        self,
        ids: list[UUID] | None = None,
        fantasy_team_season_link_ids: list[UUID] | None = None,
        season_ids: list[UUID] | None = None,
        fantasy_team_ids: list[UUID] | None = None,
        fantasy_team_owner_ids: list[UUID] | None = None,
    ) -> None:
        super().__init__(ids)

        self.fantasy_team_season_link_ids = fantasy_team_season_link_ids
        self.season_ids = season_ids
        self.fantasy_team_ids = fantasy_team_ids
        self.fantasy_team_owner_ids = fantasy_team_owner_ids


class LeaguePlayerFantasyTeamSeasonLinkDatabaseModel(CommonDatabaseModel):
    def __init__(
        self,
        id: UUID,
        fantasy_team_season_link_id: UUID,
        season_id: UUID,
        fantasy_team_id: UUID,
        fantasy_team_owner_id: UUID,
        created_at: datetime,
        updated_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at)

        self.fantasy_team_season_link_id = fantasy_team_season_link_id
        self.season_id = season_id
        self.fantasy_team_id = fantasy_team_id
        self.fantasy_team_owner_id = fantasy_team_owner_id


class LeaguePlayerFantasyTeamSeasonLinkModel(CommonModel):
    def __init__(
        self,
        id: UUID,
        fantasy_team_season_link_id: UUID,
        season_id: UUID,
        fantasy_team_id: UUID,
        fantasy_team_owner_id: UUID,
        created_at: datetime,
        updated_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at)

        self.fantasy_team_season_link_id = fantasy_team_season_link_id
        self.season_id = season_id
        self.fantasy_team_id = fantasy_team_id
        self.fantasy_team_owner_id = fantasy_team_owner_id


# Pydantic causes these class variables to safely be instance variables.
class LeaguePlayerFantasyTeamSeasonLinkOutboundModel(CommonOutboundResponseModel):
    fantasy_team_season_link_id: UUID
    season_id: UUID
    fantasy_team_id: UUID
    fantasy_team_owner_id: UUID
