import { MnfpDataTable } from "@/Components/MnfpDataTable";
import { ColumnDefTemplateItem, ColumnTypes } from "@/Lib/tableFunctions";

 

type ColumnDefTemplate = Record<string, ColumnDefTemplateItem> 

export default function AdminVenuesPage() {
  const columnTemplate: ColumnDefTemplate = {
    
    name: {
      title: 'Name',  
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: { 
        key: 'id',
        profileUrl: '/admin/venues',
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
      <h1>Admin Venues</h1>
      <MnfpDataTable
        outboundModelName="VenueOutboundModel"
        entityUrl={`${import.meta.env.VITE_BASE_API_URL}/venues`}
        columnTemplate={columnTemplate}
        defaultSortColumn="created_at"
        defaultSortDirection="desc"
      />
    </div>
  );
}