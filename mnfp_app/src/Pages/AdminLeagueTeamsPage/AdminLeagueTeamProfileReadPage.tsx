import {  useParams } from "react-router-dom"; 
import { ProfileFieldReadTypes } from "@/Components/EntityProfileComponents/MnfpEntityProfile";
import { MnfpEntityReadProfile, ProfileReadTemplate } from "@/Components/EntityProfileComponents/MnfpEntityReadProfile";

     
  
export const AdminLeagueTeamProfileReadPage : React.FC = () => {
      
  const { id } = useParams();  
     
  const profileTemplate: ProfileReadTemplate = new ProfileReadTemplate([
      ['name', { title: 'Name' }],
      ['short_name', { title: 'Short Name' }],
      ['global_mnp_id', { title: 'MNP ID' }],
      ['home_venue_id', {
         title: 'Venue', 
         typeOverride: {
            type: ProfileFieldReadTypes.FK_LINK,
            typeParams: {
              propertyKey: 'home_venue_id',
              profileUrl: '/admin/venues',
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
        entityApiName="league_teams" 
        entityNameSingular="LeagueTeam"   
        entityOutboundModelName="LeagueTeamOutboundModel"  
        profileFieldTemplate={profileTemplate} 
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}