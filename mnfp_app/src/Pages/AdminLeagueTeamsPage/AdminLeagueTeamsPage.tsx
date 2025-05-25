import { MnfpDataTable } from "@/Components/MnfpDataTable";
import { ColumnDefTemplateItem, ColumnTypes } from "@/Lib/tableFunctions";

type ColumnDefTemplate = Record<string, ColumnDefTemplateItem> 

export default function AdminLeagueTeamsPage() {
  const columnTemplate: ColumnDefTemplate = {
    
    name: {
      title: 'Name',  
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: { 
        key: 'id',
        profileUrl: '/admin/leagueTeams',
      },  
      sortable: true,
    },  
    short_name: {
      title: 'Short Name', 
      sortable: true,
    },
    global_mnp_id: {
      title: 'MNP ID',
    },
    "home_venue.name": {
      title: 'Venue',    
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: {
        key: 'home_venue_id',
        profileUrl: '/admin/venues',
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
      <h1>Admin League Teams</h1>
      <MnfpDataTable
        outboundModelName="LeagueTeamOutboundModel"
        entityUrl={`${import.meta.env.VITE_BASE_API_URL}/league_teams`}
        columnTemplate={columnTemplate}
        defaultSortColumn="created_at"
        defaultSortDirection="desc" 
        hydration={["venue"]}
      />
    </div>
  );
}