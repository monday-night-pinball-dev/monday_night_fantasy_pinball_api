

import { Button, CopyButton, Grid } from "@mantine/core";
import axios from "axios";
import { JSX, useEffect, useState } from "react";
import { NavLink } from "react-router-dom";
import { FaArrowLeft, FaClipboard } from "react-icons/fa6"; 
import { DefaultEditComponent, FkLinkEditComponent, FkLinkEditParams } from "./EntityProfileEditComponents";
import { FkLinkReadComponent, DefaultReadComponent } from "./EntityProfileReadComponents";
 
export enum ProfileFieldReadTypes {
  STRING = 'STRING',
  DATE = 'DATE', 
  FK_LINK = 'FK_LINK',
}

export enum ProfileFieldEditTypes {
  STRING = 'STRING',
  FK_LINK = 'FK_LINK',
  DATE = 'DATE',
  ENUM = 'ENUM',
  NUMBER = 'NUMBER',
}

export enum ProfileFieldCreateTypes {
  STRING = 'STRING',
  FK_LINK = 'FK_LINK',
  DATE = 'DATE',
  ENUM = 'ENUM',
  NUMBER = 'NUMBER',
}

export enum ProfileModes {
  READ = 'READ',
  EDIT = 'EDIT',
  CREATE = 'CREATE',
}

export type ProfileFieldDateReadParams = {
    format: string;
    locale: string;
}

export type ProfileFieldEnumOption = {
    displayName: string;
    value: string;
}

export type ProfileFieldEnumEditParams = {
    options: ProfileFieldEnumOption[]
}

export type ProfileFieldEnumCreateParams = {
    options: ProfileFieldEnumOption[]
}

export type ProfileFieldNumberEditParams = {
  min?: number;
  max?: number;
  decimalPlaces?: number;
  allowNegative?: boolean;
}

export type ProfileFieldNumberCreateParams = {
  min?: number;
  max?: number;
  decimalPlaces?: number;
  allowNegative?: boolean;
}
 
export type FkLinkReadParams = {
  propertyKey: string;
  profileUrl: string;
} 

export type ProfileFieldReadTypeAndParams = {
  type: ProfileFieldReadTypes.DATE,
  typeParams?: ProfileFieldDateReadParams 
} | {
  type: ProfileFieldReadTypes.STRING 
} | {
  type: ProfileFieldReadTypes.FK_LINK,
  typeParams?: FkLinkReadParams
}
 
export type ProfileFieldEditTypeAndParams = {
  type: ProfileFieldEditTypes.DATE 
} | {
  type: ProfileFieldEditTypes.STRING
} | {
  type: ProfileFieldEditTypes.FK_LINK,
  typeParams?: FkLinkEditParams
} | {
  type: ProfileFieldEditTypes.ENUM,
  typeParams?: ProfileFieldEnumEditParams
} | {
  type: ProfileFieldEditTypes.NUMBER,
  typeParams?:  ProfileFieldNumberEditParams
}

export type ProfileFieldCreateTypeAndParams = {
  type: ProfileFieldCreateTypes.DATE 
} | {
  type: ProfileFieldCreateTypes.STRING 
} | {
  type: ProfileFieldCreateTypes.FK_LINK, 
} | {
  type: ProfileFieldCreateTypes.ENUM,
  typeParams?: ProfileFieldEnumCreateParams
} | {
  type: ProfileFieldCreateTypes.NUMBER,
  typeParams?: ProfileFieldNumberCreateParams
}

export type ProfileTemplateReadItem = {
  title: string;
  typeOverride?: ProfileFieldReadTypeAndParams;
}

export type ProfileTemplateEditItem = {
  title: string;
  typeOverride?: ProfileFieldEditTypeAndParams;
}

export type ProfileTemplateCreateItem = {
  title: string;
  typeOverride?: ProfileFieldCreateTypeAndParams;
}

