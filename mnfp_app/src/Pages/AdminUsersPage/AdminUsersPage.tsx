import { MnfpDataTable } from "@/Components/EntitySearchComponents/MnfpDataTable";
import { FilterTemplate, FilterTypes } from "@/Components/EntitySearchComponents/MnfpFilters";
import { ColumnDefTemplate, ColumnTypes } from "@/Lib/tableFunctions"; 
 

export default function AdminVenuesPage() {
  const columnTemplate: ColumnDefTemplate = new ColumnDefTemplate([
    
    ['username', {
      title: 'Username',  
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: { 
        key: 'id',
        profileUrl: '/admin/users',
      },  
      sortable: true,
    }],
    ['name', {
      title: 'Name',    
      sortable: true,
    }],     
    ["league_player.name", {
      title: 'League Player Name',    
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: { 
        key: 'league_player_id',
        profileUrl: '/admin/league_players',
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
  ])

  const filterTemplate : FilterTemplate = new FilterTemplate([
     [ 'id', {
      title: 'Name',
      type: FilterTypes.STRING,
      typeParams: {
        searchKey: 'ids'
      }
    }],
    [ 'league_plahyer_id', {
      title: 'League Player Id',
      type: FilterTypes.STRING,
      typeParams: {
        searchKey: 'league_player_ids'
      }
    }],
    [ 'name', {
      title: 'Name',
      type: FilterTypes.STRING,
      typeParams: {
        searchKey: 'name_like'
      }
    }],
    [ 'username', {
      title: 'Username',
      type: FilterTypes.STRING,
      typeParams: {
        searchKey: 'username_like'
      }
    }],

    ]
  ); 

  return (
    <div>
      <h1>Admin Users</h1>
      <MnfpDataTable
        outboundModelName="UserOutboundModel"
        baseApiUrl={import.meta.env.VITE_BASE_API_URL}
        entityApiName="users"
        columnTemplate={columnTemplate}
        filterTemplate={filterTemplate} 
        defaultSortColumn="created_at"
        defaultSortDirection="desc"
        hydration={["league_player"]}
      />
    </div>
  );
}