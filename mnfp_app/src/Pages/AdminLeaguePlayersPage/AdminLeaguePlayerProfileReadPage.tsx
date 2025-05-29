import {  useParams } from "react-router-dom";  
import { MnfpEntityReadProfile, ProfileFieldReadTypes, ProfileReadTemplate } from "@/Components/EntityProfileComponents/MnfpEntityReadProfile";
 
export const AdminLeaguePlayerProfileReadPage : React.FC = () => {
      
  const { id } = useParams();  
     
  const profileTemplate: ProfileReadTemplate = new ProfileReadTemplate([
      ['name', { title: 'Name' }],
      ['global_mnp_id', { title: 'MNP ID' }],
      ['league_team_id', {
         title: 'League Team', 
         typeOverride: {
            type: ProfileFieldReadTypes.FK_LINK,
            typeParams: {
              propertyKey: 'league_team_id',
              profileUrl: '/admin/league_teams',
              displayKey: 'name',
            } 
          } 
        }],
      ['created_at', { title: 'Created At' }], 
    ])
  
  
  return (
    <div>
      <MnfpEntityReadProfile  
        entityId={id || ''} 
        entityApiName="league_players" 
        entityNameSingular="LeaguePlayer"   
        entityOutboundModelName="LeaguePlayerOutboundModel"  
        profileFieldTemplate={profileTemplate} 
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}