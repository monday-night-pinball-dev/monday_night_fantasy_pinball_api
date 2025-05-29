import {  useParams } from "react-router-dom";  
import { MnfpEntityEditProfile, ProfileEditTemplate, ProfileFieldEditTypes } from "@/Components/EntityProfileComponents/MnfpEntityEditProfile";

     
 
export const AdminFantasyTeamProfileEditPage : React.FC = () => {
      
  const { id } = useParams();  
     
  const profileTemplate: ProfileEditTemplate = new  ProfileEditTemplate([ 
    ['name', { title: 'Name' }], 
    ['owner_id', {
        title: 'Owner', 
        typeOverride: {
          type: ProfileFieldEditTypes.FK_LINK,
          typeParams: {
            optionNameKeys: ['name'],
            searchKey: 'name_like',
            searchUrl: '/users',
          } 
        } 
      }],
    ['fantasy_league_id', {
        title: 'Fantasy League', 
        typeOverride: {
          type: ProfileFieldEditTypes.FK_LINK,
          typeParams: {
            optionNameKeys: ['name'],
            searchKey: 'name_like',
            searchUrl: '/fantasy_leagues',
          } 
        } 
      }], 
    ['created_at', { title: 'Created At' }], 
  ]);
   
  return (
    <div>
      <MnfpEntityEditProfile 
        entityId={id || ''} 
        entityApiName="fantasy_teams" 
        entityNameSingular="Fantasy Team"  
        entityInboundUpdateModelName="FantasyTeamInboundUpdateModel"
        entityOutboundModelName="FantasyTeamOutboundModel" 
        profileFieldTemplate={profileTemplate}
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}