import {  useParams } from "react-router-dom"; 
import { MnfpEntityReadProfile, ProfileReadTemplate } from "@/Components/EntityProfileComponents/MnfpEntityReadProfile";
     

export const AdminFantasyLeagueProfileReadPage : React.FC = () => {
     
  const { id } = useParams();  
   

  const profileTemplate: ProfileReadTemplate = new ProfileReadTemplate([
      ['name', { title: 'Name' }], 
      ['created_at', { title: 'Created At' }], 
    ])
  
  return (
    <div>
      <MnfpEntityReadProfile 
        entityId={id || ''} 
        entityApiName="fantasy_leagues" 
        entityNameSingular="Fantasy League"  
        entityOutboundModelName="FantasyLeagueOutboundModel" 
        profileFieldTemplate={profileTemplate}
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}