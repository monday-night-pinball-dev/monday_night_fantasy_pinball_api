

import { Grid } from "@mantine/core";  
import { JSX, useEffect, useState } from "react";  
import { DefaultFilterComponent, DefaultFilterParams, FkLinkFilterComponent, FkLinkFilterParams } from "./MnfpFilterComponents";
 

export enum FilterTypes {
  STRING = 'STRING',
  FK_LINK = 'FK_LINK',
  DATE = 'DATE',
  ENUM = 'ENUM',
  NUMBER = 'NUMBER',
}
   
export type FilterEnumOption = {
    displayName: string;
    value: string;
}

export type FilterEnumParams = {
    options: FilterEnumOption[]
} 

export type FilterNumberParams = {
  decimalPlaces?: number;
  allowNegative?: boolean;
}

export type FilterStringParams = {
  searchKey: string;
}
    
export type FilterTemplateItem = 
{
  title: string,
  type: FilterTypes.DATE 
  typeParams?: never
} | {
  title: string,
  type: FilterTypes.STRING,
  typeParams?: FilterStringParams
} | {
  title: string,
  type: FilterTypes.FK_LINK,
  typeParams?: FkLinkFilterParams
} | {
  title: string,
  type: FilterTypes.ENUM,
  typeParams?: FilterEnumParams
} | {
  title: string,
  type: FilterTypes.NUMBER,
  typeParams?:  FilterNumberParams
}
  
   
 
export interface FilterParams {  
  filterTemplate: FilterTemplate;
  onFilterChange: (filterValues: Record<string,string>) => void;
}
 
export class FilterTemplate extends Map<string, FilterTemplateItem> {}
  
export const MnfpFilters : React.FC<FilterParams> = ({ 
    filterTemplate,
    onFilterChange
}) => {
    
  async function filterChangedHandler(_key: string, value: string, searchKey: string) {
    filterValues[searchKey] = value;  
    onFilterChange(filterValues);
  }

  async function renderSingleFilter(key: string, filterDef: FilterTemplateItem) {
  
      if(filterDef?.type === FilterTypes.FK_LINK) {
        const params: FkLinkFilterParams = { 
            optionNameKeys: filterDef.typeParams?.optionNameKeys || [], 
            searchKey: filterDef.typeParams?.searchKey || '',
            searchUrl: filterDef.typeParams?.searchUrl || '', 
        }

        return (
           <FkLinkFilterComponent 
                itemKey={key}
                title={filterDef.title}  
                params={params}  
                onChangeHandler={filterChangedHandler}
            />
        )
      }
        
      return (
        <DefaultFilterComponent 
          itemKey={key}  
          title={filterDef.title}   
          searchKey={(filterDef.typeParams as DefaultFilterParams)?.searchKey || ''}
          onChangeHandler={filterChangedHandler}
        />
      )
    }  

  async function renderFilters() {
     
    const kvps = filterTemplate ? Array.from(filterTemplate.entries()) : []
    const elements = kvps.map((kvp: any) => { 
      const def = kvp[1]
      const key = kvp[0]
      return( 
        
        <Grid.Col span={{ base: 12, md: 4, lg: 2, sm: 12 }} key={key}>
          <div>
            {renderSingleFilter(key, def)}
          </div> 
        </Grid.Col>  
      );
    })

    setFilters(elements);
    
  } 
  
  const [filters, setFilters] = useState<(JSX.Element | undefined)[]>();
  const [filterValues] = useState<Record<string, any>>({}); 

  useEffect(() => {   
    renderFilters();
  }, [])
 
  return (
    <div>
      Filters:
      <Grid style={{ border: '1px solid lightGrey', padding: 10, marginTop: 10 }}>
        {filters}
      </Grid>
      
    </div>
  )
}