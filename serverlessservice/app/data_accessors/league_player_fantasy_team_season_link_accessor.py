from typing import Any, List
from models.league_player_fantasy_team_season_link_model import (
    LeaguePlayerFantasyTeamSeasonLinkModel,
    LeaguePlayerFantasyTeamSeasonLinkSearchModel,
)
from util.database import DatabaseClient


class LeaguePlayerFantasyTeamSeasonLinkAccessor:
    def __init__(self, database_client: DatabaseClient) -> None:
        self.database_client = database_client

    async def insert(
        self, model: LeaguePlayerFantasyTeamSeasonLinkModel
    ) -> dict[str, Any]:
        return await self.database_client.insert(
            "league_player_fantasy_team_season_links", model
        )

    async def search(
        self, search_model: LeaguePlayerFantasyTeamSeasonLinkSearchModel
    ) -> List[dict[str, Any]]:
        return await self.database_client.search(
            "league_player_fantasy_team_season_links", search_model
        )

    async def get_by_id(self, link_id: str) -> dict[str, Any]:
        return await self.database_client.get_by_id(
            "league_player_fantasy_team_season_links", link_id
        )

    async def delete(self, link_id: str) -> bool:
        return await self.database_client.delete(
            "league_player_fantasy_team_season_links", link_id
        )
