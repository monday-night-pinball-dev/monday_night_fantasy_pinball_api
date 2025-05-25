import { MnfpDataTable } from "@/Components/MnfpDataTable";
import { ColumnDefTemplateItem, ColumnTypes } from "@/Lib/tableFunctions";

 

type ColumnDefTemplate = Record<string, ColumnDefTemplateItem> 

export default function AdminVenuesPage() {
  const columnTemplate: ColumnDefTemplate = {
    
    username: {
      title: 'Username',  
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: { 
        key: 'id',
        profileUrl: '/users',
      },  
      sortable: true,
    },
    name: {
      title: 'Name',    
      sortable: true,
    },     
    "league_player.name": {
      title: 'League Player Name',    
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: { 
        key: 'league_player_id',
        profileUrl: '/league_players',
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
      <h1>Admin Users</h1>
      <MnfpDataTable
        outboundModelName="UserOutboundModel"
        entityUrl={`${import.meta.env.VITE_BASE_API_URL}/users`}
        columnTemplate={columnTemplate}
        defaultSortColumn="created_at"
        defaultSortDirection="desc"
        hydration={["league_player"]}
      />
    </div>
  );
}