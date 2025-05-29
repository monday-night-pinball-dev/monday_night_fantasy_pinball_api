/* eslint-disable dot-notation */

import { Combobox, Input, InputBase, TextInput, useCombobox } from "@mantine/core"; 
import { useEffect, useState } from "react";
import classes from "./EntityProfileComponents.module.css";  
import axios from "axios"; 
import { resolveOptionNameHydration, resolveOptionNameValue } from "../../Lib/profileFunctions";

export type FkLinkCreateParams = {
  searchUrl: string; 
  searchKey: string; 
  optionNameKeys: string[],
}

interface DefaultCreateComponentProps {
    itemKey: string,
    actualKey: string,
    title: string,  
    onChangeHandler: (key: string, value: string, actualKey: string) => void
}

interface FkLinkCreateComponentProps {
    itemKey: string,
    title: string,  
    params: FkLinkCreateParams 
    onChangeHandler: (key: string, value: string, actualKey: string) => void
}

export const DefaultCreateComponent: React.FC<DefaultCreateComponentProps> = ({     
    itemKey, 
    title, 
    onChangeHandler
}) => { 

  const [value, setValue] = useState<string>("");
  

  useEffect(() => { 
     onChangeHandler(itemKey, value, itemKey); 
  }, [value]);

  return (
    <div className={`${classes.entityProfileFieldBox} 'formValue'`} id={itemKey}>
        <div className={classes.entityProfileFieldBoxPropertyTitleSection}>
        {title}:
        </div>
        <div className={classes.entityProfileFieldBoxPropertyValueSection}>
            <TextInput
                type="text" 
                className={classes.entityProfileFieldBoxPropertyValueSectionTextArea}
                value={value || ""} 
                style={{ resize: 'none' }}  
                onChange={(e) => { 
                    setValue(e.target.value);
                }}
            /> 
        </div>
    </div>
  );  
} 

export const FkLinkCreateComponent: React.FC<FkLinkCreateComponentProps> = ({     
    itemKey,
    title, 
    params, 
    onChangeHandler
}) => { 
    

  const getAsyncData = async () => {
    const optionsArray: { id: string, name: string }[] = [];
   
    const searchUrl = new URL(`${import.meta.env.VITE_BASE_API_URL}${params.searchUrl}`);
 
    searchUrl.searchParams.set("page_length", "10");
    
    if(search)
    {
        searchUrl.searchParams.set(params.searchKey, search);
    }
    
    const hydration = resolveOptionNameHydration(params.optionNameKeys);
    
    const response = await axios.get(searchUrl.toString(), hydration ? { headers: { 'MNFP-Hydration': hydration } } : {});
  
    response.data.items.forEach((item: Record<string,any>) => 
        optionsArray.push({ 
            id: item["id"],
            name: resolveOptionNameValue(item, params.optionNameKeys) || ""
        }
    ));

    setOptions(optionsArray) 
  };
 
  const [value, setValue] = useState<string | null>(null);
  const [valueDisplay, setValueDisplay] = useState<string | null>(null);
  const [options, setOptions] = useState<{id:string, name: string}[]>([]); 
  const [search, setSearch] = useState('');

  const combobox = useCombobox({
    onDropdownClose: () => {
      combobox.resetSelectedOption();
      combobox.focusTarget();
      setSearch('');
    },

    onDropdownOpen: () => {
      combobox.focusSearchInput();
    },
  });
  
  useEffect(() => { 
    getAsyncData();
  }, []);

  useEffect(() => { 
    getAsyncData();
  }, [search]);
  
  useEffect(() => { 
    const name = options.find((option) => option.id === value)?.name || null
    setValueDisplay(name);
    onChangeHandler(itemKey, value || "", itemKey);
  }, [value]);
 
  return (
     <div className={classes.entityProfileFieldBox} id={itemKey}>
        <div className={classes.entityProfileFieldBoxPropertyTitleSection}>
            {title}:
        </div>
        <div className={classes.entityProfileFieldBoxPropertyValueSection}> 
            <Combobox 
            store={combobox}
            withinPortal={false}
            onOptionSubmit={(val) => {
                setValue(val);
                combobox.closeDropdown();
            }}
            >
            <Combobox.Target>
                <InputBase
                component="button"
                type="button"
                pointer
                rightSection={<Combobox.Chevron />}
                onClick={() => combobox.toggleDropdown()}
                rightSectionPointerEvents="none"
                >
                {valueDisplay || <Input.Placeholder>------------</Input.Placeholder>}
                </InputBase>
            </Combobox.Target>

            <Combobox.Dropdown>
                <Combobox.Search
                value={search}
                onChange={(event) => setSearch(event.currentTarget.value)}
                placeholder="Search"
                />
                <Combobox.Options>
                    {
                        options.length > 0 ? options.map((option) => ( 
                            <Combobox.Option value={option["id"]} key={option["id"]} >
                                {option["name"]}
                            </Combobox.Option>
                        )) 
                        :
                        <Combobox.Empty>Nothing found</Combobox.Empty>
                    } 
                </Combobox.Options>
            </Combobox.Dropdown>
            </Combobox>
        </div>
    </div>
  );
} 