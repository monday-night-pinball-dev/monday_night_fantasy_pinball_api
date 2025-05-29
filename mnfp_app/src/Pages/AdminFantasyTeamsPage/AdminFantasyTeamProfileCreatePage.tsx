import {  useParams } from "react-router-dom";  
import { MnfpEntityCreateProfile, ProfileCreateTemplate, ProfileFieldCreateTypes } from "@/Components/EntityProfileComponents/MnfpEntityCreateProfile";

     
 
export const AdminFantasyTeamProfileCreatePage : React.FC = () => {
      
  const { id } = useParams();  
     
  const profileTemplate: ProfileCreateTemplate = new  ProfileCreateTemplate([ 
    ['name', { title: 'Name' }], 
    ['owner_id', {
      title: 'Owner', 
      typeOverride: {
        type: ProfileFieldCreateTypes.FK_LINK,
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
        type: ProfileFieldCreateTypes.FK_LINK,
        typeParams: {
          optionNameKeys: ['name'],
          searchKey: 'name_like',
          searchUrl: '/fantasy_leagues',
        } 
      } 
    }],  
  ]);
   
  return (
    <div>
      <MnfpEntityCreateProfile 
        entityId={id || ''} 
        entityApiName="fantasy_teams" 
        entityNameSingular="Fantasy Team"   
        entityInboundCreateModelName="FantasyTeamInboundCreateModel"
        entityOutboundModelName="FantasyTeamOutboundModel" 
        profileFieldTemplate={profileTemplate}
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}