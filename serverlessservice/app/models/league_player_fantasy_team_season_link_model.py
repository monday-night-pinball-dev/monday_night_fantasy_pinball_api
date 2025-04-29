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
from models.fantasy_league_model import FantasyLeagueModel, FantasyLeagueOutboundModel
from models.fantasy_team_model import FantasyTeamModel, FantasyTeamOutboundModel
from models.fantasy_team_season_link_model import (
    FantasyTeamSeasonLinkModel,
    FantasyTeamSeasonLinkOutboundModel,
)
from models.league_player_model import LeaguePlayerModel, LeaguePlayerOutboundModel
from models.league_team_model import LeagueTeamModel, LeagueTeamOutboundModel
from models.season_model import SeasonModel, SeasonOutboundModel
from models.user_model import UserModel, UserOutboundModel


# Pydantic causes these class variables to safely be instance variables.
class LeaguePlayerFantasyTeamSeasonLinkInboundCreateModel(BaseModel):
    fantasy_team_season_link_id: Annotated[UUID4, Strict(False)] = Field(...)
    league_player_id: Annotated[UUID4, Strict(False)] = Field(...)


# Pydantic causes these class variables to safely be instance variables.
class LeaguePlayerFantasyTeamSeasonLinkInboundSearchModel(CommonInboundSearchModel):
    league_player_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(
        default=None
    )
    league_team_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(
        default=None
    )
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
    fantasy_league_ids: Annotated[Optional[str], BeforeValidator(validate_ids)] = Query(
        default=None
    )


class LeaguePlayerFantasyTeamSeasonLinkCreateModel:
    def __init__(
        self,
        league_player_id: UUID,
        fantasy_team_season_link_id: UUID,
        league_team_id: UUID | None = None,
        season_id: UUID | None = None,
        fantasy_team_id: UUID | None = None,
        fantasy_team_owner_id: UUID | None = None,
        fantasy_league_id: UUID | None = None,
    ) -> None:
        self.league_player_id = league_player_id
        self.league_team_id = league_team_id
        self.fantasy_team_season_link_id = fantasy_team_season_link_id
        self.season_id = season_id
        self.fantasy_team_id = fantasy_team_id
        self.fantasy_team_owner_id = fantasy_team_owner_id
        self.fantasy_league_id = fantasy_league_id


class LeaguePlayerFantasyTeamSeasonLinkSearchModel(CommonSearchModel):
    def __init__(
        self,
        ids: list[UUID] | None = None,
        league_player_ids: list[UUID] | None = None,
        league_team_ids: list[UUID] | None = None,
        fantasy_team_season_link_ids: list[UUID] | None = None,
        season_ids: list[UUID] | None = None,
        fantasy_team_ids: list[UUID] | None = None,
        fantasy_team_owner_ids: list[UUID] | None = None,
        fantasy_league_ids: list[UUID] | None = None,
    ) -> None:
        super().__init__(ids)
        self.league_player_ids = league_player_ids
        self.league_team_ids = league_team_ids
        self.fantasy_team_season_link_ids = fantasy_team_season_link_ids
        self.season_ids = season_ids
        self.fantasy_team_ids = fantasy_team_ids
        self.fantasy_team_owner_ids = fantasy_team_owner_ids
        self.fantasy_league_ids = fantasy_league_ids


class LeaguePlayerFantasyTeamSeasonLinkModel(CommonModel):
    def __init__(
        self,
        id: UUID,
        league_player_id: UUID,
        league_team_id: UUID,
        fantasy_team_season_link_id: UUID,
        season_id: UUID,
        fantasy_team_id: UUID,
        fantasy_team_owner_id: UUID,
        fantasy_league_id: UUID,
        created_at: datetime,
        league_player: LeaguePlayerModel | None = None,
        league_team: LeagueTeamModel | None = None,
        fantasy_team_season_link: FantasyTeamSeasonLinkModel | None = None,
        season: SeasonModel | None = None,
        fantasy_team: FantasyTeamModel | None = None,
        fantasy_team_owner: UserModel | None = None,
        fantasy_league: FantasyLeagueModel | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at)
        self.league_player_id = league_player_id
        self.league_player = league_player
        self.league_team = league_team
        self.fantasy_team_season_link = fantasy_team_season_link
        self.season = season
        self.fantasy_team = fantasy_team
        self.fantasy_team_owner = fantasy_team_owner
        self.fantasy_league = fantasy_league
        self.fantasy_team_owner_id = fantasy_team_owner_id
        self.league_team_id = league_team_id
        self.fantasy_team_season_link_id = fantasy_team_season_link_id
        self.season_id = season_id
        self.fantasy_team_id = fantasy_team_id
        self.fantasy_team_owner_id = fantasy_team_owner_id
        self.fantasy_league_id = fantasy_league_id


# Pydantic causes these class variables to safely be instance variables.
class LeaguePlayerFantasyTeamSeasonLinkOutboundModel(CommonOutboundResponseModel):
    league_player_id: UUID
    league_player: LeaguePlayerOutboundModel | None = None
    league_team_id: UUID | None = None
    league_team: LeagueTeamOutboundModel | None = None
    fantasy_team_season_link_id: UUID
    fantasy_team_season_link: FantasyTeamSeasonLinkOutboundModel | None = None
    season_id: UUID
    season: SeasonOutboundModel | None = None
    fantasy_team_id: UUID
    fantasy_team: FantasyTeamOutboundModel | None = None
    fantasy_team_owner_id: UUID
    fantasy_team_owner: UserOutboundModel | None = None
    fantasy_league_id: UUID
    fantasy_league: FantasyLeagueOutboundModel | None = None
