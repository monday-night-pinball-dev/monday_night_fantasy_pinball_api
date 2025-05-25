import { MnfpDataTable } from "@/Components/MnfpDataTable";
import { ColumnDefTemplateItem, ColumnTypes } from "@/Lib/tableFunctions";

type ColumnDefTemplate = Record<string, ColumnDefTemplateItem> 

export default function AdminFantasyTeamSeasonLinksPage() {
  const columnTemplate: ColumnDefTemplate = {
    
    id: {
      title: 'Id',  
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: { 
        key: 'id',
        profileUrl: '/fantasy_team_season_links',
      },  
      sortable: true,
    },   
    "fantasy_team.name": {
      title: 'Fantasy Team',    
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: {
        key: 'fantasy_team_id',
        profileUrl: '/fantasy_teams', 
      },
    },
    "season.name": {
      title: 'Season',    
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: {
        key: 'seasons_id',
        profileUrl: '/seasons', 
      },
    },
    "fantasy_league.name": {
      title: 'Fantasy League',    
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: {
        key: 'fantasy_league_id',
        profileUrl: '/fantasy_leagues', 
      },
    },
    "fantasy_team_owner.name": {
      title: 'Owner',    
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: {
        key: 'fantasy_team_owner_id',
        profileUrl: '/users', 
      },
    },
    created_at: {
      title: 'Created At',
      typeOverride: ColumnTypes.DATE, 
      typeParams: {
        format: 'MMM D YYYY',
        locale: 'en',
      },
      sortable: true,
    },
  } 

  return (
    <div>
      <h1>Admin Fantasy Team Season Links</h1>
      <MnfpDataTable
        outboundModelName="FantasyTeamSeasonLinkOutboundModel"
        entityUrl={`${import.meta.env.VITE_BASE_API_URL}/fantasy_team_season_links`}
        columnTemplate={columnTemplate}
        defaultSortColumn="created_at"
        defaultSortDirection="desc" 
        hydration={["fantasy_team", "season", "fantasy_league", "fantasy_team_owner"]}
      />
    </div>
  );
}