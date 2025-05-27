import { ProfileEditTemplate, MnfpEntityEditProfile } from "@/Components/EntityProfileComponents/MnfpEntityEditProfile";
import {  useParams } from "react-router-dom";  
 
export const AdminFantasyLeagueProfileEditPage : React.FC = () => {
     
  const { id } = useParams();  
   

  const profileTemplate: ProfileEditTemplate = new ProfileEditTemplate([ 
      ['name', { title: 'Name' }], 
      ['created_at', { title: 'Created At' }], 
    ]) 
  
  return (
    <div>
      <MnfpEntityEditProfile 
        entityId={id || ''} 
        entityApiName="fantasy_leagues"
        entityNameSingular="Fantasy League"   
        entityOutboundModelName="FantasyLeagueOutboundModel"
        entityInboundUpdateModelName="FantasyLeagueInboundUpdateModel"
        profileFieldTemplate={profileTemplate}
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}




