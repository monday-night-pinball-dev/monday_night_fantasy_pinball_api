import { ProfileCreateTemplate, MnfpEntityCreateProfile } from "@/Components/EntityProfileComponents/MnfpEntityCreateProfile";
import {  useParams } from "react-router-dom";  
 
export const AdminFantasyLeagueProfileCreatePage : React.FC = () => {
     
  const { id } = useParams();  
    
  const profileTemplate: ProfileCreateTemplate = new ProfileCreateTemplate([ 
    ['name', { title: 'Name' }],  
  ]) 
  
  return (
    <div>
      <MnfpEntityCreateProfile 
        entityId={id || ''} 
        entityApiName="fantasy_leagues"
        entityNameSingular="Fantasy League"   
        entityOutboundModelName="FantasyLeagueOutboundModel" 
        entityInboundCreateModelName="FantasyLeagueInboundCreateModel"
        profileFieldTemplate={profileTemplate}
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}




