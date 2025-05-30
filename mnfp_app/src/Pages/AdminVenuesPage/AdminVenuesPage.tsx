import { MnfpDataTable } from "@/Components/EntitySearchComponents/MnfpDataTable";
import { FilterTemplate, FilterTypes } from "@/Components/EntitySearchComponents/MnfpFilters";
import {   ColumnDefTemplate, ColumnTypes } from "@/Lib/tableFunctions"; 

export default function AdminVenuesPage() {
  const columnTemplate: ColumnDefTemplate = new ColumnDefTemplate([
    ['name', {
      title: 'Name',
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: {
        key: 'id',
        profileUrl: '/admin/venues',
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
  ])


  const filterTemplate: FilterTemplate = new FilterTemplate([ 
    ['name', { 
      title: 'Name',
      type: FilterTypes.STRING, 
      typeParams: { 
        searchKey: 'name_like'
      } 
    }],
  ])

  return (
    <div>
      <div>
        <h1>Admin Venues</h1>
      </div>
  
      <MnfpDataTable
        outboundModelName="VenueOutboundModel"
        baseApiUrl={import.meta.env.VITE_BASE_API_URL}
        entityApiName="venues"
        columnTemplate={columnTemplate}
        filterTemplate={filterTemplate}
        defaultSortColumn="created_at"
        defaultSortDirection="desc"
      />
    </div>
  );
}