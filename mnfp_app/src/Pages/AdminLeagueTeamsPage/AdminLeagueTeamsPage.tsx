import { MnfpDataTable } from "@/Components/EntitySearchComponents/MnfpDataTable";
import { FilterTemplate, FilterTypes } from "@/Components/EntitySearchComponents/MnfpFilters";
import { ColumnDefTemplate, ColumnTypes } from "@/Lib/tableFunctions";

export default function AdminLeagueTeamsPage() {
  const columnTemplate: ColumnDefTemplate = new ColumnDefTemplate([
    
    ['name', {
      title: 'Name',  
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: { 
        key: 'id',
        profileUrl: '/admin/league_teams',
      },  
      sortable: true,
    }],  
    ['short_name', {
      title: 'Short Name', 
      sortable: true,
    }],
    ['global_mnp_id', {
      title: 'MNP ID',
    }],
    ["home_venue.name", {
      title: 'Venue',    
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: {
        key: 'home_venue_id',
        profileUrl: '/admin/venues',
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

  const filterTemplate: FilterTemplate = new FilterTemplate([ 
    ['id', { 
      title: 'Id',
      type: FilterTypes.STRING, 
      typeParams: { 
        searchKey: 'ids'
      } 
    }],
    ['home_venue_id', { 
      title: 'Home Venue Id',
      type: FilterTypes.STRING, 
      typeParams: { 
        searchKey: 'home_venue_ids'
      } 
    }],
    ['name', { 
      title: 'Name',
      type: FilterTypes.STRING, 
      typeParams: { 
        searchKey: 'name_like'
      } 
    }],
    ['short_name', { 
      title: 'Short Name',
      type: FilterTypes.STRING, 
      typeParams: { 
        searchKey: 'short_name'
      } 
    }],
    ['global_mnp_id', { 
      title: 'Mnp Id',
      type: FilterTypes.STRING, 
      typeParams: { 
        searchKey: 'global_mnp_id'
      } 
    }],
  ])
  
  return (
    <div>
      <h1>Admin League Teams</h1>
      <MnfpDataTable
        outboundModelName="LeagueTeamOutboundModel"
        baseApiUrl={import.meta.env.VITE_BASE_API_URL}
        entityApiName="league_teams"
        columnTemplate={columnTemplate}
        filterTemplate={filterTemplate}
        defaultSortColumn="created_at"
        defaultSortDirection="desc" 
        hydration={["home_venue"]}
      />
    </div>
  );
}