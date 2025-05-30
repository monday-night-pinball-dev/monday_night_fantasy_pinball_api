/* eslint-disable dot-notation */
import { ColumnDefTemplate, determineColumnDefs } from '@/Lib/tableFunctions';
import { Button } from '@mantine/core';
import axios from 'axios'; 
import { DataTable, DataTableColumn, DataTableSortStatus } from 'mantine-datatable';
import { useEffect, useState } from 'react'; 
import { NavLink } from 'react-router-dom';
import { FilterTemplate, MnfpFilters } from './MnfpFilters'; 
import { convertFromRecordToQueryArgs } from '@/Lib/util'; 

interface MnfpDataTableProps {
    outboundModelName: string, 
    baseApiUrl : string,
    entityApiName: string,
    columnTemplate : ColumnDefTemplate,
    filterTemplate: FilterTemplate,
    defaultSortColumn: string,
    defaultSortDirection: "asc" | "desc" ,
    hydration?: string[],
}

export const MnfpDataTable: React.FC<MnfpDataTableProps> = ({ 
    baseApiUrl,
    entityApiName,
    columnTemplate,
    filterTemplate,
    defaultSortColumn,
    defaultSortDirection,
    hydration,
}) => { 

    async function fetchTableData(
      pageIn: number, 
      pageSizeIn: number, 
      sortStatusIn: DataTableSortStatus<any>, 
      values: Record<string, any> = {}
    ) { 
        const isDescending = sortStatusIn.direction === 'desc' ? 'true' : 'false';

        const queryArgs = convertFromRecordToQueryArgs(values);

        let url = `${baseApiUrl}/${entityApiName}?page=${pageIn}&page_length=${pageSizeIn}&sort_by=${String(sortStatusIn.columnAccessor)}&is_sort_descending=${isDescending}`

        if(queryArgs) {
            url += `&${queryArgs}`;
        }

        const response = await axios.get(url, {
            headers: {
                'MNFP-Hydration': hydration?.join(","),
            }
        });

        if(hydration) {
            hydration?.forEach((hydrationName:string) => {
               response.data.items.forEach((item: Record<string, any>) => {
                    if(item[hydrationName]) {
                        // get keys
                        const keys = Object.keys(item[hydrationName]);
                        keys.forEach((key) => {
                            item[`${hydrationName}.${key}`] = item[hydrationName][key];
                        });
                    }
                });
            });
        }
         
        if (response.status === 200) { 
            setPage(response.data.paging.page);
            setTotalRecords(response.data.paging.total_record_count);
            setRecords(response.data.items); 
            setPageSize(response.data.paging.page_length);

            const sortdirection: "asc" | "desc" = response.data.paging.is_sort_descending ? "desc" : "asc";

            const sortStatusTemp: DataTableSortStatus<any> = {
                columnAccessor: response.data.paging.sort_by,
                direction: sortdirection,
            }

            setSortStatus(sortStatusTemp);
        }

        setFilterValues(values);
    }
 
  const [pageSize, setPageSize] = useState(15);
  const [page, setPage] = useState(1);
  const [totalRecords, setTotalRecords] = useState(0);
  const [records, setRecords] = useState([]);
  const [columns, setColumns] = useState<DataTableColumn[]>([]);
  const [filterValues, setFilterValues] = useState<Record<string, any>>({});

  const [sortStatus, setSortStatus] = useState<DataTableSortStatus<any>>({
    columnAccessor: defaultSortColumn,
    direction: defaultSortDirection,
  });
  
  useEffect(() => {
    const fetchColumnDefs = async () => {
      // const schema = await axios.get(`${import.meta.env.VITE_BASE_API_URL}/openapi.json`);s
      const columnDefs = determineColumnDefs(columnTemplate); 
      setColumns(columnDefs);
    }
    fetchColumnDefs();
    fetchTableData(page, pageSize, sortStatus, filterValues);
  }, [])
  
  return (
    <div>
      <div>
        Filters:
        <MnfpFilters  
          filterTemplate={filterTemplate}
          onFilterChange={(values) => {
            // Handle filter change, e.g., refetch data with new filters
            fetchTableData(page, pageSize, sortStatus, values);
          }}
        />
      </div>
      <div  style={{float:'right'}}>
        <NavLink to={`/admin/${entityApiName}/new`} className="btn btn-primary">
          <Button variant="filled" color="blue">
            Create
          </Button>
        </NavLink>
      </div>
      <div style={{clear: 'both'}}>
        <DataTable
            height={300}
            withTableBorder
            withRowBorders
            paginationWithControls
            paginationWithEdges
            withColumnBorders
            records={records}
            columns={columns}
            totalRecords={totalRecords}
            recordsPerPage={pageSize}
            page={page}
            recordsPerPageOptions={[5, 10, 15, 20, 25]}
            onSortStatusChange={(val: DataTableSortStatus) => { 
                fetchTableData(page, pageSize, val, filterValues);
            }}
            sortStatus={sortStatus} 
            onPageChange={
              (val: number) => { 
                fetchTableData(val, pageSize, sortStatus, filterValues);
              }
            } 
            onRecordsPerPageChange={
              (val: number) => { 
                fetchTableData(page, val, sortStatus, filterValues);
              }
            } 
          /> 
      </div>
    </div>
  );
}