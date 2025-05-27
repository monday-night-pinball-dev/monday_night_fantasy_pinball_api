/* eslint-disable dot-notation */

import { Combobox, Input, InputBase, TextInput, useCombobox } from "@mantine/core"; 
import { useEffect, useState } from "react";
import classes from "./EntityProfileComponents.module.css";  
import axios from "axios";

export type FkLinkEditParams = {
  searchUrl: string; 
  searchKey: string; 
  optionNameKey: string,
}

interface DefaultEditComponentProps {
    itemKey: string,
    actualKey: string,
    title: string, 
    existingValue: string
    isEnabled: boolean,
    onChangeHandler: (key: string, value: string, actualKey: string) => void
}

interface FkLinkEditComponentProps {
    itemKey: string,
    title: string, 
    existingValue: string,
    params: FkLinkEditParams
    isEnabled: boolean,
    onChangeHandler: (key: string, value: string, actualKey: string) => void
}

export const DefaultEditComponent: React.FC<DefaultEditComponentProps> = ({     
    itemKey, 
    title,
    existingValue,
    isEnabled,
    onChangeHandler
}) => { 

  const [value, setValue] = useState<string>(existingValue);
  

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
                disabled={!isEnabled}
                readOnly={!isEnabled}
                style={{ resize: 'none' }}  
                onChange={(e) => {
                    console.log("value", e.target.value);
                    setValue(e.target.value);
                }}
            /> 
        </div>
    </div>
  );  
} 

export const FkLinkEditComponent: React.FC<FkLinkEditComponentProps> = ({     
    itemKey,
    title,
    existingValue,
    params,
    isEnabled,
    onChangeHandler
}) => { 
 
  const getAsyncData = async (existingValue? : string) => {
    const optionsArray: {id:string, name: string}[] = [];

    console.log("getAsyncData called with existingValue:", existingValue);

    if(existingValue)
    {
        const retrieveUrl = new URL(`${import.meta.env.VITE_BASE_API_URL}${params.searchUrl}/${existingValue}`);
        const retrieveResponse = await axios.get(retrieveUrl.toString());

        if(retrieveResponse.status === 200) { 
            console.log("retrieveData.id:", retrieveResponse.data.id);

            optionsArray.push({
                id: retrieveResponse.data.id,
                name: retrieveResponse.data[params.optionNameKey] 
            });
        }
    }

    const searchUrl = new URL(`${import.meta.env.VITE_BASE_API_URL}${params.searchUrl}`);

    searchUrl.searchParams.set("page_length", "10");
    
    if(search)
    {
        searchUrl.searchParams.set(params.searchKey, search);
    }

    const response = await axios.get(searchUrl.toString());
  
    response.data.items.forEach((item: Record<string,any>) => 
        optionsArray.push({ 
            id: item["id"],
            name: item[params.optionNameKey]
        }
    ));

    setOptions(optionsArray)

    if(existingValue) {
        setValue(existingValue);
    } 
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
    getAsyncData(existingValue);
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
            disabled={!isEnabled}
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