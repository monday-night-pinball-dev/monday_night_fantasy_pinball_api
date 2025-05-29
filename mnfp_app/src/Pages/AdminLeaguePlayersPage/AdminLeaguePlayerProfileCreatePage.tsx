import { MnfpEntityCreateProfile, ProfileCreateTemplate, ProfileFieldCreateTypes } from "@/Components/EntityProfileComponents/MnfpEntityCreateProfile";
import {  useParams } from "react-router-dom"; 

     
  
export const AdminLeaguePlayerProfileCreatePage : React.FC = () => {
      
  const { id } = useParams();  
     
  const profileTemplate: ProfileCreateTemplate = new ProfileCreateTemplate([
      ['name', { title: 'Name' }],
      ['global_mnp_id', { title: 'MNP ID' }],
      ['league_team_id', {
         title: 'League Team', 
         typeOverride: {
            type: ProfileFieldCreateTypes.FK_LINK,
            typeParams: { 
              optionNameKeys: ['name'],
              searchKey: 'name_like',
              searchUrl: '/league_teams',
        
            } 
          } 
        }], 
    ])
  
  
  return (
    <div>
      <MnfpEntityCreateProfile  
        entityId={id || ''} 
        entityApiName="league_players" 
        entityNameSingular="LeaguePlayer"    
        entityInboundCreateModelName="LeaguePlayerInboundCreateModel"
        entityOutboundModelName="LeaguePlayerOutboundModel"  
        profileFieldTemplate={profileTemplate} 
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}