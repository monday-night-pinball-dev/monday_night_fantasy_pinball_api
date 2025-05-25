/* eslint-disable dot-notation */

import { Combobox, Input, InputBase, TextInput, useCombobox } from "@mantine/core"; 
import { useEffect, useState } from "react";
import classes from "./EntityProfileComponents.module.css";

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
    params
}) => { 
 
  const getAsyncData = async () => {
    const response = await fetch(params.searchUrl);

    const data = await response.json(); 
  
    setOptions(data.items.map((item: Record<string,any>) => ({
        id: item["id"],
        name: item["name"]
    })));
  };
 
  const [value, setValue] = useState<string | null>(existingValue);
  const [options, setOptions] = useState<{id:string, name: string}[]>([]);

  const combobox = useCombobox({
    onDropdownClose: () => combobox.resetSelectedOption() 
  });
  
  useEffect(() => { 
    getAsyncData();
  }, []);
  
  useEffect(() => { 
    console.log("value", value);
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
                    onClick={() => combobox.toggleDropdown()}
                    rightSectionPointerEvents="none"
                    >
                    {value || <Input.Placeholder>Pick value</Input.Placeholder>}
                    </InputBase>
                </Combobox.Target>

                <Combobox.Dropdown>
                    <Combobox.Options> 
                        { 
                            options.map((option) => ( 
                                <Combobox.Option value={option["id"]} key={option["id"]} >
                                    {option["name"]}
                                </Combobox.Option>
                            ))    
                        } 
                    </Combobox.Options>
                </Combobox.Dropdown>
                </Combobox>
        </div>
    </div>
  );  
} 