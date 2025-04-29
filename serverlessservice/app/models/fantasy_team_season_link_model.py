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
from models.fantasy_team_model import FantasyTeamModel, FantasyTeamOutboundModel
from models.season_model import SeasonModel, SeasonOutboundModel
from models.user_model import UserModel, UserOutboundModel


# Pydantic causes these class variables to safely be instance variables.
class FantasyTeamSeasonLinkInboundCreateModel(BaseModel):
    season_id: Annotated[UUID4, Strict(False)] = Field(...)
    fantasy_team_id: Annotated[UUID4, Strict(False)] = Field(...)


# Pydantic causes these class variables to safely be instance variables.
class FantasyTeamSeasonLinkInboundSearchModel(CommonInboundSearchModel):
    season_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(
        default=None
    )
    fantasy_team_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(
        default=None
    )
    fantasy_team_owner_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = (
        Query(default=None)
    )
    fantasy_league_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(
        default=None
    )


class FantasyTeamSeasonLinkCreateModel:
    def __init__(
        self,
        season_id: UUID,
        fantasy_team_id: UUID,
        fantasy_team_owner_id: UUID | None = None,
        fantasy_league_id: UUID | None = None,
    ) -> None:
        self.season_id = season_id
        self.fantasy_team_id = fantasy_team_id
        self.fantasy_team_owner_id = fantasy_team_owner_id
        self.fantasy_league_id = fantasy_league_id


class FantasyTeamSeasonLinkSearchModel(CommonSearchModel):
    def __init__(
        self,
        ids: list[UUID] | None = None,
        season_ids: list[UUID] | None = None,
        fantasy_team_ids: list[UUID] | None = None,
        fantasy_team_owner_ids: list[UUID] | None = None,
        fantasy_league_ids: list[UUID] | None = None,
    ) -> None:
        super().__init__(ids)
        self.season_ids = season_ids
        self.fantasy_team_ids = fantasy_team_ids
        self.fantasy_team_owner_ids = fantasy_team_owner_ids
        self.fantasy_league_ids = fantasy_league_ids


class FantasyTeamSeasonLinkModel(CommonModel):
    def __init__(
        self,
        id: UUID,
        season_id: UUID,
        fantasy_team_id: UUID,
        fantasy_team_owner_id: UUID,
        fantasy_league_id: UUID,
        created_at: datetime,
        season: SeasonModel | None = None,
        fantasy_team: FantasyTeamModel | None = None,
        fantasy_team_owner: UserModel | None = None,
        fantasy_league: FantasyLeagueModel | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at)

        self.season_id = season_id
        self.season = season
        self.fantasy_team_id = fantasy_team_id
        self.fantasy_team = fantasy_team
        self.fantasy_team_owner_id = fantasy_team_owner_id
        self.fantasy_team_owner = fantasy_team_owner
        self.fantasy_league_id = fantasy_league_id
        self.fantasy_league = fantasy_league


# Pydantic causes these class variables to safely be instance variables.
class FantasyTeamSeasonLinkOutboundModel(CommonOutboundResponseModel):
    season_id: UUID
    fantasy_team_id: UUID
    fantasy_team_owner_id: UUID
    fantasy_league_id: UUID
    season: SeasonOutboundModel | None = None
    fantasy_team: FantasyTeamOutboundModel | None = None
    fantasy_team_owner: UserOutboundModel | None = None
    fantasy_league: FantasyLeagueOutboundModel | None = None
