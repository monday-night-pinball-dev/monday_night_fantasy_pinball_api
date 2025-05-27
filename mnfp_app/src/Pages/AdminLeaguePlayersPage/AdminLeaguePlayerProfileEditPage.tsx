import {  useParams } from "react-router-dom"; 
import { MnfpEntityEditProfile, ProfileEditTemplate, ProfileFieldEditTypes } from "@/Components/EntityProfileComponents/MnfpEntityEditProfile";

     
  
export const AdminLeaguePlayerProfileEditPage : React.FC = () => {
      
  const { id } = useParams();  
     
  const profileTemplate: ProfileEditTemplate = new ProfileEditTemplate([
      ['name', { title: 'Name' }],
      ['global_mnp_id', { title: 'MNP ID' }],
      ['league_team_id', {
         title: 'League Team', 
         typeOverride: {
            type: ProfileFieldEditTypes.FK_LINK,
            typeParams: { 
              optionNameKey: 'name',
              searchKey: 'name_like',
              searchUrl: '/league_teams',
        
            } 
          } 
        }],
      ['created_at', { title: 'Created At' }], 
    ])
  
  
  return (
    <div>
      <MnfpEntityEditProfile  
        entityId={id || ''} 
        entityApiName="league_players" 
        entityNameSingular="LeaguePlayer"   
        entityInboundUpdateModelName="LeaguePlayerInboundUpdateModel"
        
        entityOutboundModelName="LeaguePlayerOutboundModel"  
        profileFieldTemplate={profileTemplate} 
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}