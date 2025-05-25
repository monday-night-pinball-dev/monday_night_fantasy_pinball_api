
import {  useEffect, useState } from "react";
import {  useParams } from "react-router-dom"; 
import { MnfpProfilePage, ProfileModes, ProfileTemplate, ProfileTemplateCreateItem, ProfileTemplateEditItem, ProfileTemplateReadItem } from "@/Components/EntityProfileComponents/MnfpEntityProfile";

     
export const combineUniqueArrays = (...arrays: any) => {
  const combinedArray = [].concat(...arrays);
  return [...new Set(combinedArray)];
}

type AdminSeasonProfilePageProps = {
  mode?: ProfileModes;
}

export const AdminSeasonProfilePage : React.FC<AdminSeasonProfilePageProps> = ({mode}) => {
     
  const [profileMode, setProfileMode] = useState<ProfileModes>(ProfileModes.READ);
  const { id } = useParams();  
   

  const profileTemplate: ProfileTemplate = {
     readTemplate: new Map<string, ProfileTemplateReadItem>([
      ['name', { title: 'Name' }],
      ['season_number', { title: 'Season Number' }],
      ['created_at', { title: 'Created At' }], 
    ]),
    createTemplate: new Map<string, ProfileTemplateCreateItem>([  
      ['name', { title: 'Name' }],
      ['season_number', { title: 'Season Number' }],
    ]),
    editTemplate: new Map<string, ProfileTemplateEditItem>([
      ['name', { title: 'Name' }],
      ['season_number', { title: 'Season Number' }],
      ['created_at', { title: 'Created At' }], 
    ]),
  }

  useEffect(() => {
    if(mode) {
      setProfileMode(mode);
    } 
  }, [])
  
  return (
    <div>
      <MnfpProfilePage 
        entityId={id || ''} 
        entityNamePlural="Seasons"
        entityNameSingular="Season" 
        entityInboundCreateModelName="SeasonInboundCreateModel"
        entityInboundUpdateModelName="SeasonInboundUpdateModel"
        entityOutboundModelName="SeasonOutboundModel"
        mode={profileMode}
        profileFieldTemplate={profileTemplate}
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}