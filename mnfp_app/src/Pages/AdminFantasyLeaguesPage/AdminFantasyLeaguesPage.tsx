import { MnfpDataTable } from "@/Components/MnfpDataTable";
import { ColumnDefTemplateItem, ColumnTypes } from "@/Lib/tableFunctions";

type ColumnDefTemplate = Record<string, ColumnDefTemplateItem> 

export default function AdminFantasyLeaguesPage() {
  const columnTemplate: ColumnDefTemplate = {
    
    name: {
      title: 'Name',  
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: { 
        key: 'id',
        profileUrl: '/admin/fantasy_leagues',
      },  
      sortable: true,
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
      <h1>Admin Fantasy Leagues</h1>
      <MnfpDataTable
        outboundModelName="FantasyLeagueOutboundModel"
        baseApiUrl={import.meta.env.VITE_BASE_API_URL} 
        entityApiName="fantasy_leagues"
        columnTemplate={columnTemplate}
        defaultSortColumn="created_at"
        defaultSortDirection="desc" 
      />
    </div>
  );
}