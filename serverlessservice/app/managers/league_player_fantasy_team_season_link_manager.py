from typing import Any, List
from models.league_player_fantasy_team_season_link_model import (
    LeaguePlayerFantasyTeamSeasonLinkModel,
    LeaguePlayerFantasyTeamSeasonLinkSearchModel,
)
from util.database import DatabaseClient


class LeaguePlayerFantasyTeamSeasonLinkManager:
    def __init__(self, database_client: DatabaseClient) -> None:
        self.database_client = database_client

    async def create_link(
        self, model: LeaguePlayerFantasyTeamSeasonLinkModel
    ) -> dict[str, Any]:
        return await self.database_client.insert(
            "league_player_fantasy_team_season_links", model
        )

    async def search_links(
        self, search_model: LeaguePlayerFantasyTeamSeasonLinkSearchModel
    ) -> List[dict[str, Any]]:
        return await self.database_client.search(
            "league_player_fantasy_team_season_links", search_model
        )

    async def get_link_by_id(self, link_id: str) -> dict[str, Any]:
        link = await self.database_client.get_by_id(
            "league_player_fantasy_team_season_links", link_id
        )
        if link:
            # Hydration logic
            # Example: Hydrate `fantasy_team_season_link_id` with data from `fantasy_team_season_links`
            link["fantasy_team_season_link"] = await self.database_client.get_by_id(
                "fantasy_team_season_links", link["fantasy_team_season_link_id"]
            )
            # Add more hydration logic if needed
        return link

    async def delete_link(self, link_id: str) -> bool:
        return await self.database_client.delete(
            "league_player_fantasy_team_season_links", link_id
        )
