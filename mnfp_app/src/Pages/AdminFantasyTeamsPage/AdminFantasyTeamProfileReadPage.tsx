import {  useParams } from "react-router-dom";  
import { MnfpEntityReadProfile, ProfileFieldReadTypes, ProfileReadTemplate } from "@/Components/EntityProfileComponents/MnfpEntityReadProfile";

     
  
export const AdminFantasyTeamProfileReadPage : React.FC = () => {
      
  const { id } = useParams();  
     
  const profileTemplate: ProfileReadTemplate = new ProfileReadTemplate([
      ['name', { title: 'Name' }],
      ['owner_id', {
         title: 'Owner', 
         typeOverride: {
            type: ProfileFieldReadTypes.FK_LINK,
            typeParams: {
              propertyKey: 'owner_id',
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
        entityApiName="fantasy_teams" 
        entityNameSingular="Fantasy Team"   
        entityOutboundModelName="FantasyTeamOutboundModel"  
        profileFieldTemplate={profileTemplate} 
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}