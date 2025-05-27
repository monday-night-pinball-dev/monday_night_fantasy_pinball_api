import {  useParams } from "react-router-dom"; 
import { ProfileFieldReadTypes } from "@/Components/EntityProfileComponents/MnfpEntityProfile";
import { MnfpEntityReadProfile, ProfileReadTemplate } from "@/Components/EntityProfileComponents/MnfpEntityReadProfile";
 
export const AdminUserProfileReadPage : React.FC = () => {
      
  const { id } = useParams();  
     
  const profileTemplate: ProfileReadTemplate = new ProfileReadTemplate([
      ['name', { title: 'Name' }],
      ['username', { title: 'Username' }],
      ['league_player_id', {
         title: 'League Player', 
         typeOverride: {
            type: ProfileFieldReadTypes.FK_LINK,
            typeParams: {
              propertyKey: 'league_player_id',
              profileUrl: '/admin/league_players',
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
        entityApiName="users" 
        entityNameSingular="User"   
        entityOutboundModelName="UserOutboundModel"  
        profileFieldTemplate={profileTemplate} 
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}