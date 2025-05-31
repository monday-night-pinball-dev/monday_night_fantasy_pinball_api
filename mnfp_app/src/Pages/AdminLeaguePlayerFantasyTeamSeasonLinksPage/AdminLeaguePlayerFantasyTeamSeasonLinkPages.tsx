import { MnfpDataTable } from "@/Components/EntitySearchComponents/MnfpDataTable";
import { FilterTemplate, FilterTypes } from "@/Components/EntitySearchComponents/MnfpFilters";
import { ColumnDefTemplate, ColumnTypes } from "@/Lib/tableFunctions";

export default function AdminLeaguePlayerFantasyTeamSeasonLinksPage() {
  const columnTemplate: ColumnDefTemplate = new ColumnDefTemplate([
    
    ['id', {
      title: 'Id',  
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: { 
        key: 'id',
        profileUrl: '/admin/league_player_fantasy_team_season_links',
      },  
      sortable: true,
    }],   
    ["fantasy_team_season_link.id", {
      title: 'Fantasy Team Season Link',    
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: {
        key: 'fantasy_team_season_link_id',
        profileUrl: '/admin/fantasy_team_season_links', 
      },
    }],
    ["league_player.name", {
      title: 'League Player',    
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: {
        key: 'league_player_id',
        profileUrl: '/admin/league_players', 
      },
    }],
    ["fantasy_team.name", {
      title: 'Fantasy Team',    
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: {
        key: 'fantasy_team_id',
        profileUrl: '/admin/fantasy_teams', 
      },
    }],
    ["season.name", {
      title: 'Season',    
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: {
        key: 'seasons_id',
        profileUrl: '/admin/seasons', 
      },
    }],
    ["fantasy_league.name", {
      title: 'Fantasy League',    
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: {
        key: 'fantasy_league_id',
        profileUrl: '/admin/fantasy_leagues', 
      },
    }],
    ["fantasy_team_owner.name", {
      title: 'Owner',    
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: {
        key: 'fantasy_team_owner_id',
        profileUrl: '/admin/users', 
      },
    }],
    ['created_at', {
      title: 'Created At',
      typeOverride: ColumnTypes.DATE, 
      typeParams: {
        format: 'MMM D YYYY',
        locale: 'en',
      },
      sortable: true,
    }],
  ]);

  const filterTemplate; FilterTemplate = new FilterTemplate([
    ['id', { 
      title: 'Id',
      type: FilterTypes.STRING, 
      typeParams: { 
        searchKey: 'ids'
      } 
    }],
    ['fantasy_team_season_link_id', { 
      title: 'Fantasy Team Season Link Id',
      type: FilterTypes.STRING, 
      typeParams: { 
        searchKey: 'fantasy_team_season_link_ids'
      } 
    }],
    ['league_player_id', { 
      title: 'League Player Id',
      type: FilterTypes.STRING, 
      typeParams: { 
        searchKey: 'league_player_ids'
      } 
    }],
    ['fantasy_team_id', { 
      title: 'Fantasy Team Id',
      type: FilterTypes.STRING, 
      typeParams: { 
        searchKey: 'fantasy_team_ids'
      } 
    }],
    ['season_id', { 
      title: 'Season Id',
      type: FilterTypes.STRING, 
      typeParams: { 
        searchKey: 'season_ids'
      } 
    }],
    ['fantasy_league_id', { 
      title: 'Fantasy League Id',
      type: FilterTypes.STRING, 
      typeParams: { 
        searchKey: 'fantasy_league_ids'
      } 
    }],
    ['fantasy_team_owner_id', { 
      title: 'Fantasy Team Owner Id',
      type: FilterTypes.STRING, 
      typeParams: { 
        searchKey: 'fantasy_team_owner_ids'
      } 
    }], 
  ]); // No filters defined for this page

  return (
    <div>
      <h1>Admin Fantasy Team Season Links</h1>
      <MnfpDataTable
        outboundModelName="LeaguePlayerFantasyTeamSeasonLinkOutboundModel"
        baseApiUrl={import.meta.env.VITE_BASE_API_URL} 
        entityApiName="league_player_fantasy_team_season_links"
        columnTemplate={columnTemplate}
        filterTemplate={filterTemplate}
        defaultSortColumn="created_at"
        defaultSortDirection="desc" 
        hydration={["fantasy_team", "season", "fantasy_league", "fantasy_team_owner", "league_player", "fantasy_team_season_link"]}
      />
    </div>
  );
}