export type ProfileFieldReadDef = {
  title: string;
  type: ProfileFieldReadTypeAndParams;
}

export type ProfileFieldEditDef = {
  title: string;
  is_editable?: boolean;
  type: ProfileFieldEditTypeAndParams
}

export type ProfileFieldCreateDef = {
  title: string;
  is_creatable?: boolean;
  type: ProfileFieldCreateTypeAndParams
}
 
export interface ProfilePageParams {
  mode: ProfileModes;
  entityNameSingular?: string;
  entityNamePlural?: string;
  entityId: string;
  baseApiUrl?: string;
  entityOutboundModelName: string;
  entityInboundCreateModelName: string;
  entityInboundUpdateModelName: string;
  profileFieldTemplate: ProfileTemplate;
 
}
 
export type ProfileTemplate = {
  readTemplate: Map<string, ProfileTemplateReadItem>;
  createTemplate: Map<string, ProfileTemplateCreateItem>;
  editTemplate: Map<string, ProfileTemplateEditItem>;
}  

export type ProfileFieldDefs = {
  read: Map<string, ProfileFieldReadDef>;
  create: Map<string, ProfileFieldCreateDef>;
  edit: Map<string, ProfileFieldEditDef>;
}
 
export const resolveReadType = (type: string) : ProfileFieldReadTypeAndParams => {
  switch(type) {
    case 'string':
      { 
        const returnVal : ProfileFieldReadTypeAndParams = { type: ProfileFieldReadTypes.STRING };
        return returnVal; 
      } 
    case 'date':
      {
        const returnVal : ProfileFieldReadTypeAndParams = {
          type: ProfileFieldReadTypes.DATE,
          typeParams: {
            format: 'MMM D YYYY',
            locale: 'en',
          }
        }
        return returnVal; 
      }
    default:
      { 
        const returnVal : ProfileFieldReadTypeAndParams = { type: ProfileFieldReadTypes.STRING };
        return returnVal; 
      } 
  }
}

export const resolveCreateType = (type: string) : ProfileFieldCreateTypeAndParams => {
  switch(type) {
    case 'string':
      { 
        const returnVal : ProfileFieldCreateTypeAndParams = { type: ProfileFieldCreateTypes.STRING };
        return returnVal; 
      } 
    case 'number': 
      {
        const returnVal: ProfileFieldCreateTypeAndParams = { 
          type: ProfileFieldCreateTypes.NUMBER,
          typeParams: { 
            decimalPlaces: 0,
            allowNegative: false
          }
        }
        return returnVal;
      }
    case 'date':
      {
        const returnVal : ProfileFieldCreateTypeAndParams = {
          type: ProfileFieldCreateTypes.DATE,
      
        }
        return returnVal; 
      }
    case 'fk_link':
      return { 
        type: ProfileFieldCreateTypes.FK_LINK
      };
    default:
      return { type: ProfileFieldCreateTypes.STRING};
  }
}

export const resolveEditType = (type: string) : ProfileFieldEditTypeAndParams => {
  switch(type) {
    case 'string':
      { 
        const returnVal : ProfileFieldEditTypeAndParams = { type: ProfileFieldEditTypes.STRING };
        return returnVal; 
      } 
    case 'number': 
      {
        const returnVal: ProfileFieldEditTypeAndParams = { 
          type: ProfileFieldEditTypes.NUMBER,
          typeParams: { 
            decimalPlaces: 0,
            allowNegative: false
          }
        }
        return returnVal;
      }
    case 'date':
      {
        const returnVal : ProfileFieldEditTypeAndParams = {
          type: ProfileFieldEditTypes.DATE 
        }
        return returnVal; 
      }
    case 'fk_link':
      return { 
        type: ProfileFieldEditTypes.FK_LINK,
      };
    default:
      return { type: ProfileFieldEditTypes.STRING};
  }
}

export const combineUniqueArrays = (...arrays: any) => {
  const combinedArray = [].concat(...arrays);
  return [...new Set(combinedArray)];
}

