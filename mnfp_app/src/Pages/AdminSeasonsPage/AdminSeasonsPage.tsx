import { MnfpDataTable } from "@/Components/EntitySearchComponents/MnfpDataTable";
import { FilterTemplate, FilterTypes } from "@/Components/EntitySearchComponents/MnfpFilters";
import { ColumnDefTemplate, ColumnTypes,  } from "@/Lib/tableFunctions";

 

export default function AdminSeasonsPage() {
  const columnTemplate: ColumnDefTemplate = new ColumnDefTemplate([
    
    ['name', {
      title: 'Name',  
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: { 
        key: 'id',
        profileUrl: '/admin/seasons',
      },  
      sortable: true,
    }],  
    ['season_number', {
      title: 'Season Number',  
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
  ])
  
  return (
    <div>
      <h1>Admin Seasons</h1>
      <MnfpDataTable
        outboundModelName="SeasonOutboundModel"
        baseApiUrl={import.meta.env.VITE_BASE_API_URL}
        entityApiName="seasons"
        columnTemplate={columnTemplate}
        filterTemplate={filterTemplate}
        defaultSortColumn="created_at"
        defaultSortDirection="desc"
      />
    </div>
  );
}