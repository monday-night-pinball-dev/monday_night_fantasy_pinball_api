import { MnfpEntityCreateProfile, ProfileCreateTemplate, ProfileFieldCreateTypes } from "@/Components/EntityProfileComponents/MnfpEntityCreateProfile";
import {  useParams } from "react-router-dom";  
 
export const AdminUserProfileCreatePage : React.FC = () => {
      
  const { id } = useParams();  
   

  const profileTemplate: ProfileCreateTemplate = new ProfileCreateTemplate([ 
      ['name', { title: 'Name' }],
      ['username', { title: 'Username' }],
      ['league_player_id', {
          title: 'League Player', 
          typeOverride: {
            type: ProfileFieldCreateTypes.FK_LINK,
              typeParams: { 
                optionNameKeys: ['name'],
                searchKey: 'name_like',
                searchUrl: '/league_players', 
              } 
            } 
        }], 
    ])
  
 
  return (
    <div>
      <MnfpEntityCreateProfile 
        entityId={id || ''} 
        entityApiName="users" 
        entityNameSingular="User"  
        entityInboundCreateModelName="UserInboundCreateModel"
        entityOutboundModelName="UserOutboundModel" 
        profileFieldTemplate={profileTemplate}
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}