export const MnfpProfilePage : React.FC<ProfilePageParams> = ({
    mode,
    entityNameSingular,
    entityNamePlural, 
    entityId,
    baseApiUrl,
    entityOutboundModelName,
    entityInboundCreateModelName,
    entityInboundUpdateModelName, 
    profileFieldTemplate
}) => {
   
  function determinePropertyDefs(
    schema: any, 
    propertyTemplate: ProfileTemplate,
    entityOutboundModelName: string, 
    entityInboundCreateModelName: string, 
    entityInboundUpdateModelName?: string) {
    
    const outboundModelDef = schema.components.schemas[entityOutboundModelName].properties;
    const inboundCreateModelDef = schema.components.schemas[entityInboundCreateModelName].properties;
    const entityInboundUpdateModelDef = entityInboundUpdateModelName ? schema.components.schemas[entityInboundUpdateModelName].properties : undefined;

    const inboundCreateModelPropertyKeys = Object.keys(inboundCreateModelDef);
    const inboundUpdateModelPropertyKeys = entityInboundUpdateModelDef ? Object.keys(entityInboundUpdateModelDef) : [];
        
    const readFieldItems = new Map<string, ProfileFieldReadDef>();  
    const createFieldItems = new Map<string, ProfileFieldCreateDef>();  
    const editFieldItems = new Map<string, ProfileFieldEditDef>();
     
    profileFieldTemplate.readTemplate.keys().forEach((key: string) => {
      const columnTemplate = propertyTemplate.readTemplate.get(key);

      if(columnTemplate) {
 
        const read_type = resolveReadType(outboundModelDef[key].type) 
 
        const fieldItemReadDef: ProfileFieldReadDef = {  
          title: columnTemplate.title,
          type: columnTemplate.typeOverride ?? read_type, 
            
        }
  
        readFieldItems.set(key, fieldItemReadDef) 
      }
    });
 
    profileFieldTemplate.createTemplate.keys().forEach((key: string) => {
      const columnTemplate = propertyTemplate.createTemplate.get(key);

      if(columnTemplate) {
 
        const create_type = resolveCreateType(outboundModelDef[key].type) 
 
        const fieldItemCreateDef: ProfileFieldCreateDef = {  
            title: columnTemplate.title,
            type: columnTemplate.typeOverride ?? create_type, 
            is_creatable: inboundCreateModelPropertyKeys.includes(key)
        }

        createFieldItems.set(key, fieldItemCreateDef)
      } 
    });
  
    profileFieldTemplate.editTemplate.keys().forEach((key: string) => {
      const columnTemplate = propertyTemplate.editTemplate.get(key);

      if(columnTemplate) {
 
        const edit_type = resolveEditType(outboundModelDef[key].type) 
 
        const fieldItemEditDef: ProfileFieldEditDef = {  
            title: columnTemplate.title,
            type: columnTemplate.typeOverride ?? edit_type, 
            is_editable: inboundUpdateModelPropertyKeys.includes(key)

        }
        
        editFieldItems.set(key, fieldItemEditDef)
      } 
    });


    setProfileFieldDefs({
      read: readFieldItems,
      create: createFieldItems, 
      edit: editFieldItems
    });
 
  }
  

  async function renderSingleReadProfileField(key: string, value: any, columnDef: ProfileFieldReadDef) {
 
      if(columnDef?.type.type === ProfileFieldReadTypes.FK_LINK) {
 
        const params: FkLinkReadParams = {
          propertyKey: key,
          profileUrl: columnDef.type.typeParams?.profileUrl || ''
        }

        return (
            <FkLinkReadComponent propertyKey={key} title={columnDef.title} value={value} params={params}/>
        )
      }
        
      return (
        <DefaultReadComponent propertyKey={key} title={columnDef.title} value={value}/>
      ) 
  }

  async function ProfileFieldValueChangedHandler(key: string, value: string) {
    ProfileFieldValues[key] = value;  
  }

  async function renderSingleEditProfileField(key: string, value: any, columnDef: ProfileFieldEditDef) {
  
      if(columnDef?.type.type === ProfileFieldEditTypes.FK_LINK) {
        const params: FkLinkEditParams = { 
            optionNameKey: columnDef.type.typeParams?.optionNameKey || '', 
            searchKey: columnDef.type.typeParams?.searchKey || '',
            searchUrl: columnDef.type.typeParams?.searchUrl || '', 
        }

        return (
           <FkLinkEditComponent 
                itemKey={key}
                title={columnDef.title} 
                existingValue={value} 
                params={params}
                onChangeHandler={ProfileFieldValueChangedHandler}
            />
        )
      }
        
      return (
        <DefaultEditComponent 
          itemKey={key} 
          actualKey="BEEF"
          title={columnDef.title} 
          existingValue={value} 
          isEnabled={columnDef.is_editable || false}
          onChangeHandler={ProfileFieldValueChangedHandler}
        />
      )
    }  


  async function renderSingleCreateProfileField(key: string, value: any, columnDef: ProfileFieldCreateDef) {
   

      if(columnDef?.type.type === ProfileFieldCreateTypes.FK_LINK) {
        return (
          <span>
            CREATE 
          
              {value} 

            { 
              value &&
              <CopyButton value={value}>
                {({ copied, copy }) => (
                  <Button 
                    style={{ marginLeft: 5 }}   
                    size='compact-xs' 
                    color={copied ? 'teal' : 'blue'} 
                    onClick={copy}
                    variant="subtle"
                    title="Copy id"
                  >
                  {copied ? <FaClipboard/> : <FaClipboard/>}
                  </Button>
                )}
              </CopyButton> 
            }
          </span>
        )
      }
        
      return (
        <div>
          CREATE - 
          {columnDef.is_creatable ?
            <span style={{ color: 'green' }}>
              Creatable
            </span> : 
            <span style={{ color: 'red' }}>
              Not Creatable
            </span>
          }
          {key}: {value}
        </div>
      ) 
  }

  async function renderProfileFields(entity: any) {
    if(profileMode === ProfileModes.CREATE) {
      const kvps = profileFieldDefs?.create ? Array.from(profileFieldDefs?.create.entries()) : []
      const elements = kvps.map((kvp: any) => { 
        const def = kvp[1]
        const key = kvp[0]
        return( 
          entity[key] && def &&
          <Grid.Col span={{ base: 12, md: 6, lg: 4, sm: 12 }} key={key}>
            <div>
              {renderSingleCreateProfileField(key, entity[key], def)}
            </div> 
          </Grid.Col>  
        );
      })

      setProfileFields(elements);
    }
    else if(profileMode === ProfileModes.EDIT) {
      const kvps = profileFieldDefs?.edit ? Array.from(profileFieldDefs?.edit.entries()) : []
      const elements = kvps.map((kvp: any) => { 
        const def = kvp[1]
        const key = kvp[0]
        return( 
          entity[key] && def &&
          <Grid.Col span={{ base: 12, md: 6, lg: 4, sm: 12 }} key={key}>
            <div>
              {renderSingleEditProfileField(key, entity[key], def)}
            </div> 
          </Grid.Col>  
        );
      })

      setProfileFields(elements);
    }
    else {
      const kvps = profileFieldDefs?.read ? Array.from(profileFieldDefs?.read.entries()) : []
      const elements = kvps.map((kvp: any) => { 
        const def = kvp[1]
        const key = kvp[0]
        return( 
          entity[key] && def &&
          <Grid.Col span={{ base: 12, md: 6, lg: 4, sm: 12 }} key={key}>
            <div>
              {renderSingleReadProfileField(key, entity[key], def)}
            </div> 
          </Grid.Col>  
        );
      })

      setProfileFields(elements);
    }
  } 

  async function fetchEntityData() {
    const entityUrl = `${baseApiUrl}/${entityNamePlural?.toLocaleLowerCase()}/${entityId}`;
    const response = await axios.get(entityUrl);
    setEntity(response.data);
  }

  async function handleEntityChanged() {
    if(!entity) {
      return;
    }

    renderProfileFields(entity) 
  }

  async function sendUpdateToApi() { 
    const updateUrl = `${baseApiUrl}/${entityNamePlural?.toLocaleLowerCase()}/${entityId}`;
    const response = await axios.patch(updateUrl || '', ProfileFieldValues);
    setEntity(response.data);
  }
  
  
  const [entity, setEntity] = useState();
  const [ProfileFields, setProfileFields] = useState<(JSX.Element | undefined)[]>();
  const [profileFieldDefs, setProfileFieldDefs] = useState<ProfileFieldDefs>();   
  const [profileMode, setProfileMode] = useState<ProfileModes>(ProfileModes.READ);
  const [ProfileFieldValues] = useState<Record<string, any>>({});
     
  useEffect(() => {
    if(mode) {
      setProfileMode(mode);
    } 
    
    const fetchColumnDefs = async () => {
        const schema = await axios.get(`${import.meta.env.VITE_BASE_API_URL}/openapi.json`);
        determinePropertyDefs(
            schema.data, 
            profileFieldTemplate, 
            entityOutboundModelName, 
            entityInboundCreateModelName, 
            entityInboundUpdateModelName
        );
    }
 
    fetchColumnDefs(); 
    fetchEntityData() 
  }, [])

  useEffect(() => {
    handleEntityChanged();
  }, [entity])


  useEffect(() => {
    fetchEntityData();
  }, [profileMode])

  return (
    <div>

      <NavLink to={`/admin/${entityNamePlural}`}>
        <Button color="blue" size="s">
          <FaArrowLeft/>
        </Button>
      </NavLink>

      {
        profileMode === ProfileModes.READ && <Button
          onClick={() => {
            setProfileMode(ProfileModes.EDIT); 
          }}
          color="blue" size="s" style={{ marginLeft: 5 }}>
            Edit
        </Button>
      }
      
      <div>
        Admin {entityNameSingular} Profile Page for id: {entityId} 
          <CopyButton value={entityId!}>
            {({ copied, copy }) => (
                <Button 
                    style={{ marginLeft: 5 }}   
                    size='compact-xs' 
                    color={copied ? 'teal' : 'blue'} 
                    onClick={copy}
                    variant="subtle"
                    title="Copy id"
                >
                {copied ? <FaClipboard/> : <FaClipboard/>}
                </Button>
            )}
          </CopyButton> 
      </div>
       
      <Grid style={{ border: '1px solid lightGrey', padding: 10, marginTop: 10 }}>
        {ProfileFields}
      </Grid>

      <div>
        {
          profileMode === ProfileModes.EDIT &&
          <span>
            <Button
                onClick={() => {
                  setProfileMode(ProfileModes.READ); 
                }
              }
              color="grey" size="s" style={{ marginLeft: 5 }}>
              Cancel
            </Button>
            <Button
                onClick={() => {
                  sendUpdateToApi()
                  setProfileMode(ProfileModes.READ); 
                }
              }
              color="blue" size="s" style={{ marginLeft: 5 }}>
              Save Changes
            </Button>
          </span>
        }
      </div>
      <div>
        {
          profileMode === ProfileModes.CREATE &&
          <span>
            <NavLink to={`/admin/${entityNamePlural}`}>
              <Button 
                color="grey" size="s" style={{ marginLeft: 5 }}>
                Cancel
              </Button>
            </NavLink>
            <NavLink to={`/admin/${entityNamePlural}`}>
              <Button 
                color="blue" size="s" style={{ marginLeft: 5 }}>
                Submit
              </Button>
            </NavLink>
          </span>
        }
      </div>
    </div>
  )
}