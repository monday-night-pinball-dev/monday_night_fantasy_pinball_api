import { MnfpDataTable } from "@/Components/EntitySearchComponents/MnfpDataTable";
import { ColumnDefTemplateItem, ColumnTypes } from "@/Lib/tableFunctions";

type ColumnDefTemplate = Record<string, ColumnDefTemplateItem> 

export default function AdminLeaguePlayersPage() {
  const columnTemplate: ColumnDefTemplate = {
    
    name: {
      title: 'Name',  
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: { 
        key: 'id',
        profileUrl: '/admin/league_players',
      },  
      sortable: true,
    },  
    global_mnp_id: {
      title: 'MNP ID',
    },
    "league_team.name": {
      title: 'League Team',    
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: {
        key: 'league_team_id',
        profileUrl: '/admin/league_teams',
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
      <h1>Admin League Players</h1>
      <MnfpDataTable
        outboundModelName="LeaguePlayerOutboundModel" 
        baseApiUrl={import.meta.env.VITE_BASE_API_URL}
        entityApiName="league_players"
        columnTemplate={columnTemplate}
        defaultSortColumn="created_at"
        defaultSortDirection="desc" 
        hydration={["league_team"]}
      />
    </div>
  );
}