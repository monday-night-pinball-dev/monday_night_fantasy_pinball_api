import { MnfpDataTable } from "@/Components/MnfpDataTable";
import { ColumnDefTemplateItem, ColumnTypes,  } from "@/Lib/tableFunctions";


type ColumnDefTemplate = Record<string, ColumnDefTemplateItem> 

export default function AdminSeasonsPage() {
  const columnTemplate: ColumnDefTemplate = {
    
    name: {
      title: 'Name',  
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: { 
        key: 'id',
        profileUrl: '/admin/seasons',
      },  
      sortable: true,
    },  
    season_number: {
      title: 'Season Number',  
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
      <h1>Admin Seasons</h1>
      <MnfpDataTable
        outboundModelName="SeasonOutboundModel"
        entityUrl={`${import.meta.env.VITE_BASE_API_URL}/seasons`}
        columnTemplate={columnTemplate}
        defaultSortColumn="created_at"
        defaultSortDirection="desc"
      />
    </div>
  );
}