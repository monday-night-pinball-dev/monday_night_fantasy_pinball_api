import {  useParams } from "react-router-dom";  
import { MnfpEntityCreateProfile, ProfileCreateTemplate, ProfileFieldCreateTypes } from "@/Components/EntityProfileComponents/MnfpEntityCreateProfile";

     
 
export const AdminLeagueTeamProfileCreatePage : React.FC = () => {
      
  const { id } = useParams();  
     
  const profileTemplate: ProfileCreateTemplate = new  ProfileCreateTemplate([ 
    ['name', { title: 'Name' }],
    ['short_name', { title: 'Short Name' }], 
    ['home_venue_id', {
        title: 'Venue', 
        typeOverride: {
          type: ProfileFieldCreateTypes.FK_LINK,
          typeParams: {
            optionNameKeys: ['name'],
            searchKey: 'name_like',
            searchUrl: '/venues',
          } 
        } 
      }],
    ['global_mnp_id', { title: 'MNP ID' }], 
  ]);
   
  return (
    <div>
      <MnfpEntityCreateProfile 
        entityId={id || ''} 
        entityApiName="league_teams" 
        entityNameSingular="League Team"   
        entityInboundCreateModelName="LeagueTeamInboundCreateModel"
        profileFieldTemplate={profileTemplate}
        entityOutboundModelName="LeagueTeamOutboundModel"  
        baseApiUrl={`${import.meta.env.VITE_BASE_API_URL}`}/>
    </div>
  )
}