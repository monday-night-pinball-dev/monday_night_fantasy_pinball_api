import { MnfpEntityCreateProfile, ProfileCreateTemplate } from "@/Components/EntityProfileComponents/MnfpEntityCreateProfile"; 
import {  useParams } from "react-router-dom";  
     

export const AdminSeasonProfileCreatePage : React.FC = () => {
     
  const { id } = useParams();  
   

  const profileTemplate: ProfileCreateTemplate = new ProfileCreateTemplate([
 
      ['name', { title: 'Name' }],
      ['season_number', { title: 'Season Number' }], 
    ]) 
  
  return (
    <div>
      <MnfpEntityCreateProfile 
        entityId={id || ''} 
        entityApiName="seasons" 
        entityNameSingular="Season"   
        entityOutboundModelName="SeasonOutboundModel"  
        entityInboundCreateModelName="SeasonInboundCreateModel"
        profileFieldTemplate={profileTemplate}
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}




