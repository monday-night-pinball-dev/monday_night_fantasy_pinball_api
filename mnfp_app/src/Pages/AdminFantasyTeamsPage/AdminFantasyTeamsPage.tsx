import { MnfpDataTable } from "@/Components/EntitySearchComponents/MnfpDataTable";
import { FilterTemplate, FilterTypes } from "@/Components/EntitySearchComponents/MnfpFilters";
import { ColumnDefTemplate, ColumnTypes } from "@/Lib/tableFunctions";
  

export default function AdminFantasyTeamsPage() {
  const columnTemplate: ColumnDefTemplate = new ColumnDefTemplate([
    
    ['name', {
      title: 'Name',  
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: { 
        key: 'id',
        profileUrl: '/admin/fantasy_teams',
      },  
      sortable: true,
    }],  
    ["owner.name", {
      title: 'Owner',    
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: {
        key: 'owner_id',
        profileUrl: '/admin/users', 
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
    ['created_at', {
      title: 'Created At',
      typeOverride: ColumnTypes.DATE, 
      typeParams: {
        format: 'MMM D YYYY',
        locale: 'en',
      },
      sortable: true,
    }]
  ]);

  const filterTemplate = new FilterTemplate([
    ['id', { 
      title: 'Id',
      type: FilterTypes.STRING, 
      typeParams: { 
        searchKey: 'ids'
      } 
    }],
    ['owner_id', { 
      title: 'Owner Id',
      type: FilterTypes.STRING, 
      typeParams: { 
        searchKey: 'owner_ids'
      } 
    }],
    ['fantasy_league_id', { 
      title: 'Fantasy League Id',
      type: FilterTypes.STRING, 
      typeParams: { 
        searchKey: 'fantasy_league_ids'
      } 
    }],
    ['name', { 
      title: 'Name',
      type: FilterTypes.STRING, 
      typeParams: { 
        searchKey: 'name_like'
      } 
    }],
  ]);

  return (
    <div>
      <h1>Admin Fantasy Teams</h1>
      <MnfpDataTable
        outboundModelName="FantasyTeamOutboundModel"
        baseApiUrl={import.meta.env.VITE_BASE_API_URL} 
        entityApiName="fantasy_teams"
        columnTemplate={columnTemplate}
        filterTemplate={filterTemplate}
        defaultSortColumn="created_at"
        defaultSortDirection="desc" 
        hydration={["owner", "fantasy_league"]}
      />
    </div>
  );
}