

import { Button, CopyButton, Grid } from "@mantine/core"; 
import { uiaxios } from "../../Lib/uiaxios"
import { JSX, useEffect, useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { FaClipboard } from "react-icons/fa6";  
import { DefaultCreateComponent, FkLinkCreateComponent, FkLinkCreateParams } from "./EntityProfileCreateComponents";
 

export enum ProfileFieldCreateTypes {
  STRING = 'STRING',
  FK_LINK = 'FK_LINK',
  DATE = 'DATE',
  ENUM = 'ENUM',
  NUMBER = 'NUMBER',
}
   
export type ProfileFieldEnumOption = {
    displayName: string;
    value: string;
}

export type ProfileFieldEnumCreateParams = {
    options: ProfileFieldEnumOption[]
} 

export type ProfileFieldNumberCreateParams = {
  min?: number;
  max?: number;
  decimalPlaces?: number;
  allowNegative?: boolean;
}
   
export type ProfileFieldCreateTypeAndParams = {
  type: ProfileFieldCreateTypes.DATE 
} | {
  type: ProfileFieldCreateTypes.STRING
} | {
  type: ProfileFieldCreateTypes.FK_LINK,
  typeParams?: FkLinkCreateParams
} | {
  type: ProfileFieldCreateTypes.ENUM,
  typeParams?: ProfileFieldEnumCreateParams
} | {
  type: ProfileFieldCreateTypes.NUMBER,
  typeParams?:  ProfileFieldNumberCreateParams
}
   
export type ProfileTemplateCreateItem = {
  title: string;
  typeOverride?: ProfileFieldCreateTypeAndParams;
}
  
export type ProfileFieldCreateDef = {
  title: string;
  isCreatable?: boolean;
  type: ProfileFieldCreateTypeAndParams
}
 
 
export interface ProfilePageCreateParams { 
  entityApiName: string;
  entityNameSingular: string; 
  entityId: string;
  baseApiUrl: string;  
  entityOutboundModelName: string;
  entityInboundCreateModelName: string; 
  profileFieldTemplate: ProfileCreateTemplate;
 
}
 
export class ProfileCreateTemplate extends  Map<string, ProfileTemplateCreateItem> {}

export class ProfileFieldCreateDefs extends  Map<string, ProfileFieldCreateDef> {}
   
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
          type: ProfileFieldCreateTypes.DATE 
        }
        return returnVal; 
      }
    case 'fk_link':
      return { 
        type: ProfileFieldCreateTypes.FK_LINK,
      };
    default:
      return { type: ProfileFieldCreateTypes.STRING};
  }
}
 

