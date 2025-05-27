import { ProfileEditTemplate, MnfpEntityEditProfile } from "@/Components/EntityProfileComponents/MnfpEntityEditProfile";
import {  useParams } from "react-router-dom";  
     

export const AdminSeasonProfileEditPage : React.FC = () => {
     
  const { id } = useParams();  
   

  const profileTemplate: ProfileEditTemplate = new ProfileEditTemplate([
 
      ['name', { title: 'Name' }],
      ['season_number', { title: 'Season Number' }],
      ['created_at', { title: 'Created At' }], 
    ]) 
  
  return (
    <div>
      <MnfpEntityEditProfile 
        entityId={id || ''} 
        entityApiName="seasons" 
        entityNameSingular="Season"   
        entityOutboundModelName="SeasonOutboundModel"
        entityInboundUpdateModelName="SeasonInboundUpdateModel"
        profileFieldTemplate={profileTemplate}
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}




