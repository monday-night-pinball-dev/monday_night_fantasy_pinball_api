import { MnfpDataTable } from "@/Components/EntitySearchComponents/MnfpDataTable";
import { FilterTemplate, FilterTypes } from "@/Components/EntitySearchComponents/MnfpFilters";
import { ColumnDefTemplate, ColumnTypes } from "@/Lib/tableFunctions";

export default function AdminLeaguePlayersPage() {
  const columnTemplate: ColumnDefTemplate = new ColumnDefTemplate([ 
    ['name', {
      title: 'Name',  
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: { 
        key: 'id',
        profileUrl: '/admin/league_players',
      },  
      sortable: true,
    }],  
    ['global_mnp_id', {
      title: 'MNP ID',
    }],
    ["league_team.name", {
      title: 'League Team',    
      typeOverride: ColumnTypes.FK_LINK,
      typeParams: {
        key: 'league_team_id',
        profileUrl: '/admin/league_teams',
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

  const filterTemplate: FilterTemplate = new FilterTemplate([ 
    ['id', { 
      title: 'Id',
      type: FilterTypes.STRING, 
      typeParams: { 
        searchKey: 'ids'
      } 
    }], 
    ['league_team_id', { 
      title: 'League Team Id',
      type: FilterTypes.STRING, 
      typeParams: { 
        searchKey: 'league_team_ids'
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
      <h1>Admin League Players</h1>
      <MnfpDataTable
        outboundModelName="LeaguePlayerOutboundModel" 
        baseApiUrl={import.meta.env.VITE_BASE_API_URL}
        entityApiName="league_players"
        columnTemplate={columnTemplate}
        filterTemplate={filterTemplate}
        defaultSortColumn="created_at"
        defaultSortDirection="desc" 
        hydration={["league_team"]}
      />
    </div>
  );
}