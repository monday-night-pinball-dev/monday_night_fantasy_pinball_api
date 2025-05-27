import { MnfpDataTable } from "@/Components/MnfpDataTable";
import { ColumnDefTemplateItem, ColumnTypes } from "@/Lib/tableFunctions";

type ColumnDefTemplate = Record<string, ColumnDefTemplateItem> 

export default function AdminFantasyTeamsPage() {
  const columnTemplate: ColumnDefTemplate = {
    
    name: {
      title: 'Name',  
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: { 
        key: 'id',
        profileUrl: '/admin/fantasy_teams',
      },  
      sortable: true,
    },  
    
    "owner.name": {
      title: 'Owner',    
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: {
        key: 'owner_id',
        profileUrl: '/admin/users', 
      },
    }, 
    "fantasy_league.name": {
      title: 'Fantasy League',    
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: {
        key: 'fantasy_league_id',
        profileUrl: '/admin/fantasy_leagues', 
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
      <h1>Admin Fantasy Teams</h1>
      <MnfpDataTable
        outboundModelName="FantasyTeamOutboundModel"
        entityUrl={`${import.meta.env.VITE_BASE_API_URL}/fantasy_teams`}
        columnTemplate={columnTemplate}
        defaultSortColumn="created_at"
        defaultSortDirection="desc" 
        hydration={["owner", "fantasy_league"]}
      />
    </div>
  );
}