export const MnfpEntityCreateProfile : React.FC<ProfilePageCreateParams> = ({ 
    entityApiName,
    entityNameSingular,  
    entityId,
    baseApiUrl, 
    entityOutboundModelName,
    entityInboundCreateModelName, 
    profileFieldTemplate
}) => {
   
  function determinePropertyDefs(
    schema: any, 
    propertyTemplate: ProfileCreateTemplate,
    entityOutboundModelName: string, 
    entityInboundCreateModelName?: string) {
    
    const outboundModelDef = schema.components.schemas[entityOutboundModelName].properties;
    const entityInboundCreateModelDef = entityInboundCreateModelName ? schema.components.schemas[entityInboundCreateModelName].properties : undefined;

    const inboundCreateModelPropertyKeys = entityInboundCreateModelDef ? Object.keys(entityInboundCreateModelDef) : [];

    const createFieldItems = new Map<string, ProfileFieldCreateDef>();
      
    profileFieldTemplate.keys().forEach((key: string) => {
      const columnTemplate = propertyTemplate.get(key);

      if(columnTemplate) {
 
        const edit_type = resolveCreateType(outboundModelDef[key].type) 
 
        const fieldItemCreateDef: ProfileFieldCreateDef = {  
            title: columnTemplate.title,
            type: columnTemplate.typeOverride ?? edit_type, 
            isCreatable: inboundCreateModelPropertyKeys.includes(key)
        }
        
        createFieldItems.set(key, fieldItemCreateDef)
      } 
    });

    return createFieldItems;
  }
    
  async function ProfileFieldValueChangedHandler(key: string, value: string) {
    profileFieldValues[key] = value;  
  }

  async function renderSingleCreateProfileField(key: string, columnDef: ProfileFieldCreateDef) {
  
      if(columnDef?.type.type === ProfileFieldCreateTypes.FK_LINK) {
        const params: FkLinkCreateParams = { 
            optionNameKeys: columnDef.type.typeParams?.optionNameKeys || [], 
            searchKey: columnDef.type.typeParams?.searchKey || '',
            searchUrl: columnDef.type.typeParams?.searchUrl || '', 
        }

        return (
           <FkLinkCreateComponent 
                itemKey={key}
                title={columnDef.title}  
                params={params} 
                error={profileFieldErrors[key]}
                onChangeHandler={ProfileFieldValueChangedHandler}
            />
        )
      }
        
      return (
        <DefaultCreateComponent 
          itemKey={key}  
          title={columnDef.title}  
          error={profileFieldErrors[key]}
          onChangeHandler={ProfileFieldValueChangedHandler}
        />
      )
    }  

  async function sendCreateToApi() { 
    const createUrl = `${baseApiUrl}/${entityApiName?.toLocaleLowerCase()}`;
    const response = await uiaxios.post(createUrl || '', profileFieldValues);

    
 
    if(response.status === 201) { 
      navigate(`/admin/${entityApiName}/${response.data.id}`);
    }
    else
    {
      const errorsRecord : Record<string,string>= {}

      if(response.status === 422) {
        const errors = response.data.detail;

        errors.forEach((error: any) => {
          const errorLocation = error.loc[1]
          errorsRecord[errorLocation] = error.msg;
          
        });
      
      }
      else {
        console.error('Error creating entity:', response);
      }

      setProfileFieldErrors(errorsRecord); // Trigger re-render with errors 
    }
  }

  async function renderProfileFields() {
     
    const kvps = profileFieldDefs ? Array.from(profileFieldDefs.entries().filter((x)=> x[1].isCreatable)) : []
    const elements = kvps.map((kvp: any) => { 
      const def = kvp[1]
      const key = kvp[0]
      return( 
        
        <Grid.Col span={{ base: 12, md: 6, lg: 4, sm: 12 }} key={key}>
          <div>
            {renderSingleCreateProfileField(key, def)}
          </div> 
        </Grid.Col>  
      );
    })

    setProfileFields(elements);
    
  } 

  async function fetchEntitySchema() {
 
    const schema = await uiaxios.get(`${import.meta.env.VITE_BASE_API_URL}/openapi.json`,{});
   
    const profileFields = determinePropertyDefs(
        schema.data, 
        profileFieldTemplate,  
        entityOutboundModelName,
        entityInboundCreateModelName
    ); 

    setProfileFieldDefs(profileFields); 
  }
 
 
  const [profileFields, setProfileFields] = useState<(JSX.Element | undefined)[]>();
  const [profileFieldDefs, setProfileFieldDefs] = useState<ProfileFieldCreateDefs>();    
  const [profileFieldValues] = useState<Record<string, any>>({});
  const [profileFieldErrors, setProfileFieldErrors] = useState<Record<string, string>>({});
     
  const navigate = useNavigate();

  useEffect(() => { 
    fetchEntitySchema() 
  }, [])

  useEffect(() => {
    if(profileFieldDefs) {
      renderProfileFields();
    }
  }, [profileFieldDefs, profileFieldErrors]);
 
  return (
    <div>
 
      <div>
        Admin {entityNameSingular} Create Page for {entityNameSingular}: {entityId} 
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
        {profileFields}
      </Grid>

      <div> 
          
          <span>
            <NavLink to={`/admin/${entityApiName}/${entityId}`}>
              <Button
                  onClick={() => { 
                  }
                }
                color="grey" size="s" style={{ marginLeft: 5 }}>
                Cancel
              </Button>
            </NavLink>

            <NavLink to={`/admin/${entityApiName}/${entityId}`}>
              <Button
                  onClick={(e) => {
                    e.preventDefault();
                    sendCreateToApi();
                  }
                }
                color="blue" size="s" style={{ marginLeft: 5 }}>
                Save Changes
              </Button>
            </NavLink>
          </span>
       
      </div>
      
    </div>
  )
}