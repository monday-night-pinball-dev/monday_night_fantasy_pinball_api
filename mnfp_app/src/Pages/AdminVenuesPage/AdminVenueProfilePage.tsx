
import {  useEffect, useState } from "react";
import {  useParams } from "react-router-dom"; 
import { MnfpProfilePage, ProfileModes, ProfileTemplate, ProfileTemplateCreateItem, ProfileTemplateEditItem, ProfileTemplateReadItem } from "@/Components/EntityProfileComponents/MnfpEntityProfile";

     
export const combineUniqueArrays = (...arrays: any) => {
  const combinedArray = [].concat(...arrays);
  return [...new Set(combinedArray)];
}

type AdminVenueProfilePageProps = {
  mode?: ProfileModes;
}

export const AdminVenueProfilePage : React.FC<AdminVenueProfilePageProps> = ({mode}) => {
     
  const [profileMode, setProfileMode] = useState<ProfileModes>(ProfileModes.READ);
  const { id } = useParams();  
   

  const profileTemplate: ProfileTemplate = {
     readTemplate: new Map<string, ProfileTemplateReadItem>([
      ['name', { title: 'Name' }], 
      ['created_at', { title: 'Created At' }], 
    ]),
    createTemplate: new Map<string, ProfileTemplateCreateItem>([  
      ['name', { title: 'Name' }], 
    ]),
    editTemplate: new Map<string, ProfileTemplateEditItem>([
      ['name', { title: 'Name' }], 
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
        entityNamePlural="Venues"
        entityNameSingular="Venue" 
        entityInboundCreateModelName="VenueInboundCreateModel"
        entityInboundUpdateModelName="VenueInboundUpdateModel"
        entityOutboundModelName="VenueOutboundModel"
        mode={profileMode}
        profileFieldTemplate={profileTemplate}
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}