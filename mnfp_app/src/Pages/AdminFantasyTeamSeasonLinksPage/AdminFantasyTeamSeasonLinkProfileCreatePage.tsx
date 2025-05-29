import { MnfpEntityCreateProfile, ProfileCreateTemplate, ProfileFieldCreateTypes } from "@/Components/EntityProfileComponents/MnfpEntityCreateProfile";
import {  useParams } from "react-router-dom"; 

     
  
export const AdminFantasyTeamSeasonLinkProfileCreatePage : React.FC = () => {
      
  const { id } = useParams();  
     
  const profileTemplate: ProfileCreateTemplate = new ProfileCreateTemplate([ 
    ['fantasy_team_id', {
        title: 'Fantasy Team', 
        typeOverride: {
          type: ProfileFieldCreateTypes.FK_LINK,
          typeParams: { 
            optionNameKeys: ['name'],
            searchKey: 'name',
            searchUrl: '/fantasy_teams', 
          } 
        } 
      }],
    ['season_id', {
      title: 'Season', 
      typeOverride: {
        type: ProfileFieldCreateTypes.FK_LINK,
        typeParams: { 
          optionNameKeys: ['name'],
          searchKey: 'name',
          searchUrl: '/seasons', 
        } 
      } 
    }], 
  ])
 
  return (
    <div>
      <MnfpEntityCreateProfile  
        entityId={id || ''} 
        entityApiName="fantasy_team_season_links" 
        entityNameSingular="Fantasy Team Season Link"    
        entityInboundCreateModelName="FantasyTeamSeasonLinkInboundCreateModel"
        entityOutboundModelName="FantasyTeamSeasonLinkOutboundModel"  
        profileFieldTemplate={profileTemplate} 
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}