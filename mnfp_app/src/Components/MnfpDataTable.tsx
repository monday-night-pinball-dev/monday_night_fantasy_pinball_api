/* eslint-disable dot-notation */
import { ColumnDefTemplateItem, determineColumnDefs } from '@/Lib/tableFunctions';
import axios from 'axios'; 
import { DataTable, DataTableColumn, DataTableSortStatus } from 'mantine-datatable';
import { useEffect, useState } from 'react'; 

interface MnfpDataTableProps {
    outboundModelName: string,
    entityUrl: string,
    columnTemplate : Record<string, ColumnDefTemplateItem>,
    defaultSortColumn: string,
    defaultSortDirection: "asc" | "desc" ,
    hydration?: string[],
}

export const MnfpDataTable: React.FC<MnfpDataTableProps> = ({
    outboundModelName,
    entityUrl,
    columnTemplate,
    defaultSortColumn,
    defaultSortDirection,
    hydration,
}) => { 

    async function fetchTableData(pageIn: number, pageSizeIn: number, sortStatusIn: DataTableSortStatus<any>) { 

        const isDescending = sortStatusIn.direction === 'desc' ? 'true' : 'false';

        const response = await axios.get(`${entityUrl}?page=${pageIn}&page_length=${pageSizeIn}&sort_by=${String(sortStatusIn.columnAccessor)}&is_sort_descending=${isDescending}`, {
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
    }
 
  const [pageSize, setPageSize] = useState(15);
  const [page, setPage] = useState(1);
  const [totalRecords, setTotalRecords] = useState(0);
  const [records, setRecords] = useState([]);
  const [columns, setColumns] = useState<DataTableColumn[]>([]);

  const [sortStatus, setSortStatus] = useState<DataTableSortStatus<any>>({
    columnAccessor: defaultSortColumn,
    direction: defaultSortDirection,
  });
  
  useEffect(() => {
    const fetchColumnDefs = async () => {
      const schema = await axios.get(`${import.meta.env.VITE_BASE_API_URL}/openapi.json`);
      const columnDefs = determineColumnDefs(outboundModelName, schema.data, columnTemplate); 
      setColumns(columnDefs);
    }
    fetchColumnDefs();
    fetchTableData(page, pageSize, sortStatus);
  }, [])
  
  return (
    <div>
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
              fetchTableData(page, pageSize, val);
          }}
          sortStatus={sortStatus} 
          onPageChange={
            (val: number) => { 
              fetchTableData(val, pageSize, sortStatus);
            }
          } 
          onRecordsPerPageChange={
            (val: number) => { 
              fetchTableData(page, val, sortStatus);
            }
          } 
        /> 
    </div>
  );
}