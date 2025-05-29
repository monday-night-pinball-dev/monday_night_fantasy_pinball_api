import {  useParams } from "react-router-dom"; 
import { MnfpEntityEditProfile, ProfileEditTemplate, ProfileFieldEditTypes } from "@/Components/EntityProfileComponents/MnfpEntityEditProfile";

     
  
export const AdminUserProfileEditPage : React.FC = () => {
      
  const { id } = useParams();  
     
  const profileTemplate: ProfileEditTemplate = new ProfileEditTemplate([
      ['name', { title: 'Name' }],
      ['username', { title: 'Username' }],
      ['league_player_id', {
         title: 'League Player', 
         typeOverride: {
            type: ProfileFieldEditTypes.FK_LINK,
            typeParams: { 
              optionNameKeys: ['name'],
              searchKey: 'name_like',
              searchUrl: '/league_players',
        
            } 
          } 
        }],
      ['created_at', { title: 'Created At' }], 
    ])
  
  
  return (
    <div>
      <MnfpEntityEditProfile  
        entityId={id || ''} 
        entityApiName="users" 
        entityNameSingular="User"   
        entityInboundUpdateModelName="UserInboundUpdateModel"
        entityOutboundModelName="UserOutboundModel"  
        profileFieldTemplate={profileTemplate} 
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}