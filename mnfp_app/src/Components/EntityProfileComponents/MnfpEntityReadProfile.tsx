

import { Button, CopyButton, Grid } from "@mantine/core";
import axios, { AxiosResponse } from "axios";
import { JSX, useEffect, useState } from "react";
import { NavLink } from "react-router-dom";
import { FaArrowLeft, FaClipboard } from "react-icons/fa6";  
import { FkLinkReadComponent, DefaultReadComponent, FkLinkReadParams } from "./EntityProfileReadComponents";
 
export enum ProfileFieldReadTypes {
  STRING = 'STRING',
  DATE = 'DATE', 
  FK_LINK = 'FK_LINK',
} 
  
export type ProfileFieldDateReadParams = {
    format: string;
    locale: string;
}

export type ProfileFieldEnumOption = {
    displayName: string;
    value: string;
}  

export type ProfileFieldReadTypeAndParams = {
  type: ProfileFieldReadTypes.DATE,
  typeParams?: ProfileFieldDateReadParams 
} | {
  type: ProfileFieldReadTypes.STRING 
} | {
  type: ProfileFieldReadTypes.FK_LINK,
  typeParams: FkLinkReadParams
}
  
export type ProfileTemplateReadItem = {
  title: string;
  typeOverride?: ProfileFieldReadTypeAndParams;
}
 

export type ProfileFieldReadDef = {
  title: string;
  type: ProfileFieldReadTypeAndParams;
}
 
export interface ProfileReadPageParams { 
  entityApiName: string;
  entityNameSingular: string; 
  entityId: string;
  baseApiUrl: string;
  entityOutboundModelName: string; 
  profileFieldTemplate: ProfileReadTemplate; 
  hideEditButton?: boolean; 
}
 
export class ProfileReadTemplate extends Map<string, ProfileTemplateReadItem> {}
  
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

export const MnfpEntityReadProfile : React.FC<ProfileReadPageParams> = ({
    entityApiName, 
    entityNameSingular, 
    entityId,
    baseApiUrl,
    entityOutboundModelName, 
    profileFieldTemplate,
    hideEditButton
}) => {
   
  function determinePropertyDefs(
    schema: any, 
    propertyTemplate: ProfileReadTemplate,
    entityOutboundModelName: string): Map<string, ProfileFieldReadDef> {
    
    const outboundModelDef = schema.components.schemas[entityOutboundModelName].properties;
 
    const readFieldItems = new Map<string, ProfileFieldReadDef>();   
     
    profileFieldTemplate.keys().forEach((key: string) => {
      const columnTemplate = propertyTemplate.get(key);

      if(columnTemplate) {
 
        const read_type = resolveReadType(outboundModelDef[key].type) 
 
        const fieldItemReadDef: ProfileFieldReadDef = {  
          title: columnTemplate.title,
          type: columnTemplate.typeOverride ?? read_type, 
            
        }
  
        readFieldItems.set(key, fieldItemReadDef) 
      }
    });
   
    return readFieldItems;
 
  }
   
  async function renderSingleReadProfileField(key: string, entity: Record<string,any>, columnDef: ProfileFieldReadDef) {
 
      if(columnDef?.type.type === ProfileFieldReadTypes.FK_LINK) {
 
        const params: FkLinkReadParams = {
          propertyKey: key,
          profileUrl: columnDef.type.typeParams.profileUrl,
          displayKey: columnDef.type.typeParams.displayKey, 
        } 

        const hydratedObjectKey = key.substring(0, key.length-3);

        const hydratedObject = entity[hydratedObjectKey];

        const displayValue = hydratedObject && hydratedObject[columnDef.type.typeParams.displayKey] ? hydratedObject[columnDef.type.typeParams.displayKey] : null;

        return (
            <FkLinkReadComponent propertyKey={key} title={columnDef.title} value={entity[key]} params={params} displayValue={displayValue}/>
        )
      }
        
      return (
        <DefaultReadComponent propertyKey={key} title={columnDef.title} value={entity[key]}/>
      ) 
  } 
  
  async function renderProfileFields(entity: any) {
     
      const kvps = profileFieldDefs ? Array.from(profileFieldDefs?.entries()) : []
      const elements = kvps.map((kvp: any) => { 
        const def = kvp[1]
        const key = kvp[0]
        return( 
          
          <Grid.Col span={{ base: 12, md: 6, lg: 4, sm: 12 }} key={key}>
            <div>
              {renderSingleReadProfileField(key, entity, def)}
            </div> 
          </Grid.Col>  
          
        );
      })

      setProfileFields(elements);
   
  }  

  async function fetchEntityData() {

    const schema = await axios.get(`${import.meta.env.VITE_BASE_API_URL}/openapi.json`);
     
    const profileFieldDefsLocal = determinePropertyDefs(
        schema.data,
        profileFieldTemplate,
        entityOutboundModelName
    );

    const fkLinkProps: string[] = []
    
    if(profileFieldDefsLocal) {
      for  (const [key, def] of profileFieldDefsLocal.entries()) {
        if(def.type.type === ProfileFieldReadTypes.FK_LINK) {
          const hydration_key = key.substring(0, key.length-3);
          fkLinkProps.push(hydration_key);
        }
      }
    }

    const entityUrl = `${baseApiUrl}/${entityApiName?.toLocaleLowerCase()}/${entityId}`;
    
    let response: AxiosResponse;

    if(fkLinkProps.length > 0) {
      response= await axios.get(entityUrl,
        {
          headers: {
            'MNFP-Hydration': fkLinkProps.join(',')
          }
        }
      );
    }
    else{
      response = await axios.get(entityUrl);
    }

    setProfileFieldDefs(profileFieldDefsLocal);
    setEntity(response.data);
    
  }

  async function handleEntityChanged() {
    if(!entity) {
      return;
    }
    
    renderProfileFields(entity) 
  }
 
  
  
  const [entity, setEntity] = useState();
  const [profileFields, setProfileFields] = useState<(JSX.Element | undefined)[]>(); 
  const [profileFieldDefs, setProfileFieldDefs] = useState<Map<string, ProfileFieldReadDef>>();   
     
  useEffect(() => {
    const Do = async () => {
        
      await fetchEntityData(); 
    } 

    Do();
  }, [])

  useEffect(() => {
    handleEntityChanged();
  }, [entity])


  return (
    <div>

      <NavLink to={`/admin/${entityApiName}`}>
        <Button color="blue" size="s">
          <FaArrowLeft/>
        </Button>
      </NavLink>

      {
        !hideEditButton && 
        <NavLink to={`/admin/${entityApiName}/${entityId}/edit`}>
          <Button color="blue" size="s">
            Edit
          </Button>
        </NavLink>
      }

      <div>
        Admin Profile Page for {entityNameSingular}: {entityId} 
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
 
    </div>
  )
}