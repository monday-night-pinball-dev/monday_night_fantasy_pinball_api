import {  useParams } from "react-router-dom";  
import { MnfpEntityReadProfile, ProfileFieldReadTypes, ProfileReadTemplate } from "@/Components/EntityProfileComponents/MnfpEntityReadProfile";

     
  
export const AdminFantasyTeamSeasonLinkProfileReadPage : React.FC = () => {
      
  const { id } = useParams();  
     
  const profileTemplate: ProfileReadTemplate = new ProfileReadTemplate([
      ['fantasy_team_id', {
         title: 'Fantasy Team', 
         typeOverride: {
            type: ProfileFieldReadTypes.FK_LINK,
            typeParams: {
              propertyKey: 'fantasy_team_id',
              profileUrl: '/admin/fantasy_teams',
              displayKey: 'name',
            } 
          } 
        }],
      ['season_id', {
        title: 'Season', 
        typeOverride: {
          type: ProfileFieldReadTypes.FK_LINK,
          typeParams: {
            propertyKey: 'season_id',
            profileUrl: '/admin/seasons',
            displayKey: 'name',
          } 
        } 
      }],
      ['fantasy_team_owner_id', {
        title: 'Owner', 
        typeOverride: {
          type: ProfileFieldReadTypes.FK_LINK,
          typeParams: {
            propertyKey: 'fantasy_team_owner_id',
            profileUrl: '/admin/users',
            displayKey: 'name',
          } 
        } 
      }],
      ['fantasy_league_id', {
         title: 'Fantasy League', 
         typeOverride: {
            type: ProfileFieldReadTypes.FK_LINK,
            typeParams: {
              propertyKey: 'fantasy_league_id',
              profileUrl: '/admin/fantasy_leagues',
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
        entityApiName="fantasy_team_season_links" 
        entityNameSingular="Fantasy Team Season Link"   
        entityOutboundModelName="FantasyTeamSeasonLinkOutboundModel"  
        profileFieldTemplate={profileTemplate} 
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`} 
        hideEditButton
      />
    </div>
  )
}