import { MnfpEntityCreateProfile, ProfileCreateTemplate, ProfileFieldCreateTypes } from "@/Components/EntityProfileComponents/MnfpEntityCreateProfile";
import {  useParams } from "react-router-dom"; 

     
  
export const AdminLeaguePlayerFantasyTeamSeasonLinkProfileCreatePage : React.FC = () => {
      
  const { id } = useParams();  
     
  const profileTemplate: ProfileCreateTemplate = new ProfileCreateTemplate([
      ['fantasy_team_season_link_id', {
        title: 'Fantasy Team Season Link', 
        typeOverride: {
          type: ProfileFieldCreateTypes.FK_LINK,
          typeParams: { 
            optionNameKeys: ['fantasy_team.name', 'season.name'],
            searchKey: 'ids',
            searchUrl: '/fantasy_team_season_links', 
          } 
        } 
      }],
    ['league_player_id', {
      title: 'League Player', 
      typeOverride: {
        type: ProfileFieldCreateTypes.FK_LINK,
        typeParams: { 
          optionNameKeys: ['name'],
          searchKey: 'name',
          searchUrl: '/league_players', 
        } 
      } 
    }], 
  ])
 
  return (
    <div>
      <MnfpEntityCreateProfile  
        entityId={id || ''} 
        entityApiName="league_player_fantasy_team_season_links" 
        entityNameSingular="League Player Fantasy Team Season Link"    
        entityInboundCreateModelName="LeaguePlayerFantasyTeamSeasonLinkInboundCreateModel"
        entityOutboundModelName="LeaguePlayerFantasyTeamSeasonLinkOutboundModel"
        profileFieldTemplate={profileTemplate} 
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}