import { MnfpDataTable } from "@/Components/EntitySearchComponents/MnfpDataTable";
import { FilterTemplate, FilterTypes } from "@/Components/EntitySearchComponents/MnfpFilters";
import { ColumnDefTemplate, ColumnTypes } from "@/Lib/tableFunctions";
 
export default function AdminFantasyLeaguesPage() {
  const columnTemplate: ColumnDefTemplate = new ColumnDefTemplate([
    
    ['name', {
      title: 'Name',  
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: { 
        key: 'id',
        profileUrl: '/admin/fantasy_leagues',
      },  
      sortable: true,
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

  const filterTemplate = new FilterTemplate([
    ['id', { 
      title: 'Id',
      type: FilterTypes.STRING, 
      typeParams: { 
        searchKey: 'ids'
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
      <h1>Admin Fantasy Leagues</h1>
      <MnfpDataTable
        outboundModelName="FantasyLeagueOutboundModel"
        baseApiUrl={import.meta.env.VITE_BASE_API_URL} 
        entityApiName="fantasy_leagues"
        columnTemplate={columnTemplate}
        filterTemplate={filterTemplate}
        defaultSortColumn="created_at"
        defaultSortDirection="desc" 
      />
    </div>
  );
}