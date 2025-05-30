

import { Button, CopyButton, Grid } from "@mantine/core"; 
import { JSX, useEffect, useState } from "react";
import { useNavigate, NavLink } from "react-router-dom";
import { FaClipboard } from "react-icons/fa6"; 
import { DefaultEditComponent, FkLinkEditComponent, FkLinkEditParams, ProfileFieldEnumEditParams, ProfileFieldNumberEditParams } from "./EntityProfileEditComponents";
import { uiaxios } from "@/Lib/uiaxios";

export enum ProfileFieldEditTypes {
  STRING = 'STRING',
  FK_LINK = 'FK_LINK',
  DATE = 'DATE',
  ENUM = 'ENUM',
  NUMBER = 'NUMBER',
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
   
export type ProfileTemplateEditItem = {
  title: string;
  typeOverride?: ProfileFieldEditTypeAndParams;
}
  
export type ProfileFieldEditDef = {
  title: string;
  is_editable?: boolean;
  type: ProfileFieldEditTypeAndParams
}
 
 
export interface ProfilePageEditParams { 
  entityApiName: string;
  entityNameSingular: string; 
  entityId: string;
  baseApiUrl: string;  
  entityOutboundModelName: string;
  entityInboundUpdateModelName: string;

  profileFieldTemplate: ProfileEditTemplate;
 
}

 
export class ProfileEditTemplate extends  Map<string, ProfileTemplateEditItem> {}

export class ProfileFieldEditDefs extends  Map<string, ProfileFieldEditDef> {}
   
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
 

export const MnfpEntityEditProfile : React.FC<ProfilePageEditParams> = ({ 
    entityApiName,
    entityNameSingular,  
    entityId,
    baseApiUrl, 
    entityOutboundModelName,
    entityInboundUpdateModelName, 
    profileFieldTemplate
}) => {
   
  function determinePropertyDefs(
    schema: any, 
    propertyTemplate: ProfileEditTemplate,
    entityOutboundModelName: string, 
    entityInboundUpdateModelName?: string) {
    
    const outboundModelDef = schema.components.schemas[entityOutboundModelName].properties;
    const entityInboundUpdateModelDef = entityInboundUpdateModelName ? schema.components.schemas[entityInboundUpdateModelName].properties : undefined;

    const inboundUpdateModelPropertyKeys = entityInboundUpdateModelDef ? Object.keys(entityInboundUpdateModelDef) : [];

    const editFieldItems = new Map<string, ProfileFieldEditDef>();
      
    profileFieldTemplate.keys().forEach((key: string) => {
      const columnTemplate = propertyTemplate.get(key);

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


    return editFieldItems;
 
  }
    
  async function ProfileFieldValueChangedHandler(key: string, value: string) {
    ProfileFieldValues[key] = value;  
  }

  async function renderSingleEditProfileField(key: string, value: any, columnDef: ProfileFieldEditDef) {
  
      if(columnDef?.type.type === ProfileFieldEditTypes.FK_LINK) {
        const params: FkLinkEditParams = { 
            optionNameKeys: columnDef.type.typeParams?.optionNameKeys || [], 
            searchKey: columnDef.type.typeParams?.searchKey || '',
            searchUrl: columnDef.type.typeParams?.searchUrl || '', 
        }

        return (
           <FkLinkEditComponent 
                itemKey={key}
                title={columnDef.title} 
                existingValue={value} 
                params={params}
                isEnabled={columnDef.is_editable || false}
                error={profileFieldErrors[key]}
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
          error={profileFieldErrors[key]}
          onChangeHandler={ProfileFieldValueChangedHandler}
        />
      )
    }  

 

  async function renderProfileFields() {
     
    const kvps = profileFieldDefs ? Array.from(profileFieldDefs.entries()) : []
    const elements = kvps.map((kvp: any) => { 
      const def = kvp[1]
      const key = kvp[0]
      return( 
        
        <Grid.Col span={{ base: 12, md: 6, lg: 4, sm: 12 }} key={key}>
          <div>
            {renderSingleEditProfileField(key, entity?.[key], def)}
          </div> 
        </Grid.Col>  
      );
    })

    setProfileFields(elements);
    
  } 

  async function fetchEntityData() {
 
    const schema = await uiaxios.get(`${import.meta.env.VITE_BASE_API_URL}/openapi.json`, {});
   
    const profileFields = determinePropertyDefs(
        schema.data, 
        profileFieldTemplate,  
        entityOutboundModelName,
        entityInboundUpdateModelName
    );

    const entityUrl = `${baseApiUrl}/${entityApiName}/${entityId}`;
    const response = await uiaxios.get(entityUrl, {});

    setProfileFieldDefs(profileFields);
    setEntity(response.data);
  }

  async function handleEntityChanged() {
    if(!entity) {
      return;
    }

    renderProfileFields() 
  }

  async function sendUpdateToApi() { 
    const updateUrl = `${baseApiUrl}/${entityApiName?.toLocaleLowerCase()}/${entityId}`;
    const response = await uiaxios.patch(updateUrl || '', ProfileFieldValues, {});
      
    if(response.status === 200) { 
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
      setEntity(response.data);
    }
  }
  
   
  const navigate = useNavigate();
  const [entity, setEntity] = useState();
  const [ProfileFields, setProfileFields] = useState<(JSX.Element | undefined)[]>();
  const [profileFieldDefs, setProfileFieldDefs] = useState<ProfileFieldEditDefs>();    
  const [ProfileFieldValues] = useState<Record<string, any>>({});
  const [profileFieldErrors, setProfileFieldErrors] = useState<Record<string, string>>({});
     
  useEffect(() => { 
    fetchEntityData() 
  }, [])

  useEffect(() => {
    handleEntityChanged();
  }, [entity])

  useEffect(() => {
    if(profileFieldDefs) {
      renderProfileFields();
    }
  }, [profileFieldDefs, profileFieldErrors]);
 
  return (
    <div>
 
      <div>
        Admin {entityNameSingular} Edit Page for {entityNameSingular}: {entityId} 
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
 
            <Button
                onClick={() => {
                  sendUpdateToApi()
                }
              }
              color="blue" size="s" style={{ marginLeft: 5 }}>
              Save Changes
            </Button> 
          </span>
       
      </div>
      
    </div>
  )
}